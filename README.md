data_pre:包括了鞋子，裤子，衬衫的预处理数据，为发售开始前八周的数据


KMpre.csv :https://drive.google.com/open?id=1VdSq17AvE3wQjRoS7pLVn3SqQYRAdaNU

# Exploration
可以发现某些衣服具有季节效应，因此决定对地区，月份，货品名称，颜色，尺码进行独热编码

## data

### sales_total_sku.csv  : 整合了所有的sale_date的数据后join了sku的信息，无匹配sku信息的占极少数，因此舍弃掉了

https://drive.google.com/open?id=1cvF-dC0ALavUm0FtvcPm7_usboufcaUq

### sales_total_sku_channel.csv： 在上述数据中又join了channel_date的信息，由于四分之一多的没有匹配相关信息，因此是left join，保存了无channel信息的数据
columns = ['sale_no', 'sale_date', 'channel_id', 'sale_price', 'sku_id', 'Quantity', 'goods_no', 'goods_name', 'color_id', 'color_name', 'long', 'size_name', 'brand', 'category', 'category_sub', 'years', 'season','sale_date_sku', 'tag_price', 'material', 'series', 'designer','barcode', 'channel_no', 'channel_name', 'nation', 'province', 'city','county', 'address', 'channel_type', 'area', 'open_date', 'close_date','shopping_guide_quantity']


https://drive.google.com/open?id=1lMcOcIRbq5FcJs18vg00vuBu8Q_iHDOI


### 定义了销售时的季节： 345春，678夏， 9 10 11秋， 12 1 2冬

### goods.csv： 筛选了货品特征，仅包括了很必要的渠道特征

https://drive.google.com/open?id=1BVHQKsN215BHZX-tfeo8-WTSwGe0eaGk
### goods_channel.csv: 筛选了货品特征，包括了渠道特征

https://drive.google.com/open?id=1_yA66yAo6QRu0x_Zxdi66s2sRlT5y9SL



年份.zip :https://drive.google.com/open?id=1nngLn_XwArSI9zxMsecLGZgf8ZdSP8Sd
店铺.zip:https://drive.google.com/open?id=1y0Aylt3a8YHW-MPtaetl0Y_2gNDUkXei
purchase_info.csv :https://drive.google.com/open?id=1BVwZdkWWuJIRHc7Co02Hjr5DKfXVcAIa
purchase_2013.csv:https://drive.google.com/open?id=1U1EBO3ukqhk6Lie8_UkfZ5A52qNPc8oF

