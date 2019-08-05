
import pandas as pd
import numpy as np


import sys

args = sys.argv 

input1 = "sku_need.csv"  # 补货信息的文件路径
input2 = "utf-8" #编码方式
input3 = "standard.csv"#保护值标准
output = "sku_results.csv"#输出

if len(args)>1:
    input1 = args[1]
if len(args)>2:
    input2 = args[2]
if len(args)>3:
    input3= args[3]
if len(args)>4:
    output = args[4]    
   
    
df = pd.read_csv(input1,encoding = input2) #补货数据
standard = pd.read_csv(input3)#标准



standard.rename({"店铺代码":"ShopCode","在店库存件数\n（下限值）":"StorageMin","陈列SKC标准":"SkcNum","齐码率":"UniformRate"},axis = 1,inplace =True)

df_ = pd.merge(df,standard,on ="ShopCode").copy()
df_["top保护"] = 0
df_["满场率的保护"] = 0
df_["库存量保护"] = 0
df_["调入不调出保护"] = 0
mask= (df_["need_coefficient"]<0) #调出的
df_["调入不调出保护"][mask*(df_["LastWeekMoveQty"]>0)] = 1 #上周调入过，且这周想要调出的sku，被保护


###

 
### 保护

#2.5调入不调出保护，第一遍过滤,如果上周有调入则不调出,但是可以调入
mask= (df_["need_coefficient"]<0) #调出的
df_["SkuNeed"][mask]=df_["SkuNeed"][mask]*(df_["LastWeekMoveQty"][mask]<=0)
df_["调入不调出保护"] = 0
df_["调入不调出保护"][mask*(df_["LastWeekMoveQty"]>0)] = 1 #记录
#2.7(top保护) 由于top保护比较简单，可以先用top保护进行一遍过滤
group = df_.groupby(by = "ShopCode",sort = False)
def top(df):
    
    df_temp = df.sort_values(by = "LastWeekSaleQty",ascending = False)
    if(df.shape[0]>19):
        lst = df_temp.index[:20]
    else:
        lst = df_temp.index
    df["SkuNeed"][lst]  =0 
    df["top保护"][lst] = 1
    return df
df_=group.apply(top)

###

 
"""
#2.8(最小包裹保护) 由于最小包裹保护也会改变满场率，放在库存量保护之前
group = df_.groupby(by = "ShopCode",sort = False)
def minpackage(df):
    mask = (abs(df["SkuNeed"])<3)
    df["SkuNeed"][mask]=0
    return df
df_ = group.apply(minpackage)    
"""
#2.6尾数清零保护,整款（skc）调出
group = df_.groupby(by = "ShopCode",sort = False)
def clean(df):
    mask =(((df["Qty"]+df["SkuNeed"])==0)*df["SizeCoreFlag"]*(df["SkuNeed"]<0)==1) #找到导致缺码且要调出的sku
    skc = df["MatCode"][mask] #进而找到缺码的skc的编号
    mask=df["MatCode"].apply(lambda x: True if x in skc.values else False) #把缺码的全部调出,这行代码找到全部调出skc的sku
    df["SkuNeed"][mask] = df["Qty"][mask]  #全部调出
    df["尾数清零保护"] = mask  #记录是否导致了缺码以及清零，用于之后的齐码率保护
    return df

df_=group.apply(clean)


###

 
# 2.3(库存量保护)  以及2.1(满场率保护)
##在这里我们判断调出后是否满足库存量以及满场率，如果不满足则优先保留调出导致断码的货品（提升满场率），
##并且优先保留调出需求小的（可提升满场率以及库存量）
group = df_.groupby(by = "ShopCode",sort = False)
def MinSkc(df):#满场率的保护
    
    mask =(((df["Qty"]+df["SkuNeed"])==0)*df["SizeCoreFlag"])==1 #断码的货品
    skc = df["MatCode"][mask] #进而找到缺码的skc的编号
    mask=df["MatCode"].apply(lambda x: False if x in skc.values else True) #找出所有齐码的
    skc_num = df["MatCode"][mask].value_counts().size
    diff=int(skc_num-df["SkcNum"].mean())
    if diff<0: #如果不满足满场率
        if(df["MatCode"][df["尾数清零保护"]].value_counts().size<=(-diff)):
            df["SkuNeed"][df["尾数清零保护"]]=0
            df["满场率的保护"][df["尾数清零保护"]]=1
            df["尾数清零保护"]=False #因断码而被清空的货品全部用来恢复满场率
            
        else:
            lst=df[df["SkuNeed"]<0].groupby(by = "MatCode",sort = False)["SkuNeed"].sum().sort_values(ascending = False).index[:-diff]
            mask =df["MatCode"].apply(lambda x: True if x in lst.values else False)#挑选出相应skc
            df["SkuNeed"][mask] = 0
            df["尾数清零保护"][mask]=False
            df["满场率的保护"][mask] = 1
            
    return df    
df_ = group.apply(MinSkc) 
group = df_.groupby(by = "ShopCode",sort = False)


###

 

def MinStorageProtect(df):
    
    store =(df["Qty"]+df["SkuNeed"] ).sum()#库存
    diff =int( store - df["StorageMin"].mean())
    if diff<0: #如果不满足最低库存，则优先保留调出需求最大的，因为之前经过了满场率的清洗，所以满场率不重要，库存重要
        df_temp = df[df["SkuNeed"]<0].sort_values(by = "SkuNeed",ascending = True)
        sum_ = 0
        for ind in df_temp.index.values:
            sum_+=abs(df["SkuNeed"][ind])
            df["SkuNeed"][ind] =0
            df["库存量保护"][ind] = 1
            if (sum_+diff)>=0:
                break
        mask =(((df["Qty"]+df["SkuNeed"])==0)*df["SizeCoreFlag"]*(df["SkuNeed"]<0)==1) #找到导致缺码且要调出的sku
        df["尾数清零保护"] = mask  #更新是否导致了缺码以及清零，避免出现错误
    return df 
df_=group.apply(MinStorageProtect)

###

 

df_final = df_.reset_index(drop = True)
df_final.to_csv(output,index = False)


mask1 = (df_final["当季"]==1).astype("int")
mask2 = (df_final["当年"]==1).astype("int")

df_final[(mask1*mask2).astype("bool")].to_csv("当年当季_623.csv",index = False)
df_final[(mask1*(1-mask2)).astype("bool")].to_csv("不当年但当季_623.csv",index = False)
df_final[((1-mask1)*(1-mask2)).astype("bool")].to_csv("不当年不当季_623.csv",index = False)
df_final[((1-mask1)*mask2).astype("bool")].to_csv("当年不当季_623.csv",index = False)
