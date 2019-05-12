import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from pandas.tseries.offsets import Hour, Minute, Day, MonthEnd


# 重采样及频率转换
# 重采样指的是将时间序列从一个频率转换到另一个频率的处理过程
# 高频率数据聚合到低频率成为降采样，而将低频率数据转换为高频率数据则称为升采样
# 并不是所有的重采样都能被划分到这两个大类中
# 将W-WED转换为W-FRI既不是降采样也不是升采样

# pandas对象都带有一个resample方法，是各种频率转换工作的主力函数
# rng = pd.date_range('1/1/2000', periods=100, freq='D')
# ts = Series(randn(len(rng)), index=rng)
# print(ts.resample('M', how='mean'))
# print(ts.resample('M', how='mean', kind='period'))
# resample是一个灵活高效的方法，可用于处理非常大的时间序列


# resample方法的参数
# resample方法参数_1.png
# resample方法参数_2.png


# 降采样
# 将数据聚合到规整的低频率是一件非常普通的时间序列处理任务
# 待聚合的数据不必拥有固定的频率，期望的频率会自动定义聚合的面元边界，这些
# 面元用于将时间序列拆分为多个片段
# 例如，要转换到月度频率，数据需要被划分到多个单月时间段中
# 各时间段都是半开放的，一个数据点只能属于一个时间段，所有时间段的并集必须
# 能组成整个时间帧
# 在用resample对数据进行降采样时，需要考虑两样东西
# 1、各区间哪边是闭合的
# 2、如何标记各个聚合面元，用区间的开头还是末尾
# 首先，看一些"1分钟"数据
# rng = pd.date_range('1/1/2000', periods=12, freq='T')
# ts = Series(np.arange(12), index=rng)
# print(ts)
# 假设你想要通过求和的方式将这些数据聚合到"5分钟"块中
# print(ts.resample('5min', how='sum'))
# 传入的频率会以"5分钟"的增量定义面元边界
# 默认情况下，面元的右边界是包含的，因此00:00到00:05的区间中时包含00：05的
# 传入closed='left'会让区间以左边界闭合
# print(ts.resample('5min', how='sum', closed='left'))
# 最终的时间序列是以各面元右边界的时间戳进行标记的
# 传入label='left'即可用面元的左边界对其进行标记
# print(ts.resample('5min', how='sum', closed='left', label='left'))

# 重采样演示.png

# 你可能希望对结果索引做一些唯一，比如从右边界减去一秒以便更容易明白该时间戳
# 到底表示的是哪个区间
# 只需通过loffset设置一个字符串或日期偏移量即可实现这个目的
# print(ts.resample('5min', how='sum', loffset='-1s'))
# 也可以调用结果对象的shift方法来实现这个目的


# OHLC重采样
# 金融领域中有一种无所不在的时间序列聚合方式，即计算各面元的四个值
# 1、开盘
# 2、收盘
# 3、最大值
# 4、最小值
# 传入how='ohlc'即可得到一个含有这四种聚合值的DataFrame
# print(ts.resample('5min', how='ohlc'))


# 通过groupby进行重采样
# 另一种降采样的办法是使用pandas的groupby功能
# 例如，根据月份或星期几进行分组，只需传入一个能够访问时间序列的索引上的这些字段的函数即可
# rng = pd.date_range('1/1/2000', periods=100, freq='D')
# ts = Series(np.arange(100), index=rng)
# print(ts.groupby(lambda x:x.month).mean())
# print(ts.groupby(lambda x:x.weekday).mean())


# 升采样和插值
# 在将数据从低频率转换到高频率时，就不需要聚合了
# frame = DataFrame(randn(2, 4), 
#                 index = pd.date_range('1/1/2000', periods=2, freq='W-WED'),
#                 columns=['Colorado', 'Texas', 'New York', 'Ohio'])
# print(frame[:5])
# 将其重采样到日频率，默认会引入缺失值
# df_daily = frame.resample('D')
# print(df_daily)
# 假如你想要用前面的周型值填充"非星期三"
# resampling的填充和插值方式跟fillna和reindex的一样
# print(frame.resample('D', fill_method='ffill'))
# 同样，这里你也可以只填充指定的时期数(目的是限制前面的观测值的持续使用距离)
# print(frame.resample('D', fill_method='ffill', limit=2))
# 注意，新的日期索引完全没必要要跟旧的相交
# print(frame.resample('W-THU', fill_method='ffill'))


# 通过时期进行重采样
# 对那些使用时期索引的数据进行重采样是件非常简单的事情
# frame = DataFrame(randn(24, 4),
#            index=pd.period_range('1-2000', '12-2001', freq='M'),
#            columns=['Colorado', 'Texas', 'New York', 'Ohio'])
# print(frame[:5])
# annual_frame = frame.resample('A-DEC', how='mean')
# print(annual_frame)
# 升采样要稍微麻烦一些，因为你必须决定在新频率中各区间的哪端用于放置原来的值，
# 就像asfreq方法那样
# convention参数默认为'end',可设置为'start'
# Q-DEC：季度型(每年以12月结束)
# printt(annual_frame.resample('Q-DEC', fill_method='ffill'))
# print(annual_frame.resample('Q-DEC', fill_method='ffill', 
#       convention='start'))
# 由于时期指的是时间区间，所以升采样和降采样的规则就比较严格
# 1、在降采样中，目标频率必须是源频率的子时期
# 2、在升采样中，目标频率必须是源频率的超时期
# 如果不满足这些条件，就会引发异常
# 这主要影响的是按季、年、周计算的频率
# 例如，由Q-MAR定义的时间区间只能升采样为A-MAR、A-JUN、A-SEP、A-DEC等
# print(annual_frame.resample('Q-MAR', fill_method='ffill'))
# 