import numpy as np
import pandas as pd
from pandas import DataFrame, Series


# 重塑和轴向旋转
# 有许多用于重新排列表格型数据的基础运算。这些函数也称作重塑或轴向旋转运算


# 重塑层次化索引
# 层次化索引为DataFrame数据的重排任务提供了一种具有良好一致性的方式，主要功能有二
# stack：将数据的列旋转为行
# unstack：将数据的行旋转为列
data = DataFrame(np.arange(6).reshape((2, 3)),
                 index=pd.Index(['Ohio', 'Colorado'], name='state'),
                 columns=pd.Index(['one', 'two', 'three'], name='number'))
# print(data)
# 使用该数据的stack方法既可将列转换为行，得到一个Series
result = data.stack()
# print(result)
# 对于一个层次化索引的Series，你可以用unstack将其重排为一个DataFrame
# print(result.unstack())
# 默认情况下，unstack操作的是最内层（stack也是如此），传入分层级别的编号或名称既可对
# 其他级别进行unstack操作
print(result.unstack(0))
print(result.unstack('state'))
# 如果不是所有的级别都能在各分组中找到的话，则unstack操作可能会引入缺失数据
s1 = Series([0, 1, 2, 3], index=['a', 'b', 'c', 'd'])
s2 = Series([4, 5, 6], index=['c', 'd', 'e'])
data2 = pd.concat([s1, s2], keys=['one', 'two'])
print(data2.unstack())
# stack默认会滤除缺失数据，因此该运算是可逆的
print(data2.unstack.stack())
print(data2.unstack().stack(dropna=False))
# 在对DataFrame进行unstack操作时，作为旋转轴的级别将会成为结果中的最低级别
df = DataFrame({'left':result, 'right':result + 5,
	columns=pd.Index(['left', 'right'], name='side')})
print(df)


# 将长格式旋转为宽格式
# 时间序列数据通常是以所谓的长格式或堆叠格式存储在数据库或CSV中的
# 关系型数据库中的数据经常都是这样存储的，因为固定架构有一个好处，随着表中数据的增加或删除，
# item列中的值的种类能够增加或减少
# 使用DataFrame的pivot方法完全可以实现这个转换
# pivoted = ldata.pivot('date', 'item', 'value')
# print(pivoted.head())
# 前两个参数值分别做行和列索引的列名，最后一个参数则是用于填充DataFrame的数据列的列名
# 假设有两个需要参与重塑的数据列
# ldata['value2'] = np.random.randn(len(ldata))
# ldata[:10]
# 如果忽略最后一个参数，得到的DataFrame就会带有层次化的列
# pivoted = ldata.pivot('date', 'item')
# print(pivoted[:5])
# pivoted['value'][:5]
# 注意，pivot其实只是一个快捷方式而已，用set_index创建层次化索引，再用unstack重塑
# unstacked = ldata.set_index(['date', 'item']).unstack('item')
# print(unstacked[:7])
# 