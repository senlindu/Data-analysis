import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from pandas_datareader import data as web

# 汇总和计算描述统计
# pandas对象拥有一组常用的数学和统计方法
# 它们大部分都属于约简和汇总统计，用于从Series中提取单个值，
# 或从DataFrame的行或列中提取一个Series
# 跟对应的numpy数组方法相比，它们都是基于没有缺失数据的假设构建的
# df = DataFrame([[1.4, np.nan], [7.1, -4.5],
#                 [np.nan, np.nan], [0.75, -1.3]],
#                index=['a', 'b', 'c', 'd'],
#                columns=['one', 'two'])
# print(df)
# 调用DataFrame的sum方法将会返回一个含有列小计的Series
# print(df.sum())
# 传入axis=1将会按行进行求和运算
# print(df.sum(axis=1))
# NA值会自动被排除，除非整个切片（这里指行或列）都是NA
# 通过skipna选项可以禁用该功能
# print(df.mean(axis=1, skipna=False))
# 约简方法的选项
# 约简方法的选项.png

# 有些方法（idxmin和idxmax）返回的是间接统计（比如达到最小值或
# 最大值的索引）
# print(df.idxmax())
# 另一些方法则是累计型的
# print(df.cumsum())
# 还有一种，既不是约简型也不是累计型
# describe就是一个例子，用于一次性产生多个汇总统计
# print(df.describe())
# 对于非数值型数据，describe会产生另外一种汇总统计
# obj = Series(['a', 'a', 'b', 'c'] * 4)
# print(obj.describe())

# 描述和汇总统计
# 描述和汇总统计_1.png
# 描述和汇总统计_2.png

# 相关系数与协方差
# 有些汇总统计（如相关系数和协方差）是通过参数对计算出来的
# 数据来自Yahoo!Finance的股票价格和成交量
# all_data = {}
# for ticker in ['AAPL', 'IBM', 'MSFT', 'GOOG']:
#     all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2000', '1/1/2010')

# price = DataFrame({tic: data['Adj Close'] for tic, data in all_data.iteritems()})
# volume = DataFrame({tic: data['volume'] for tic, data in all_data.iteritems()})
# 接下来计算价格的百分数变化
# returns = price.pct_change()
# print(returns.tail())

# Series的corr方法用于计算两个Series中重叠的、非NA的、
# 按索引对齐的值的相关系数
# 与此类似，cov用于计算协方差
# returns.MSFT.corr(returns.IBM)
# returns.MSFT.cov(returns.IBM)
# DataFrame的corr和cov方法将以DataFrame的形式返回完整的相关系数
# 或协方差矩阵
# returns.corr()
# returns.cov()
# 利用DataFrame的corrwith方法，你可以计算其列或行跟另一个Series
# 或DataFrame之间的相关系数。
# 传入一个Series将会返回一个相关系数值Series（针对各列进行计算）
# returns.corrwith(re\turn.IBM)
# 传入一个DataFrame则会计算按列名配对的相关系数
# 这里，计算百分比变化与成交量的相关系数
# returns.corrwith(volume)
# 传入axis=1即可按行进行计算
# 无论如何，在计算相关系数之前，所有的数据项都会按标签对齐

# 唯一值、值计数以及成员资格
# 还有一类方法可以从一维Series的值中抽取信息
# obj = Series(['c', 'a', 'd', 'a', 'a', 'b', 'b', 'c', 'c'])
# 第一个函数是unique，它可以得到Series中的唯一值数组
# uniques = obj.unique()
# print(uniques)
# 返回的唯一值是未排序的，如果需要的话，可以对结果再次进行排序
# print(np.sort(uniques))
# value_counts用于计算一个Series中各值出现的频率
# print(obj.value_counts())
# 为了方便查看，结果Series是按值频率降序排列的
# value_counts还是一个顶级的pandas方法，可用于任何数组或序列
# print(pd.value_counts(obj.values, sort=False))
# 最后是isin，用于判断矢量化集合的成员资格，可用于选取Series
# 或DataFrame列中数据的子集
# mask = obj.isin(['b', 'c'])
# print(mask)
# print(obj[mask])
# 唯一值、值计数、成员资格方法
# 唯一值-计数-成员资格.png
# 有时，你可能希望得到DataFrame中多个相关列的一张柱形图
data = DataFrame({'Qu1': [1, 3, 4, 3, 4],
	'Qu2': [2, 3, 1, 2, 3], 'Qu3': [1, 5, 2, 4, 4]})
print(data)
# 将pandas的value_counts传给该DataFrame的apply函数
print(data.apply(pd.value_counts).fillna(0))