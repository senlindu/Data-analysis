import numpy as np
import pandas as pd
from pandas import DataFrame, Series


# 数据分析和建模方面的大量编程工作都是用在数据准备上的：加载、清理、转换以及重塑
# 合并数据集
# pandas对象中的数据可以通过一些内置的方式进行合并
# pandas.merge可根据一个或多个键将不同DataFrame中的行连接起来。SQL或其他关系型数据库的用户对此
# 应该会比较熟悉，因为它实现的就是数据库的连接操作
# pandas.concat可以沿着一条轴将多个对象堆叠到一起
# 实例方法combine_first可以将重复数据编接在一起，用一个对象中的值填充另一个对象中的缺失值


# 数据库风格的DataFrame合并
# 数据集的合并或连接运算时通过一个或多个键将行链接起来的
# 这些运算是关系型数据库的核心
# pandas的merge函数是对数据应用这些算法的主要切入点
# df1 = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
# 'data1': range(7)})
# df2 = DataFrame({'key': ['a', 'b', 'd'], 'data2': range(3)})
# print(df1)
# print(df2)
# 这是一种多对一的合并
# df1中的数据由多个被标记为a和b的行，而df2的key列的每个值则仅对应一行
# 对这些对象调用merge即可得到
# print(pd.merge(df1, df2))
# 注意，并没有指明要用哪个列进行连接
# 如果没有指定，merge就会将重叠列的列名当作键
# 不过，最好显式指定一下
# print(pd.merge(df1, df2, on='key'))
# 如果两个对象的列名不同，也可以分别进行指定
# df3 = DataFrame({'lkey': ['b', 'b', 'a', 'c', 'a', 'a', 'b'],
#                  'data1': range(7)})
# df4 = DataFrame({'rkey': ['a', 'b', 'd'], 'data2': range(3)})
# print(pd.merge(df3, df4, left_on='lkey', right_on='rkey'))
# 默认情况下，merge做的是"inner"连接，结果中的键是交集
# 其他方式还有"left", "right"以及"outer"
# 外连接求取的是键的并集，组合了左连接和右连接的效果
# print(pd.merge(df1, df2, how='outer'))
# 多对多的合并操作非常简单，无需额外的工作
# df1 = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],
#                  'data1': range(6)})
# df2 = DataFrame({'key': ['a', 'b', 'a', 'b', 'd'], 'data2': range(5)})
# print(df1)
# print(df2)
# print(pd.merge(df1, df2, on='key', how='left'))
# 多对多连接产生的是行的笛卡尔积
# 由于左边的DataFrame有3个"b"行，右边的有2个，最终结果中有6个"b"行
# 连接方式只影响出现在结果中的键
# print(pd.merge(df1, df2, how='inner'))
# 要根据多个键进行合并，传入一个由列名组成的列表即可
# left = DataFrame({'key1': ['foo', 'foo', 'bar'],
#                   'key2': ['one', 'two', 'one'],
#                   'lval': [1, 2, 3]})
# right = DataFrame({'key1': ['foo', 'foo', 'bar', 'bar'],
#                    'key2': ['one', 'one', 'one', 'two'],
#                    'rval': [4, 5, 6, 7]})
# print(left)
# print(right)
# print(pd.merge(left, right, on=['key1', 'key2'], how='outer'))
# 结果中会穿线哪些键组合取决于所选的合并方式
# 多个键形成一系列元组，并将其当做单个连接键（当然，实际上不是这么回事）
# 警告：在进行列-列连接时，DataFrame对象中的索引会被丢弃
# 对于合并原酸需要考虑的最后一个问题是对重复列名的处理
# 虽然你可以手工处理列名重叠的问题，但merge有一个更实用的suffixes选项，用于
# 指定附加到左右两个DataFrame对象的重叠列名上的字符串
# print(pd.merge(left, right, on='key1'))
# print(pd.merge(left, right, on='key1', suffixes=('_left', '_right')))

