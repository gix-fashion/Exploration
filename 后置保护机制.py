
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np


import sys

args = sys.argv 

input1_1 = "当年当季/results_mm.csv"  # 当年当季
input1_2 = "当年当季/sku_list_mm.csv" #sku
input1_3 = "当年当季/store_list_mm.csv"#store

input2_1 = "不当年不当季/results_nn.csv"  # 不当年不当季
input2_2 = "不当年不当季/sku_list_nn.csv" #sku
input2_3 = "不当年不当季/store_list_nn.csv"#store

input3_1 = "当年不当季/results_mn.csv"  # 当年不当季
input3_2 = "当年不当季/sku_list_mn.csv" #sku
input3_3 = "当年不当季/store_list_mn.csv"#store

input4_1 = "不当年但当季/results_nm.csv"  # 不当年但当季
input4_2 = "不当年但当季/sku_list_nm.csv" #sku
input4_3 = "不当年但当季/store_list_nm.csv"#store

input_long = "623_results_nj.csv"

df_long = pd.read_csv(input_long)


# In[ ]:


df1_ = pd.read_csv(input1_1)
df1_ = df1_[-(df1_.drop(["0","1"],axis = 1)==0).all(axis = 1)]
df_sku1_ = pd.read_csv(input1_2)
df_store1_ = pd.read_csv(input1_3)

#对邓神数据的再处理
df_store1_.drop('Unnamed: 0',axis = 1, inplace = True)
df_sku1_.drop('Unnamed: 0',axis = 1, inplace = True)
df_sku1_.rename({"0":"MatCode","1":"SizeName"},axis = 1 ,inplace = True)


# In[ ]:


df2_ = pd.read_csv(input2_1)
df2_ = df2_[-(df2_.drop(["0","1"],axis = 1)==0).all(axis = 1)]
df_sku2_ = pd.read_csv(input2_2)
df_store2_ = pd.read_csv(input2_3)

#对邓神数据的再处理
df_store2_.drop('Unnamed: 0',axis = 1, inplace = True)
df_sku2_.drop('Unnamed: 0',axis = 1, inplace = True)
df_sku2_.rename({"0":"MatCode","1":"SizeName"},axis = 1 ,inplace = True)


# In[ ]:


df3_ = pd.read_csv(input3_1)
df3_ = df3_[-(df3_.drop(["0","1"],axis = 1)==0).all(axis = 1)]
df_sku3_ = pd.read_csv(input3_2)
df_store3_ = pd.read_csv(input3_3)

#对邓神数据的再处理
df_store3_.drop('Unnamed: 0',axis = 1, inplace = True)
df_sku3_.drop('Unnamed: 0',axis = 1, inplace = True)
df_sku3_.rename({"0":"MatCode","1":"SizeName"},axis = 1 ,inplace = True)


# In[ ]:


df4_ = pd.read_csv(input4_1)
df4_ = df4_[-(df4_.drop(["0","1"],axis = 1)==0).all(axis = 1)]
df_sku4_ = pd.read_csv(input4_2)
df_store4_ = pd.read_csv(input4_3)

#对邓神数据的再处理
df_store4_.drop('Unnamed: 0',axis = 1, inplace = True)
df_sku4_.drop('Unnamed: 0',axis = 1, inplace = True)
df_sku4_.rename({"0":"MatCode","1":"SizeName"},axis = 1 ,inplace = True)


# In[ ]:


#计算求和
df1_["sum"] = df1_.sum(axis =1) - df1_["0"] - df1_["1"]

df2_["sum"] = df2_.sum(axis =1) - df2_["0"] - df2_["1"]

df3_["sum"] = df3_.sum(axis =1) - df3_["0"] - df3_["1"]

df4_["sum"] = df4_.sum(axis =1) - df4_["0"] - df4_["1"]


# In[ ]:


df1_["最小包裹保护"] = df1_["sum"].apply(lambda x:(x<4))
df1_["最小包裹保护后"] =  df1_["sum"].apply(lambda x:0 if x<4 else x)


