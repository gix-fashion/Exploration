# Exploration
可以发现某些衣服具有季节效应，因此决定对地区，月份，货品名称，颜色，尺码进行独热编码

## data

### sales_total_sku.csv  : 整合了所有的sale_date的数据后join了sku的信息，无匹配sku信息的占极少数，因此舍弃掉了
整合了4199366条数据。join之后包括4196640条数据， columns = ['sale_no', 'sale_date_x', 'channel_id', 'sale_price', 'sku_id',
       'Quantity', 'goods_no', 'goods_name', 'color_id', 'color_name', 'long',
       'size_name', 'brand', 'category', 'category_sub', 'years', 'season',
       'sale_date_y', 'tag_price', 'material', 'series', 'designer',
       'barcode']
       
https://drive.google.com/file/d/1cvF-dC0ALavUm0FtvcPm7_usboufcaUq/view?usp=sharing

### sales_total_sku_channel.csv： 在上述数据中又join了channel_date的信息，由于四分之一多的没有匹配相关信息，因此是left join，保存了无channel信息的数据
columns = ['sale_no', 'sale_date', 'channel_id', 'sale_price', 'sku_id', 'Quantity', 'goods_no', 'goods_name', 'color_id', 'color_name', 'long', 'size_name', 'brand', 'category', 'category_sub', 'years', 'season','sale_date_sku', 'tag_price', 'material', 'series', 'designer','barcode', 'channel_no', 'channel_name', 'nation', 'province', 'city','county', 'address', 'channel_type', 'area', 'open_date', 'close_date','shopping_guide_quantity']


https://drive.google.com/open?id=1lMcOcIRbq5FcJs18vg00vuBu8Q_iHDOI


### 定义了销售时的季节： 345春，678夏， 9 10 11秋， 12 1 2冬