# merge函数的参数
# merge函数的参数_1.png
# merge函数的参数_2.png


# 索引上的合并
# 有时候，DataFrame中的连接键位于其索引中
# 你可以传入left_index=True或right_index=True（或两个都传，以说明索引应该被用作
# 连接键）
# left1 = DataFrame({'key': ['a', 'b', 'a', 'a', 'b', 'c'], 'value': range(6)})
# right1 = DataFrame({'group_val': [3.5, 7]}, index=['a', 'b'])
# print(left1)
# print(right1)
# print(pd.merge(left1, right1, left_on='key', right_index=True))
# 由于默认的merge方法是求取连接键的交集，因此你可以通过外连接的方式得到它们的并集
# print(pd.merge(left1, right1, left_on='key', right_index=True, how='outer'))
# 对于层次化索引的数据，事情就有点复杂了
# lefth = DataFrame({'key1': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
#                    'key2': [2000, 2001, 2002, 2001, 2002],
#                    'data': np.arange(5.)})
# righth = DataFrame(np.arange(12).reshape((6, 2)),
#                    index=[['Nevada', 'Nevada', 'Ohio', 'Ohio', 'Ohio', 'Ohio'],
#                           [2001, 2000, 2000, 2000, 2001, 2002]],
#                    columns=['event1', 'event2'])
# print(lefth)
# print(righth)
# 这种情况下，你必须以列表的形式指明用作合并键的多个列（注意对重复索引值的处理）
# print(pd.merge(lefth, righth, left_on=['key1', 'key2'], right_index=True))
# print(pd.merge(lefth, righth, left_on=['key1', 'key2'], right_index=True, how='outer'))
# 同时使用合并双方的索引也没问题
# left2 = DataFrame([[1, 2], [3, 4], [5, 6]], index=['a', 'c', 'e'],
#                   columns=['Ohio', 'Nevada'])
# right2 = DataFrame([[7, 8], [9, 10], [11, 12], [13, 14]],
#                    index=['b', 'c', 'd', 'e'], columns=['Missouri', 'Alabama'])
# print(left2)
# print(right2)
# print(pd.merge(left2, right2, how='outer', left_index=True, right_index=True))
# DataFrame还有一个join实例方法，它能更为方便地实现按索引合并
# 它还可用于合并多个带有相同或相似索引的DataFrame对象，而不管他们之间有没有重叠的列
# print(left2.join(right2, how='outer'))
# 它还支持参数DataFrame的索引跟调用者DataFrame的某个列之间的连接
# print(left1.join(right1, on='key'))
# 对于简单的索引合并，你还可以向join传入一组DataFrame
# another = DataFrame([[7, 8], [9, 10], [11, 12], [16, 17]],
#                     index=['a', 'c', 'e', 'f'],
#                     columns=['New York', 'Oregon'])


# print(left2.join([right2, another]))
# print(left2.join([right2, another], how='outer'))


