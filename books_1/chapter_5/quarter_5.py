import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy import nan as NA

# 层次化索引
# 层次化索引是pandas的一项重要功能，它使你能在一个轴上拥有多个
# （两个以上）索引级别。
# 它使你能以低纬度形式处理高维度数据
# 创建一个Series，并用一个由列表或数组组成的列表作为索引
# data = Series(np.random.randn(10),
#               index=[['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'd', 'd'],
#                      [1, 2, 3, 1, 2, 3, 1, 2, 2, 3]])
# print(data)
# 这就是带有MultiIndex索引的Series的格式化输出形式
# 索引之间的“间隔”表示“直接使用上面的标签”
# print(data.index)
# 对于一个层次化索引的对象，选取数据子集的操作很简单
# print(data['b'])
# print(data['b':'c'])
# print(data.ix[['b', 'd']])
# 有时甚至可以在“内层”中进行选取
# print(data[:, 2])
# 层次化索引在数据重塑和基于分组的操作（如透视表生成）中扮演中重要角色
# 例如，这段数据可以通过其UNstack方法被重新安排到一个DataFrame中
# print(data.unstack())
# unstack的逆运算是stack
# print(data.unstack().stack())
# 对于一个DataFrame，每条轴都可以有分层索引
# frame = DataFrame(np.arange(12).reshape((4, 3)),
#                   index=[['a', 'a', 'b', 'b'], [1, 2, 1, 2]],
#                   columns=[['Ohio', 'Ohio', 'Colorado'],
#                            ['Green', 'Red', 'Green']])
# print(frame)
# 各层都可以有名字（可以是字符串，也可以是别的Python对象）
# 如果指定了名称，它们就会显示在控制台输出中（不要将索引名称跟轴标签混为一谈）
# frame.index.names = ['key1', 'key2']
# frame.columns.names = ['state', 'color']
# print(frame)
# 由于有了分部的列索引，因此可以轻松选取列分组
# print(frame['Ohio'])
# 可以单独创建MultiIndex然后复用
# 上面那个DataFrame中的（分级的）列可以这样创建
# MultiIndex.from_arrays([['Ohio', 'Ohio', 'Colorado'],
# 	['Green', 'Red', 'Green']], names=['state', 'color'])


# 重排分级顺序
# 有时，你需要重新调整某条轴上各级别的顺序，或根据指定级别上的值对数据进行排序
# swaplevel接受两个级别编号或名称，并返回一个互换了级别的新对象（但数据不会发生变化）
# print(frame.swaplevel('key1', 'key2'))
# 而sortlevel则根据单个级别中的值对数据进行排序（稳定的）
# 交换级别时，常常也会用到sortlevel，这样最终结果就是有序的
# sortlevel is deprecated, use sort_index(level= ...)
# print(frame.sort_index(level=1))
# print(frame.swaplevel(0, 1).sort_index(level=0))
# 注意：在层次化索引的对象上，如果索引是按字典方式从外到内排序
# （即调用sort_index的结果），数据选取操作的性能要好很多


# 根据级别汇总统计
# 许多对DataFrame和Series的描述和汇总统计都有一个level选项，
# 用于指定在某条轴上求和的级别。
# 以上面DataFrame为例，可以根据行或列上的级别进行求和
# print(frame.sum(level='key2'))
# print(frame.sum(level='color', axis=1))
# 这其实是利用了pandas的groupby功能


# 使用DataFrame的列
# 经常需要将DataFrame的一个或多个列当做行索引来用，或者可能希望
# 将行索引变成DataFrame的列
frame = DataFrame({'a': range(7), 'b': range(7, 0, -1),
                   'c': ['one', 'one', 'one', 'two', 'two', 'two', 'two'],
                   'd': [0, 1, 2, 0, 1, 2, 3]})
print(frame)
# DataFrame的set_index函数会将其一个或多个列转换为行索引，并创建
# 一个新的DataFrame
frame2 = frame.set_index(['c', 'd'])
print(frame2)
# 默认情况下，那些列会从DataFrame中移除，但也可以保留下来
print(frame.set_index(['c', 'd'], drop=False))
# reset_index的功能与set_index刚好相反，层次化索引的级别会被
# 转移到列里面
print(frame2.reset_index())