import numpy as np
import pandas as pd 
from pandas import DataFrame, Series
from pandas_datareader import data as web

# 其他有关pandas的话题

# 整数索引
# 操作由整数索引的pandas对象常常会让新手抓狂，因为它们跟内置的Python
# 数据结构在索引语义上有些不同
# 例如，下面的代码你可能认为不会产生一个错误
# ser = Series(np.arange(3.))
# ser[-1]
# 在这种情况下，虽然pandas会求助于整数索引，但没有哪种办法
# 能够既不引入任何bug又安全有效地解决该问题
# 我们含有0、1、2的索引，但很难推断出用户想要什么（基于标签或位置的索引）
# ser
# 相反，对于一个非整数索引，就没有这样的歧义
# ser2 = Series(np.arange(3.), index=['a', 'b', 'c'])
# ser2[-1]
# 为了保持良好的一致性，如果你的轴索引含有索引器，根据整数进行数据选取
# 的操作将总是面向标签的。这也包括用ix进行切片
# ser.ix[:1]
# 如果你需可靠的、不考虑索引类型的、基于位置的索引，可以使用
# Series的iget_value方法和DataFrame的irow和icol方法
# ser3 = Series(range(3), index=[-5, 1, 3])
# print(ser3.iget_value(2))
# frame = DataFrame(np.arange(6).reshape(3, 2), index=[2, 0, 1])
# print(frame.irow(0))


# 面板数据
# pandas有一个panel数据结构，可以将其看做一个三维板的DataFrame
# pandas的大部分开发工作都集中在表格型数据的操作上，因为这些数据
# 更常见，而且层次化索引也使得多数情况下没必要使用真正的N维数组

# 你可以用个由DataFrame对象组成的字典或一个三维ndarray创建panel对象
# pdata = pd.Panel(dict((stk, web.get_data_yahoo(stk, '1/1/2009',
	# '6/1/2012')) for stk in ['AAPL', 'GOOG', 'MSFT', 'DELL']))
# Panel中的每一项（类似于DataFrame的列）都是一个DataFrame
# print(pdata)
# pdata = pdata.swapaxes('items', 'minor')
# print(pdata['Adj Close'])
# 基于ix的标签索引被推广到三个维度，因此我们可以选取指定日期或日期
# 范围的所有数据
# print(pdata.ix[:, '6/1/2012', :])
# print(pdata.ix['Adj Close', '5/22/2012':, :])
# 另一个用于呈现面板数据（尤其是对拟合统计模型）的办法是“堆积式的”DataFrame
# stacked = pdata.ix[:, '5/30/2012':, :].to_frame()
# print(stacked)
# DataFrame有一个相应的to_panel方法，是to_frame的逆运算
# print(stacked.to_panel())