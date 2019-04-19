import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy import nan as NA

# 处理缺失数据
# pandas的设计目标之一就是让缺失数据的处理任务尽量轻松
# pandas使用浮点值NaN表示浮点和非浮点数组中的缺失数据
# 它只是一个便于被检测出来的标记而已
# string_data = Series(['aardvark', 'artichoke', np.nan, 'avocado'])
# print(string_data)
# print(string_data.isnull())
# Python内置的None值也会被当做NA处理
# string_data[0] = None
# print(string_data.isnull())
#
# NA处理方法
# NA处理方法.png


# 滤除缺失数据
# 过滤掉缺失数据的办法有很多种
# dropna可能会更实用一些
# 对于一个Series，dropna返回一个仅含有非空数据和索引值的Series
# data = Series([1, NA, 3.5, NA, 7])
# print(data.dropna())
# 当然也可以通过布尔型索引达到这个目的
# print(data[data.notnull()])
# 而对于DataFrame对象，就会更复杂了
# 你可能希望丢弃全NA或含有NA的行或列
# dropna默认丢弃任何含有缺失值的行
# data = DataFrame([[1., 6.5, 3.], [1., NA, NA],
# 	[NA, NA, NA], [NA, 6.5, 3.]])
# cleaned = data.dropna()
# print(data)
# print(cleaned)
# 传入how='all'将只丢弃全为NA的那些行
# print(data.dropna(how='all'))
# 要用这种方式丢弃列，只需传入axis=1即可
# data[4] = NA
# print(data)
# print(data.dropna(axis=1, how='all'))
# 另一个滤除DataFrame行的问题涉及时间序列数据
# 假设你只想留下一部分观测数据，可以用thresh参数实现此目的
# 应该是保留至少有n个非NaN数据的行/列
# df = DataFrame(np.random.randn(7, 3))
# df.ix[:4, 1] = NA
# df.ix[:2, 2] = NA
# print(df)
# print(df.dropna(thresh=3))


# 填充缺失数据
# 对于大多数情况而言，fillna方法是最主要的函数
# 通过一个常数调用fillna就会将缺失值替换为那个常数值
# print(df.fillna(0))
# 若是通过一个字典调用fillna，就可以实现对不同的列填充不同的值
# print(df.fillna({1: 0.5, 3: -1}))
# fillna默认会返回新对象，但也可以对现有对象进行就地修改
# df1 = df.fillna(0, inplace=True)
# print(df1)
# reindex有效的那些插值方法也可用于fillna
# df = DataFrame(np.random.randn(6, 3))
# df.ix[2:, 1] = NA
# df.ix[4:, 2] = NA
# print(df)
# print(df.fillna(method='ffill'))
# print(df.fillna(method='ffill', limit=2))
# 只要稍微动动脑子，你就可以利用fillna实现许多别的功能
# 你可以传入Series的平均值或中位数
# data = Series([1., NA, 3.5, NA, 7])
# print(data)
# mean只计算非NA之外的数值的平均值
# print(data.mean())
# print(data.fillna(data.mean()))

# fillna函数的参数
# fillna函数的参数_1.png
# fillna函数的参数_2.png