
# coding: utf-8

# ## 调用常用包和定义常用函数
# 

# In[25]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt

from sklearn.naive_bayes import BernoulliNB
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

#将catogorical的feature转换成numerical
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


#把月份转换成季节
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

#定义了我们所沿用的损失函数
def loss_function(y_pred,y_test,d):
    loss = []
    for i in range(d):
        error = abs(y_pred[:,i]-y_test[:,i])
        scaled = (error/y_pred[:,i])*100
        score = scaled.mean()
        print(score) #舍弃周次的encode
        loss.append(score)

        
input1 = "1_22中类销售/"  # 中类销售的文件路径
input2 = "gbk" #编码方式
output1 = "standard.csv"#输出数据
output2 = "中类data训练数据.csv"#输出训练数据

if len(args)>1:
    input1 = args[1]
if len(agrs)>2:
    input2 = args[2]
if len(agrs)>3:
    input3= args[3]
if len(agrs)>4:
    output = args[4]    
            
        
get_ipython().run_line_magic('matplotlib', 'inline')


# In[102]:


def sub(string):
    string = string.replace("10","十")
    string = string.replace("1","一")
    string = string.replace("2","二")
    string = string.replace("3","三")
    string = string.replace("4","四")
    string = string.replace("5","五")
    string = string.replace("6","六")
    string = string.replace("7","七")
    string = string.replace("8","八")
    string = string.replace("9","九")
    return string
#df0 = df0[df0["波段"].apply(lambda x : "波段" in x)]
#df0["波段"]=df0["波段"].apply(sub)


# In[233]:


import os
ls = os.listdir(input1)
wasd= ['棉衣', '皮鞋']#这两个的字段名称不一样

df0 = pd.DataFrame()
for file in ls:
    if not (file.split("销售")[0] in wasd):
        df = pd.read_csv("1_22中类销售/"+file,encoding =input2)
        df0 = pd.concat([df0,df])
#预处理

df0["首销月"]= pd.to_datetime(df0["首销日"]).apply(lambda x:x.strftime("%m")).astype("int")

df0["首销季节"] = df0["首销月"].apply(season)

df0["首销年"]= pd.to_datetime(df0["首销日"]).apply(lambda x:x.strftime("%y")).astype("int")


# ## 训练模型

# In[236]:


def train_predict(x,y):
    lr = LinearRegression()
    lr.fit(x,y)
    return(lr.predict(19))
    


# In[238]:


df0["销量"] = 0
df0["销额"] = 0
df0.fillna(0,inplace=True)
for i in range(12):
    df0["销量"]+=df0["第"+str(i+1)+"周销量"]
    df0.drop("第"+str(i+1)+"周销量",axis=1,inplace = True)
    df0["销额"]+= df0["第"+str(i+1)+"周销额"]
    df0.drop("第"+str(i+1)+"周销额",axis=1,inplace = True)


# In[239]:


encode_text_dummy(df0,"商品年份")


# In[240]:


#将不同年的销量销额encode到不同列当中去
for i in [2015,2016,2017,2018,2019]:
    df0["商品年份-"+str(i)+"-销量"] = df0["商品年份-"+str(i)]* df0["销量"]
    df0["商品年份-"+str(i)+"-销额"] = df0["商品年份-"+str(i)]* df0["销额"]


# In[242]:


cols = df0.columns[20:]

df1 = df0.groupby(["分公司","中类","小类","季节","首销月"])[cols].sum()#.reset_index()


# In[249]:


df1 = df1.reset_index()
df1.to_csv(output2,index = False)


# In[263]:


df1["商品年份-2019-销量-同比"]=df1.apply(lambda x: train_predict([[16],[17],[18]],[ x["商品年份-"+str(i)+"-销量"] for i in [2016,2017,2018]])[0],axis = 1)

df1["商品年份-2019-销额-同比"]=df1.apply(lambda x: train_predict([[16],[17],[18]],[ x["商品年份-"+str(i)+"-销额"] for i in [2016,2017,2018]])[0],axis = 1)


# In[293]:


df1["2019-销量-相对误差"]=(df1["商品年份-2019-销量"]-df1["商品年份-2019-销量-同比"])/(df1["商品年份-2019-销量-同比"]+0.001)


# In[294]:


df1["2019-销额-相对误差"]=(df1["商品年份-2019-销额"]-df1["商品年份-2019-销额-同比"])/(df1["商品年份-2019-销额-同比"]+0.01)


# In[295]:


def Ringratio(df):
    n = df.shape[0]
    if n>1:
        df.loc[1:,"商品年份-2019-销额-环比修正项"]=df.loc[:n-1,"2019-销额-相对误差"]*df.loc[:n-1,"商品年份-2019-销额-同比"]*0.5
        df.loc[1:,"商品年份-2019-销量-环比修正项"]=df.loc[:n-1,"2019-销量-相对误差"]*df.loc[:n-1,"商品年份-2019-销量-同比"]*0.5
    return df    


# In[296]:


df1["商品年份-2019-销额-环比修正项"]=0
df1["商品年份-2019-销量-环比修正项"]=0


# In[297]:


df2 = df1.groupby(["分公司","中类","小类","季节"]).apply(Ringratio)


# In[302]:


df2["商品年份-2019-销额-环比修正后"]=df2["商品年份-2019-销额-同比"]+df2["商品年份-2019-销额-环比修正项"]
df2["商品年份-2019-销量-环比修正后"]=df2["商品年份-2019-销量-同比"]+df2["商品年份-2019-销量-环比修正项"]


# In[305]:


df2.to_csv(output1,index = False)

