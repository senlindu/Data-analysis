import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import rand, randn

# 数据聚合与分组运算
# 对数据集进行分组并对各组应用一个函数，是数据分析工作的重要环节
# 将数据集准备好之后，通常的任务就是计算分组统计或生成透视表
# pandas提供了一个灵活高效的groupby功能，使你能以一种自然的方式对
# 数据集进行切片、切块、摘要等操作

# 关系型数据库和SQL能够流行的原因之一就是其能够方便地对
# 数据进行连接、过滤、转换和聚合
# 分组运算
# 1、根据一个或多个键（可以是函数、数组或DataFrame列名）拆分pandas对象
# 2、计算分组摘要统计，如计数、平均值、标准差、或用户自定义函数
# 3、对DataFrame的列应用各种各样的函数
# 4、应用组内转换或其他运算，如规格化、线性回归、排名或选取子集等
# 5、计算透视表或交叉表
# 6、拆分分位数分析以及其他分组分析


# GroupBy技术
# 分组运算的第一个阶段，pandas对象中的数据会根据你提供的一个或多个键被拆分为多组
# 然后，将一个函数应用到各个分组并产生一个新值
# 最后，所有这些函数的执行结果会被合并到最终的结果对象中
# 结果对象的形式一般取决于数据上所执行的操作

# 分组聚合过程
# groupby过程.png

# 分组键可以有多种形式，且类型不必相同：
# 1、 列表或数组，其长度与带分组的轴一样
# 2、表示DataFrame某个列名的值
# 3、字典或Series，给出待分组轴上的值与分组名之间的对应关系
# 4、函数，用于处理轴索引或索引中的各个标签
# 注意，后三种都只是快捷方式而已，最终目的仍然是产生一组用于拆分对象的值
# df = DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
#                 'key2': ['one', 'two', 'one', 'two', 'one'],
#                 'data1': randn(5),
#                 'data2': randn(5)})
# print(df)
# 假设按照key1进行分组，并计算data1列的平均值，实现该功能的方式很多
# 访问data1， 并根据key1调用groupby
# grouped = df['data1'].groupby(df['key1'])
# print(grouped)
# 变量grouped是一个GroupBy对象
# 实际上还没有进行任何计算，只是含有一些有关分组键df['key1']的中间数据而已
# 该对象已经有了接下来对各分组执行运算所需的一切信息
# 可以调用GroupBy的mean方法来计算分组平均值
# print(grouped.mean())
# 数据根据分组键进行了聚合，产生了一个新的Series，其索引为key1列中的唯一值
# 如果我们一次传入多个数组，就会得到不同的结果
# means = df['data1'].groupby([df['key1'], df['key2']]).mean()
# print(means)
# 通过两个键对数据进行了分组，得到的Series具有一个层次化索引
# print(means.unstack())
# 实际上，分组键可以是任何长度适当的数组
# states = np.array(['Ohio', 'California', 'California', 'Ohio', 'Ohio'])
# years = np.array([2005, 2005, 2006, 2005, 2006])
# print(df['data1'].groupby([states, years]).mean())
# 你还可以将列名（可以是字符串、数字或其他Python对象）用作分组键
# df.groupby('key1').mean()
# df.groupby(['key1', 'key2']).mean()
# 无论你准备拿groupby做什么，都可能会用到GroupBy的size方法，返回一个
# 含有分组大小的Series
# print(df.groupby(['key1', 'key2']).size())


# 对分组进行迭代
# GroupBy对象支持迭代，可以产生一组二元元组（由分组名和数据块组成）
# df = DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
#                 'key2': ['one', 'two', 'one', 'two', 'one'],
#                 'data1': randn(5),
#                 'data2': randn(5)})
# for name, group in df.groupby('key1'):
#     print(name)
#     print(group)
# 对于多重键的情况，元组的第一个元素将会是由键值组成的元组
# for (k1, k2), group in df.groupby(['key1', 'key2']):
#     print(k1, k2)
#     print(group)
# 当然你可以对这些数据片段做任何操作，有一个你可能会觉得有用的运算，将这些数据
# 片段做成一个字典
# pieces = dict(list(df.groupby('key1')))
# print(pieces['b'])
# groupby默然是在axis=0上进行分组的，通过设置也可以在其他任何轴上进行分组
# 可以根据dtype对列进行分组
# print(df.dtypes)
# grouped = df.groupby(df.dtypes, axis=1)
# print(dict(list(grouped)))


# 选取一个或一组列
# 对于由DataFrame产生的GroupBy对象，如果用一个（单个字符串）或
# 一组（字符串数组）列名对其进行索引，就能实现选取部分列进行聚合
# 的目的
# df.groupby('key1')['data1']
# df.groupby('key1')['data1']
# 是以下代码的语法糖
# df['data1'].groupby(df['key1'])
# df[['data2']].groupby(df['key1'])
# 尤其对于大数据集，很可能只需要对部分列进行聚合
# print(df.groupby(['key1', 'key2'])[['data2']].mean())
# 这种索引操作返回的对象是一个已分组的DataFrame(如果传入的是列表或数组)或
# 已分组的Series（如果传入的是标量形式的单个列名）
# s_grouped = df.groupby(['key1', 'key2'])['data2']
# print(s_grouped)
# print(s_grouped.mean())


# 通过字典或Series进行分组
# 除数组以外，分组信息还可以其他形式存在
# people = DataFrame(randn(5, 5),
#                    columns=['a', 'b', 'c', 'd', 'e'],
#                    index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
# people.ix[2:3, ['b', 'c']] = np.nan
# print(people)
# 假设已知列的分组关系，并希望根据分组计算列的总计
# mapping = {'a': 'red', 'b': 'red', 'c': 'blue',
#            'd': 'blue', 'e': 'red', 'f': 'orange'}
# 现在只需将这个字典传给groupby即可
# by_column = people.groupby(mapping, axis=1)
# print(by_column)
# print(by_column.sum())
# Series也有同样的功能，可以被看做一个固定大小的映射
# 如果用Series作为分组键，pandas会检查Series以确保其索引跟分组
# 轴是对齐的
# map_series = Series(mapping)
# print(map_series)
# print(people.groupby(map_series, axis=1).count())


# 通过函数进行分组
# 相较于字典或Series，Python函数在定义分组映射关系时可以更有创意且更为抽象
# 任何被当做分组键的函数都会在各个索引值上呗调用一次，其返回值就会被用作分组名称
# 假设你希望根据人名的长度进行分组，虽然可以求取一个字符串长度数组，但其实仅仅传入
# len函数就可以了
# people = DataFrame(randn(5, 5),
#                    columns=['a', 'b', 'c', 'd', 'e'],
#                    index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
# print(people.groupby(len).sum())
# 将函数跟数组、列表、字典、Series混合使用也不是问题，因为任何东西最终都会被转换为数组
# key_list = ['one', 'one', 'one', 'two', 'two']
# print(people.groupby([len, key_list]).min())


# 根据索引级别分组
# 层次化索引数据集最方便的地方就在于他能够根据索引级别进行聚合
# 通过level关键字传入级别编号或名称既可
columns = pd.MultiIndex.from_arrays([['US', 'US',
                                      'US', 'JP', 'JP'], [1, 3, 5, 1, 3]],
                                    names=['cty', 'tenor'])
hier_df = DataFrame(randn(4, 5), columns=columns)
print(hier_df)
print(hier_df.groupby(level='cty', axis=1).count())
