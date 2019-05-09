import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
from matplotlib import rcParams
from matplotlib.collections import LineCollection
import shapefile
# import dbflib


# 示例：2012联邦选举委员会数据库
# 数据包括赞助者的姓名、职业、雇主、地址以及出资额等信息
# （P00000001-ALL.csv）
fec = pd.read_csv('e:/datasets/fec/P00000001-ALL.csv')
# print(fec[:10])
# print(fec.ix[123456])
# 不难看出，该数据中没有党派信息，因此最好把它加进去
# 通过unique，可以获取全部的候选人名单
unique_cands = fec.cand_nm.unique()
# print(unique_cands)
# 最简单的办法是利用字典说明党派关系
parties = {'Bachmann, Michelle': 'Repubican',
           'Cain, Herman': 'Repubican',
           'Gingrich, Newt': 'Repubican',
           'Huntsman, Jon': 'Repubican',
           'Johnson, Gary Earl': 'Repubican',
           'McCotter, Thaddeus G': 'Repubican',
           'Obama, Barack': 'Democrat',
           'Paul, Ron': 'Repubican',
           'Pawlenty, Timothy': 'Repubican',
           'Perry, Rick': 'Repubican',
           "Roemer, Charles E. 'Buddy' III": 'Repubican',
           'Romney, Mitt': 'Repubican',
           'Santorum, Rick': 'Repubican'}
# 现在，通过这个映射以及Series对象的map方法，你可以根据勾选人姓名得到一组党派信息
# print(fec.cand_nm[123456:123461])
# print(fec.cand_nm[123456:123461].map(parties))
# 将其添加为一个新列
fec['party'] = fec.cand_nm.map(parties)
# print(fec['party'].value_counts())
# 两个需要注意的地方
# 第一，该数据既包括赞助也包括退款（负的出资额）
# print((fec.contb_receipt_amt > 0).value_counts())
# 为了简化分析过程，此处限定该数据集只能有正的出资额
fec = fec[fec.contb_receipt_amt > 0]
# 由于Barack Obama和Mitt Romney是最主要的两名候选人，专门准备一个子集，
# 只包含针对他们两人的竞选活动的赞助信息
fec_mrbo = fec[fec.cand_nm.isin(['Obama, Barack', 'Romney, Mitt'])]

# 根据职业和雇主统计赞助信息
# 基于职业的赞助信息统计是另一种经常被研究的统计任务
# 根据职业计算出资总额
# print(fec.contbr_occupation.value_counts()[:10])
# 许多职业都设计相同的基本工作类型，或者同一样东西有多种变体
# 清理数据（将一个职业信息映射到另一个）
# 这里巧妙地利用dict.get，它允许没有映射关系的职业也能“通过”
occ_mapping = {'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
               'INFORMATION REQUESTED': 'NOT PROVIDED',
               'INFORMATION REQUESTED (BEST EFFORTS)': 'NOT PROVIDED',
               'C.E.O.': 'CEO'}
# 如果没有提供相关映射，则返回x


def f(x): return occ_mapping.get(x, x)


fec.contbr_occupation.map(f)

# 对雇主信息也进行同样的处理
emp_mapping = {'INFORMATION REQUESTED PER BEST EFFORTS': 'NOT PROVIDED',
               'INFORMATION REQUESTED': 'NOT PROVIDED',
               'SELF': 'SELF-EMPLOYED',
               'SELF EMPLOYED': 'SELF-EMPLOYED'}
# 如果没有提供相关映射，则返回x


def f(x): return emp_mapping.get(x, x)


fec.contbr_employer = fec.contbr_employer.map(f)
# 现在你可以通过pivot_table根据党派和职业对数据进行聚合，然后
# 过滤掉总出资额不足200万美元的数据
# rows更新为index
# cols更新为columns
by_occupation = fec.pivot_table('contb_receipt_amt',
                                index='contbr_occupation',
                                columns='party', aggfunc='sum')
over_2mm = by_occupation[by_occupation.sum(1) > 2000000]
# print(over_2mm)
# 把这些数据做成柱状图看起来会更加清楚
over_2mm.plot(kind='barh')
# plt.show()
# 想要分析对Obama和Romney总出资额最高的职业和企业
# 对候选人进行分组，然后使用本章前面介绍的那种求取最大值的方法