# 轴向连接
# 另一种数据合并运算也被称作连接、绑定或堆叠
# numpy有一个用于合并原始numpy数组的concatenation函数
# arr = np.arange(12).reshape((3, 4))
# print(arr)
# print(np.concatenate([arr, arr], axis=1))
# 对于pandas对象，带有标签的轴使你能够进一步推广数组的连接运算
# 具体来说，你还需要考虑以下这些东西
# 1、如果各对象其他轴上的索引不同，那些轴应该是做并集还是交集
# 2、结果对象中的分组需要各不相同吗
# 3、用于连接的轴重要吗
# pandas的concat函数提供了一种能够解决这些问题的可靠方式
# 假设有三个没有重叠索引的Series
# s1 = Series([0, 1], index=['a', 'b'])
# s2 = Series([2, 3, 4], index=['c', 'd', 'e'])
# s3 = Series([5, 6], index=['f', 'g'])
# 对这些对象调用concat可以将值和索引黏合在一起
# print(pd.concat([s1, s2, s3]))
# 默认情况下，concat是在axis=0上工作的，最终产生一个新的Series
# 如果传入axis=1，则结果就会变成一个DataFrame(axis=1是列)
# print(pd.concat([s1, s2, s3], axis=1))
# 这种情况下，另外一条轴上没有重叠，从索引的有序并集（外连接）上就可以看出来
# 传入join='inner'即可得到它们的交集
# s4 = pd.comcat([s1 * 5, s3])
# print(pd.concat([s1, s4], axis=1))
# print(pd.concat([s1, s4], axis=1, join='inner'))
# 你可以通过join_axes指定要在其他轴上使用的索引
# print(pd.concat([s1, s4], axis=1, join_axes=[['a', 'c', 'b', 'e']]))
# 参与连接的片段在结果中区分不开
# 假设你想要在连接轴上创建一个层次化索引，使用keys参数即可达到这个目的
# result = pd.concat([s1, s1, s3], keys=['one', 'two', 'three'])
# print(result)
# print(result.unstack())
# 如果沿着axis=1对Series进行合并，则keys就会成为DataFrame的列头
# print(pd.concat([s1, s2, s3], axis=1, keys=['one', 'two', 'three']))
# 同样的逻辑对DataFrame对象也是一样
# df1 = DataFrame(np.arange(6).reshape(3, 2),
#                 index=['a', 'b', 'c'], columns=['one', 'two'])
# df2 = DataFrame(5 + np.arange(4).reshape(2, 2),
#                 index=['a', 'c'], columns=['three', 'four'])
# print(pd.concat([df1, df2], axis=1, keys=['level1', 'level2']))
# 如果传入的不是列表而是一个字典，则字典的键就会被当做keys选项的值
# print(pd.concat({'level1':df1, 'level2':df2}, axis=1))
# 此外还有两个用于管理层次化索引创建方式的参数
# print(pd.concat([df1, df2], axis=1, keys=['level1', 'level2'],
# 	names=['upper', 'lower']))
# 最后一个需要考虑的问题是，跟当前分析工作无关的DataFrame行索引
# df1 = DataFrame(np.random.randn(3, 4), columns=['a', 'b', 'c', 'd'])
# df2 = DataFrame(np.random.randn(2, 3), columns=['b', 'd', 'a'])
# print(df1)
# print(df2)
# 在这种情况下，传入ignore_index=True即可
# print(pd.concat([df1, df2], ignore_index=True))


# concat函数的参数
# concat函数的参数.png


# 合并重叠数据
# 还有一种数据组合问题不能用简单的合并或连接运算来处理
# 比如，你可能有索引全部或部分重叠的两个数据集。给这个例子增加一点启发性，我们使用
# numpy的where函数，它用于表达一种矢量化的if-else
a = Series([np.nan, 2.5, np.nan, 3.5, 4.5, np.nan],
           index=['f', 'e', 'd', 'c', 'b', 'a'])
b = Series(np.arange(len(a), dtype=np.float64),
           index=['f', 'e', 'd', 'c', 'b', 'a'])
b[-1] = np.nan
# print(a)
# print(b)
# print(np.where(pd.isnull(a), b, a))
# Series有一个combine_first方法，实现的也是一样的功能，而且会进行数据对齐
print(b[:-2].combine_first(a[2:]))
# 对于DataFrame，combine_first自然也会在列上做同样的事情，因此你可以将其看做
# 用参数对象中的数据为调用者对象的缺失数据“打补丁”
df1 = DataFrame({'a': [1, np.nan, 5., np.nan],
                 'b': [np.nan, 2., np.nan, 6.], 'c': range(2, 18, 4)})
df2 = DataFrame({'a': [5., 4., np.nan, 3., 7.],
                 'b': [np.nan, 3., 4., 6., 8.]})
print(df1.combine_first(df2))
