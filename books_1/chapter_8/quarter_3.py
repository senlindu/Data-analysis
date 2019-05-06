import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import rand, randn
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


# 绘制地图：图形化显示海底地震危机数据
data = pd.read_csv('e:/datasets/haiti/Haiti.csv')
# print(data[:5])
# 每一行表示一条从某人的手机上发送的紧急或其他问题的报告
# 每个报告都有一个时间戳和位置（经度和维度）
# print(data[['INCIDENT DATE', 'LATITUDE', 'LONGITUDE']][:10])
# CATEGORY字段含有一组以逗号分隔的代码，表示消息的类型
# print(data['CATEGORY'][:6])
# 有些分类数据缺失了，因此我们需要丢弃这些数据点
# 调用describe还能发现数据中存在一些异常的地理位置
# print(data.describe())
# 清楚错误位置信息并移除缺失分类信息是一件很简单的事情
data = data[(data.LATITUDE > 18) & (data.LATITUDE < 20) &
            (data.LONGITUDE > -75) & (data.LONGITUDE < -70) &
            data.CATEGORY.notnull()]
# 现在根据分类对数据做一些分析或图形化工作，但是各个分类字段中可能含有多个分类
# 各个分类不仅有一个编码，还有一个英文名称
# 需要对数据做一些规整化处理
# 首先，编写了两个函数，一个用于获取所有分类的列表，一个用于将各个分类信息拆分为
# 编码和英语名称
# print(data['CATEGORY'][:6])


def to_cat_list(catstr):
    stripped = (x.strip() for x in catstr.split(','))
    return [x for x in stripped if x]


def get_all_categories(cat_series):
    cat_sets = (set(to_cat_list(x)) for x in cat_series)
    return sorted(set.union(*cat_sets))


def get_english(cat):
    code, names = cat.split('.')
    if '|' in names:
        names = names.split('|')[1]
    return code, names.strip()


# 测试get_english函数是否工作正常
# print(get_english('2. Urgences logistiques | Vital Lines'))
# 将编码跟名称映射起来的字典，等会要用编码进行分析
# 这里用的是生成器表达式，而不是列表推导式
all_cats = get_all_categories(data.CATEGORY)
# print(all_cats)
# 生成器表达式
english_mapping = dict(get_english(x) for x in all_cats)
# print(english_mapping['2a'])
# print(english_mapping['6c'])
# 根据分类选取记录的方式有很多，其中之一是添加指标（或哑变量）列，每个分类一列
# 首先抽取出唯一的分类编码，并构造一个全零DataFrame（列为分类编码，索引跟data
# 的索引一样）


def get_code(seq):
    return [x.split('.')[0] for x in seq if x]


all_codes = get_code(all_cats)
code_index = pd.Index(np.unique(all_codes))
dummy_frame = DataFrame(np.zeros((len(data), len(code_index))), index=data.index,
                        columns=code_index)
# print(dummy_frame.ix[:, :6])
# 将各行中适当的项设置为1， 然后再与data进行连接
for row, cat in zip(data.index, data.CATEGORY):
    codes = get_code(to_cat_list(cat))
    dummy_frame.ix[row, codes] = 1

data = data.join(dummy_frame.add_prefix('category_'))
# 现在data有了一些新的列
# print(data.ix[:, 10:15])
# 由于是空间坐标数据，希望吧数据绘制在海地的地图上
# basemap工具集，(http://matplotlib.github.com/basemap, matplotlib的一个插件)
# 使得我们能够用Python在地图上绘制2D数据
# basemap提供了许多不同的地球投影以及一种将地球上的经纬度坐标投影转换为二维matplotlib
# 图的方式
# 绘制一张简单的黑白海地地图


def basic_haiti_map(ax=None, lllat=17.25, urlat=20.25, lllon=-75, urlon=-71):
        # 创建极球面投影的Basemap实例
    m = Basemap(ax=ax, projection='stere',
                lon_0=(urlon + lllon) / 2,
                lat_0=(urlat + lllat) / 2,
                llcrnrlat=lllat, urcrnrlat=urlat,
                llcrnrlon=lllon, urcrnrlon=urlon,
                resolution='f')
    # 绘制海岸线、州界、国界以及地图边界
    m.drawcoastlines()
    m.drawstates()
    m.drawcountries()
    return m


# 现在的问题，如何让返回的这个Basemap对象知道该怎样将坐标转换到画布上
# 对于每一个分类，在数据集中找到对应的坐标，并在适当的subplot中绘制一个
# Basemap，转换坐标，然后通过Basemap的plot方法绘制点：
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10))
fig.subplots_adjust(hspace=0.05, wspace=0.05)

to_plot = ['2a', '1', '3c', '7a']

lllat = 17.25
urlat = 20.25
lllon = -75
urlon = -71

for code, ax in zip(to_plot, axes.flat):
    m = basic_haiti_map(ax, lllat=lllat, urlat=urlat,
                        lllon=lllon, urlon=urlon)
    cat_data = data[data['category_%s' % code] == 1]

    # 计算地图的投影坐标
    x, y = m(cat_data.LONGITUDE, cat_data.LATITUDE)

    m.plot(x, y, 'k.', alpha=0.5)
    ax.set_title('%s: %s' % (code, english_mapping[code]))

    plt.show()
# basemap还可以叠加来自shapefile的地图数据
# 下载一个带有太子港道路的shapefile
# Basemap对象有一个非常方便的readshapefile方法，在解压完道路数据文件之后，
# 在代码中加以下几行就可以了
# shapefile_path = filepath
# m.readshapefile(shapefile_path, 'roads')
# 