def get_top_amounts(group, key, n=5):
    totals = group.groupby(key)['contb_receipt_amt'].sum()
    # 根据key对totals进行降序排列
    return totals.sort_values(ascending=False)[:n]


# 根据职业和雇主进行聚合
grouped = fec_mrbo.groupby('cand_nm')
# print(grouped.apply(get_top_amounts, 'contbr_occupation', n=7))
# print(grouped.apply(get_top_amounts, 'contbr_employer', n=10))

# 对出资额分组
# 还可以对该数据做另一种非常实用的分析
# 利用cut函数根据出资额的大小将数据离散化到多个面元中
bins = np.array([0, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000])
labels = pd.cut(fec_mrbo.contb_receipt_amt, bins)
# print(labels)
# 然后根据候选人姓名以及面元标签对数据进行分组
grouped = fec_mrbo.groupby(['cand_nm', labels])
# print(grouped.size().unstack(0))
# 从这个数据中可以看出，在小额度赞助方面，Obama获得的数量比Romney多得多
# 还可以对出资额求和并在面元内规格化，以便图形化显示两位候选人各种赞助额度的比例
bucket_sums = grouped.contb_receipt_amt.sum().unstack(0)
# print(bucket_sums)
normed_sums = bucket_sums.div(bucket_sums.sum(axis=1), axis=0)
# print(normed_sums)
normed_sums[:-2].plot(kind='barh', stacked=True)
# plt.show()
# 排除了两个最大的面元，因为这些不是个人捐赠的
# 还可以对该分析过程做许多的提炼和改进
# 可以根据赞助人的姓名和邮编对数据聚合，以便找出哪些人进行了多次小额捐赠，
# 哪些人又进行了一次或多次大额捐款

# 根据州统计赞助信息
# 首先根据候选人和州对数据进行聚合
grouped = fec_mrbo.groupby(['cand_nm', 'contbr_st'])
totals = grouped.contb_receipt_amt.sum().unstack(0).fillna(0)
totals = totals[totals.sum(1) > 100000]
# print(totals[:10])
# 如果对各行除以总赞助额，就会得到各候选人在各州的总赞助额比例
percent = totals.div(totals.sum(1), axis=0)
print(percent[:10])
# 找到有关州界的shape file（http://nationalatlas.gov/atlasftp.html?openChapters=chpbound）
obama = percent['Obama, Barack']

fig = plt.figure(figsize=(12, 12))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

lllat = 21
urlat = 53
lllon = -118
urlon = -62

# shapefile
# https://www.cnblogs.com/nygfcn1234/p/3399605.html
# geopandas
# https://blog.csdn.net/gwj992/article/details/82744576
m = Basemap(ax=ax, projection='stere',
            lon_0=(urlon + lllon) / 2,
            lat_0=(urlat + lllat) / 2,
            llcrnrlat=lllat,
            urcrnrlat=urlat,
            llcrnrlon=lllon,
            urcrnrlon=urlon,
            resolution='l')
m.drawcoastlines()
m.drawcountries()

shp = ShapeFile('.../states/statessp020')
dbf = dbflib.open('../states/statessp020')

for npoly in range(shp.info()[0]):
    # 在地图上绘制彩色多边形
    shpsegs = []
    shp_object = shp.read_object(npoly)
    verts = shp_object.vertices()
    rings = len(verts)
    for rings in range(rings):
        lons, lats = zip(*verts[ring])
        x, y = m(lons, lats)
        shpsegs.append(zip(x, y))
        if ring == 0:
            shapedict = dbf.read_record(npoly)
        name = shapedict['STATE']
    lines = LineCollection(shpsegs, antialiaseds=(1, ))

    # state_to_code字典，例如'ALASKA' -> 'AK'， omitted
    try:
        per = obama[state_to_code[name.upper()]]
    except KeyError:
        continue

    lines.set_facecolors('k')
    lines.set_alpha(0.75 * per)
    lines.set_edgecolors('k')
    lines.set_linewidth(0.3)
plt.show()