# In[ ]:


dic_store1_ = df_store1_.T.to_dict("records")[0]
df1_["发出"] =df1_["0"].apply(lambda x: dic_store1_[x-1])

df1_["接收"] = df1_["1"].map(lambda x: dic_store1_[x-1]) #检索


# In[ ]:


dic_store2_ = df_store2_.T.to_dict("records")[0]
df2_["发出"] =df2_["0"].apply(lambda x: dic_store2_[x-1])

df2_["接收"] = df2_["1"].map(lambda x: dic_store2_[x-1]) #检索


# In[ ]:


dic_store3_ = df_store3_.T.to_dict("records")[0]
df3_["发出"] =df3_["0"].apply(lambda x: dic_store3_[x-1])

df3_["接收"] = df3_["1"].map(lambda x: dic_store3_[x-1]) #检索


# In[ ]:


dic_store4_ = df_store4_.T.to_dict("records")[0]
df4_["发出"] =df4_["0"].apply(lambda x: dic_store4_[x-1])

df4_["接收"] = df4_["1"].map(lambda x: dic_store4_[x-1]) #检索


# In[ ]:


##当年当季保护
def dd(df,df2):  #df为当年当季 df2为其他的，进行过商店转码，并且计算过sum

    df2["是否随当年当季"] = df2.apply(lambda x:(df[(df["发出"]==x["发出"])*(df["接收"]==x["接收"])*(-df["最小包裹保护"])].shape[0]>0),axis =1)
    df2["最小包裹保护"]=False
    df2["最小包裹保护"][-df2["是否随当年当季"]] = df2["sum"][-df2["是否随当年当季"]].apply(lambda x:(x<10))
    df2["最小包裹保护后"] = df2["sum"]
    df2["最小包裹保护后"][df2["最小包裹保护"]] =0
dd(df1_,df2_)    
dd(df1_,df3_)
dd(df1_,df4_)


# In[ ]:


## 接收sku编号，店铺编号，找到原数据集中的对应记录，并加以改变，然后留下原数据集的记录，一行算完之后传回包裹数据集

def backprop(sku,store,df,sku_list):
    matcode = sku_list.loc[sku,"MatCode"]
    sizename = sku_list.loc[sku,"SizeName"]
    return df[(df["MatCode"]==matcode)*(df["SizeName"]==sizename)*(df["ShopCode"]==store)]


ls_protect = ['调入不调出保护', 'top保护', '满场率的保护', '库存量保护', '尾数清零保护']


df_long["最小包裹保护"] = False
for df in[df1_,df2_,df3_,df4_]:
    for column in ls_protect:
        df[column]=False        #将最小包裹保护回传，再将原记录转移到现在包裹记录上面
    for i in range(df.shape[0]):    
        sku = df.columns[df.iloc[i]!=0] #得到i行里面非零的列名
        l1=False
        l2=False
        l3=False
        l4=False
        l5=False
        for column in sku[2:-5]:   
            v=backprop(int(column)-2,df.iloc[i]["接收"],df_long,df_sku).loc[:,ls_protect]#.columns[:]
            if v.shape[0]>0:
                ind = v.index[0]
    
                va = v.values[0]
        
                df_long.loc[ind]["最小包裹保护"] = df.iloc[i]["最小包裹保护"] 
                l1=l1|bool(va[0])
                l2=l2|bool(va[1])
                l3=l3|bool(va[2])
            
                l4=l4|bool(va[3])
                l5=l5|bool(va[4])
            
           
        
        df.iloc[i][ls_protect[0]] = l1  
        df.iloc[i][ls_protect[1]] = l2
        df.iloc[i][ls_protect[2]] = l3
        df.iloc[i][ls_protect[3]] = l4
        df.iloc[i][ls_protect[4]] = l5
        


# In[ ]:


df_long.to_csv("results.csv")
df1_.to_csv("当年当季.csv")
df2_.to_csv("不当年不当季.csv")
df3_.to_csv("当年不当季.csv")
df4_.to_csv("不当年但当季.csv")

