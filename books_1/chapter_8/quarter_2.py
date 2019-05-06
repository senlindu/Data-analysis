import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
from numpy.random import randn, rand, normal


# pandas中的绘图函数
# matplotlib实际上是一种比较低级的工具
# 要组装一张图表，需要用它的各种基础组件才行：
# 数据展示（图表类型：线型图、柱状图、盒形图、散布图、等值线图）、图例、标题、刻度标签以及
# 其他注解型信息
# 根据数据制作一张完整的图表通常都需要用到多个对象
# 在pandas中，我们有行标签、列标签以及分组信息
# pandas有许多能够利用DataFrame对象数据组织特点来创建标准图表的高级绘图方法


# 线型图
# Series和DataFrame都有一个用于生成各类图表的plot方法
# 默认情况下，它们所生成的是线型图
# s = Series(randn(10).cumsum(), index=np.arange(0, 100, 10))
# s.plot()
# plt.show()
# 该Series对象的索引会被传给matplotlib，并用以绘制X轴，可以通过use_index=False禁用
# X轴的刻度和界限可以通过xticks和xlim选项进行调节，Y轴就用yticks和ylim
# pandas的大部分绘图方法都有一个可选的ax参数，它可以是一个matplotlib的subplot对象
# 这使你能够在网络布局中更为灵活地处理subplot的位置

# DataFrame的plot方法会在一个subplot中为各列绘制一条线，并自动创建图例
# df = DataFrame(randn(10, 4).cumsum(0), columns=['A', 'B', 'C', 'D'],
#                index=np.arange(0, 100, 10))
# df.plot()
# plt.show()
# 注意：plot的其他关键字参数会被传给相应的matplotlib绘图函数，所以更深入地自定义图表，
# 必须学习更多有关matplotlib API的知识


# Series.plot方法的参数
# series-plot_1.png
# series-plot_2.png


# DataFrame还有一些用于对列进行灵活处理的选项
# 专用于DataFrame的plot参数
# DataFrame-plot.png


# 柱状图
# 在生成线型图的代码中加上kind='bar'（垂直柱状图）或kind='barh'（水平柱状图）
# 即可生成柱状图。Series和DataFrame的索引将会被用作X或Y刻度
# fig, axes = plt.subplots(2, 1)
# data = Series(rand(16), index=list('abcdefghijklmnop'))
# data.plot(kind='bar', ax=axes[0], color='k', alpha=0.7)
# data.plot(kind='barh', ax=axes[1], color='k', alpha=0.7)
# plt.show()
# 对于DataFrame，柱状图会将每一行的值分为一组
# df = DataFrame(rand(6, 4),
#                index=['one', 'two', 'three', 'four', 'five', 'six'],
#                columns=pd.Index(['A', 'B', 'C', 'D'], name='Genus'))
# print(df)
# df.plot(kind='bar')
# plt.show()
# 注意，DataFrame各列的名称“Genus”被用作了图例的标题
# 设置stacked=True即可为DataFrame生成堆积柱状图，这样每行的值就会被堆积在一起
# df.plot(kind='barh', stacked=True, alpha=0.5)
# plt.show()
# 注意：柱状图有一个非常不错的用法：利用value_counts图形化显示Series中各值的
# 出现频率，比如s.value_count().plot(kind='bar')
# examples/tips.csv
# 做一张堆积柱状图展示每天各种聚会规模的数据点的百分比
# 将数据加载进来，根据日期和聚会规模创建一张交叉表
# tips = pd.read_csv('e:/examples/tips.csv')
# print(tips[:5])
# print(tips.day)
# size不能用于列名，tips.size会计算总长度
# print(tips.times)
# party_counts = pd.crosstab(tips['day'], tips['times'])
# print(party_counts)
# party_counts = party_counts.ix[:, 2:5]
# 然后进行规格化，使得各行的和为1（必须转换成浮点数，以避免整数除法问题），生成图表
# 规格化成"和为1"
# party_pcts = party_counts.div(party_counts.sum(1).astype(float), axis=0)
# print(party_pcts)
# party_pcts.plot(kind='bar', stacked=True)
# plt.show()
# 从该数据集可以看出，聚会规模在周末会变大


# 直方图和密度图
# 直方图是一种对值频率进行离散化显示的柱状图
# 数据点被拆分到离散的、间隔均匀的面元中，绘制的是个面元中数据点的数量
# 再以前面那个小费数据为例，通过Series的hist方法，可以声称一张“小费
# 占消费总额百分比”的直方图
# tips = pd.read_csv('e:/examples/tips.csv')
# print(tips)
# tips['tip_pct'] = tips['tip'] / tips['total_bill']
# tips['tip_pct'].hist(bins=50)
# plt.show()
# 与此相关的一种图表类型是密度图，是通过计算“可能会产生观测数据的连续概率分布的估计”
# 而产生的。一般的过程是将该分布近似为一组核（即正态（高斯）分布之类的较为简单的分布）
# 调用plot时加上kind='kde'即可生成一张密度图（标准混合正态分布KDE）
# tips['tip_pct'].plot(kind='kde')
# plt.show()
# 这两种图表常常会被画在一起。直方图以规格化形式给出（以便给出面元化密度），然后
# 再在其上绘制核密度估计。
# comp1 = normal(0, 1, size=200)
# comp2 = normal(10, 2, size=200)
# values = Series(np.concatenate([comp1, comp2]))
# # normed换成density
# values.hist(bins=100, alpha=0.3, color='k', density=True)
# values.plot(kind='kde', style='k--')
# plt.show()


# 散布图
# 散布图是观察两个一维数据序列之间的关系的有效手段
# matplotlib的scatter方法是绘制散布图的主要方法
# 加载statesmodels项目的macrodata数据集，选择其中几列，计算对数差
# macro = pd.read_csv('e:/examples/macrodata.csv')
# data = macro[['cpi', 'm1', 'tbilrate', 'unemp']]
# trans_data = np.log(data).diff().dropna()
# print(trans_data[-5:])
# 利用plt.scatter即可轻松绘制一张简单的散布图
# plt.scatter(trans_data['m1'], trans_data['unemp'])
# plt.title('Changes in log %s vs. log %s' % ('m1', 'unemp'))
# plt.show()
# 在探索式数据分析工作中，同时观察一组变量的散布图是很有意义的，也被成为散布图矩阵
# pandas提供了一个能从DataFrame创建散布图矩阵的scatter_matrix函数，还支持在对角
# 线上放置各变量的直方图或密度图
# pd.scatter_matrix被pd.plotting.scatter_matrix替代
# pd.plotting.scatter_matrix(trans_data, diagonal='kde', color='k', alpha=0.3)
# plt.show()
