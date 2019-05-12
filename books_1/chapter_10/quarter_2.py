import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse


# 时间序列基础
# pandas最基本的时间序列类型就是以时间戳为索引的Series
# dates = [datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7),
#          datetime(2011, 1, 8), datetime(2011, 1, 10), datetime(2011, 1, 12)]
# ts = Series(randn(6), index=dates)
# print(ts)
# 这些datetime对象实际上是被放在一个DatetimeIndex中的
# 变量ts就成为一个TimeSeries
# print(type(ts))
# print(ts.index)
# 注意：没必要显式使用TIMESeries的构造函数，当创建一个带有DatetimeIndex的Series
# 时，pandas就会知道该对象是一个时间序列
# 跟其他Series一样，不同索引的时间序列之间的算术运算会自动按日期对齐
# print(ts + ts[::2])
# pandas用Numpy的datetime64数据类型以纳秒形式存储时间戳
# print(ts.index.dtype)
# DatetimeIndex中的各个标量值是pandas的Timestamp对象
# stamp = ts.index[0]
# print(stamp)
# 只要有需要，TimeStamp可以随时自动转换为datetime对象，此外，还可以存储频率信息，
# 且知道如何执行时区转换以及其他操作


# 索引、选取、子集构造
# 由于TIMESeries是Series的一个子类，所以在索引以及数据选取方面它们的行为是一样的
# stamp = ts.index[2]
# print(ts[stamp])
# 还有一种更为方便的用法：传入一个可以被解释为日期的字符串
# print(ts['1/10/2011'])
# print(ts['20110110'])
# 对于较长的实践序列，只需传入“年”或“年月”即可轻松选取数据的切片
longer_ts = Series(randn(1000),
                   index=pd.date_range('1/1/2000', periods=1000))
# print(longer_ts)
# print(longer_ts['2001'])
# print(longer_ts['2001-05'])
# 通过日期进行切片的方式只对规则Series有效
# print(ts[datetime(2011, 1, 7)])
# 由于大部分时间序列数据都是按照时间先后排序的，因此你也可以用不存在于
# 该时间序列中的时间戳对其进行切片(即范围查询)
# print(ts)
# print(ts['1/6/2011':'1/11/2011'])
# 跟以前一样，这里可以传入字符串日期、datetime或Timestamp
# 注意，这样切片所产生的是源时间序列的视图，跟Numpy数组的
# 切片运算时一样的
# 此外，还有一个等价的实例方法也可以截取两个日期之间的TimeSeries
# print(ts.truncate(after='1/9/2011'))
# 上面操作对于DataFrame也有效
# dates = pd.date_range('1/1/2000', periods=100, freq='W-WED')
# long_df = DataFrame(randn(100, 4), index=dates,
# 	columns=['Colorado', 'Texas', 'New York', 'Ohio'])
# print(long_df.ix['5-2001'])


# 带有重复索引的时间序列
# 在某些应用场景中，可能存在多个观测数据落在同一个时间点上的情况
dates = pd.DatetimeIndex(['1/1/2000', '1/2/2000',
                          '1/2/2000', '1/2/2000', '1/3/2000'])
dup_ts = Series(np.arange(5), index=dates)
print(dup_ts)
# 通过检查索引的is_unique属性，可以知道它是不是唯一的
# print(dup_ts.index.unique())
# 对这个时间序列进行索引，要么产生标量值，要么产生切片，具体要看
# 所选的时间点是否重复
# 不重复
# print(dup_ts['1/3/2000'])
# 重复
# print(dup_ts['1/2/2000'])
# 假如你想要对具有非唯一时间戳的数据进行聚合
# 一个办法是使用groupby，并传入level=0(索引的唯一一层)
# grouped = dup_ts.groupby(level=0)
# print(grouped.mean())
# print(grouped.count())