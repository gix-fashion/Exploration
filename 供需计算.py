
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np


import sys

args = sys.argv 

input1 = "补货信息.csv"  # 补货信息的文件路径
input2 = "gbk" #编码方式
output = "sku_need.csv"#输出

if len(args)>1:
    input1 = args[1]
if len(agrs)>2:
    input2 = args[2]


df = pd.read_csv(input1,encoding = input2) #补货数据


def season(i):
    if i in [3,4,5]:
        return "春"
    if i in [6,7,8]:
        return "夏"
    if i in [9,10,11]:
        return "秋"
    if i in [12,1,2]:
        return "冬"
    return np.nan
    

#清洗
df["AvgLastWeekSaleQty"].fillna(0,inplace = True)
df['LastWeekMoveQty'].fillna(0,inplace = True)
df["LastWeekSaleQty"]=((df["AvgLastWeekSaleQty"]*7).apply(round))

df["Year"] = pd.to_datetime(df["StockDate"]).apply(lambda x:x.strftime("%Y")).astype("int")
df["Month"] =  pd.to_datetime(df["StockDate"]).apply(lambda x:x.strftime("%m")).astype("int")
df["Season"] = df["Month"].apply(season)
df["当年"] =(df["Year"].astype("int")==df["YearNo"].astype(int)).astype("int")
df["当季"] =(df["Season"]==df["SeasonName"]).astype("int")





storage = df['LastWeekInitQty'] + df['LastWeekMoveQty'] - df['LastWeekSaleQty']
total_need = df['LastWeekSaleQty'] * df['CZPSuppleRate'] + df['DisPlayQty'] #需求= 上周销量 * 畅滞平系数 + 陈列需求 – 现有库存

#计算需求减去库存
need = total_need-storage
#考虑Sku & Skc的CZP
def czp(df_):
    skc = df_["SKCCzpFlag"]
    sku = df_["CZPFlag"]
    if(skc in ["滞","超滞"]):
        return -1
    elif(skc =="平"):
        if(sku in ["滞","超滞"]):
            return -1
    if(skc in ["畅","爆"]):
        return 1
    elif(skc =="平"):
        if(sku in ["畅","爆"]):
            return 1
    return 0    
    
czp_coefficient =df.apply(czp,axis =1)#SKC为 滞销 超滞销的 可以 供出 SKC为 平， 其 SKU 为滞销 超滞销的，可以供出

                                      # SKC 为 畅销 爆款 可以 提出需求 SKC 为 平， 其SKU 为 畅销 爆款的， 可以提出需求    
need_coefficient = ((need>0).astype("int"))*2-1

need_sku = need*czp_coefficient 
need_sku= need_sku+abs(need_sku)#只保留大于零的，表示供需consistent
need_sku = need_sku*need_coefficient #赋予符号


df["SkuNeed"] = need_sku
df["need_coefficient"]=need_coefficient

df.to_csv(output,index = False)

