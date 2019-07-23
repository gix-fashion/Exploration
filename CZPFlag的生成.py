
# coding: utf-8




import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt
import math
import os
import sys
from sklearn.naive_bayes import BernoulliNB
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
def encode_text_dummy(df, name):
    dummies = pd.get_dummies(df[name])
    for x in dummies.columns:
        dummy_name = "{}-{}".format(name, x)
        df[dummy_name] = dummies[x]
    df.drop(name, axis=1, inplace=True)
def encode_text_index(df, name):
    le = preprocessing.LabelEncoder()
    df[name] = le.fit_transform(df[name])
    return le.classes_    

get_ipython().run_line_magic('matplotlib', 'inline')

args = sys.argv 

input1 = "补货信息.csv"  # 补货信息的文件路径
input2 = "商品指标标准.xlsx" #商品指标的文件路劲
input3 = "result的副本" #李蕊学姐输出文件夹的路径
input4 = 1             #是否按照李蕊学姐的文件重新整理分公司的文件，如果否则需要输入0
input5 = "销售占比/"    #输出分公司文件的文件夹
if len(args)>1:
    input1 = args[1]
if len(agrs)>2:
    input2 = args[2]
if len(agrs)>3:
    input3 = args[3]
if len(agrs)>4:
    input4 = args[4]
if len(agrs)>5:
    input5 = args[5]
#读取数据，并且计算周数
df =pd.read_csv(input1,encoding="gbk")
df["LastWeekSaleQty"]=((df["AvgLastWeekSaleQty"]*7).apply(round))


df["Weeks"]=(pd.to_datetime(df.StockDate)-pd.to_datetime(df.FirstInStockDate)).apply(lambda x:int(x.days/7)+1)
df["Weeks"] = df["Weeks"].apply(lambda x: 12 if x>12 else x)



#将李蕊学姐的文件转换成分公司的
if bool(input4):
    ls = list(map(lambda x:x.split("销售")[0],os.listdir(input3)))
    
    
    
    
    df_ = pd.DataFrame()
    for item in ls:
        df__ = pd.read_csv(input3+"/"+item+"销售.csv") 
        df__["中类"] = item
        df_ = pd.concat((df_,df__),ignore_index =True,sort = False)
    
    df_.drop("Unnamed: 0",axis = 1,inplace = True)
    
    
    groupby = df_.groupby("分公司")
    for name, group in groupby:
        group.to_csv(input5+name+".csv",index = False)




# ### 生成CZP




standard = pd.read_excel(input2)
standard.rename({"店铺代码":"ShopCode","在店库存件数\n（下限值）":"StorageMin","陈列SKC标准":"SkcNum","齐码率":"UniformRate"},axis = 1,inplace =True)





df_full = pd.merge(df,standard,on ="ShopCode").copy()
groupby = df_full.groupby("分公司")
def accumulate(df1,df2):
    sum_ = 0
    for i in range[df1["Weeks"]]:
        sum_ += df2["第"+str(i+1)+"周销量占比"][df1["ModelName"]]
    return sum_    
def to_zcp(x,y):
    if x>y:
        return("爆")
    elif x>(0.75*y):
        return("畅")
    elif x>(0.5*y):
        return("平")
    elif x>(0.25*y):
        return("滞")
    elif x:
        return("超滞")
    
for name, group in groupby:
    mid = pd.read_csv(input5+name+"分公司"+".csv")                        #中类的标准,SKU
    mid.set_index("中类",inplace = True)
    group["Y"] = group.apply(lambda x: accumulate(x,mid))
    group["X_sku"] = (group['TotalSaleQty']/group['TotalMoveQty'])*0.5+0.5*(group['LastWeekSaleQty']/(group['LastWeekInitQty']+group['LastWeekMoveQty']))
    group["X_skc"] = (group['SKCTotalSaleQty']/group['SKCTotalMoveQty'])*0.5+0.5*(group['SKCLastWeekSaleQty']/(group['SKCLastWeekInitQty']+group['SKCLastWeekMoveQty']))
    group['CZPFlag'] = group.apply(lambda x: to_czp(x["X_sku"],x["Y"]))
    group['SKCCZPFlag'] = group.apply(lambda x: to_czp(x["X_skc"],x["Y"]))
    group.to_csv(name+"补货数据.csv",)

