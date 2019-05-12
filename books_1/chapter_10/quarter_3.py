import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from pandas.tseries.offsets import Hour, Minute, Day, MonthEnd


# 日期的范围、频率以及移动
# pandas的时间序列一般被认为是不规则的，没有固定的频率
# 常常需要以某种相对固定的频率进行分析，这样会在时间序列中引入缺失值
# pandas有一整套标准时间序列频率以及用于重采样、频率推断、生成固定频率日期范围的工具
# 将时间序列转换为一个具有固定频率的时间序列，调用resample即可
# dates = [datetime(2011, 1, 2), datetime(2011, 1, 5), datetime(2011, 1, 7),
#          datetime(2011, 1, 8), datetime(2011, 1, 10), datetime(2011, 1, 12)]
# ts = Series(randn(6), index=dates)
# print(ts)
# print(ts.resample(D))
# 频率的转换（或重采样）是一个比较大的主题
# 如何使用基本的频率


# 生成日期范围
# pandas.date_range可用于生成指定长度的DatetimeIndex
# index = pd.date_range('4/1/2012', '6/1/2012')
# print(index)
# 默认，date_range会产生按天计算的时间点
# 如果只传入起始或结束日期，还得传入一个表示一段时间的数字
# print(pd.date_range(start='4/1/2012', periods=20))
# print(pd.date_range(end='6/1/2012', periods=20))
# 起始和结束日期定义了日期索引的严格边界
# 生成一个由每月最后一个工作日组成的日期索引，传入BM频率，
# 这样就只会包含时间间隔内(或刚好在边界上)符合频率要求的日期
# print(pd.date_range('1/1/2000', '12/1/2000', freq='BM'))
# date_range默认会保留起始和结束时间戳的时间信息
# print(pd.date_range('5/2/2012 12:56:31', periods=5))
# 有时，虽然起始和结束日期带有时间信息，但你希望产生一组被规范化
# 到午夜的时间戳。normalize选项即可实现该功能
# print(pd.date_range('5/2/2012 12:56:31', periods=5, normalize=True))


# 频率和日期偏移量
# pandas中的频率是由一个基础频率和一个乘数组成的
# 基础频率通常以一个字符串别名表示，比如"M"表示每月，"H"表示每小时
# 对于每个基础频率，都有一个被称为日期偏移量的对象与之对应
# hour = Hour()
# print(hour)
# 传入一个整数即可定义偏移量的倍数
# four_hours = Hour(4)
# print(four_hours)
# 一般来说，无需显式创建这样的对象，只需使用诸如"H"或"4H"这样的字符串别名
# 即可。在基础频率前面放上一个整数即可创建倍数
# print(pd.date_range('1/1/2000', '1/3/2000 23:59', freq='4h'))
# 大部分偏移量对象都可以通过加法进行连接
# print(Hour(2) + Minute(30))
# 也可以传入频率字符串(如"2h30min")，这种字符串可以被高效地解析为
# 等效的表达式
# print(pd.date_range('1/1/2000', periods=10, freq='1h30min'))
# 有些频率描述的时间点并不是均匀分隔的
# 例如'M'和'BM'就取决于每月的天数，后者还要考虑月末是不是周末
# 由于没有更好的术语，将这些称为锚点偏移量

# 频率代码和日期偏移量类
# 基础频率_1.png
# 基础频率_2.png


# WOM日期
# WOM是一种非常实用的频率类，以WOM开头，使你能获得诸如
# "每月第3个星期五"之类的日期
# rng = pd.date_range('1/1/2012', '9/1/2012', freq='WOM-3FRI')
# print(list(rng))


# 移动(超前和滞后)数据
# 移动指的是沿着时间轴将数据前移或后移
# Series和DataFrame都有一个shift方法用于执行单纯的前移或后移操作，保持索引不变
# ts = Series(randn(4), index=pd.date_range('1/1/2000', periods=4, freq='M'))
# print(ts)
# print(ts.shift(2))
# print(ts.shift(-2))
# shift通常用于计算一个时间序列或多个时间序列中的百分比变化
# ts / ts/shift(1) -1
# 由于单纯的移位操作不会修改索引，所以部分数据会被丢弃
# 如果频率已知，则可以将其传给shift以便实现对时间戳进行位移而不是对数据进行简单位移
# print(ts.shift(2, freq='M'))
# 还可以使用其他频率，你能非常灵活地对数据进行超前和滞后处理
# print(ts.shift(3, freq='D'))
# print(ts.shift(1, freq='3D'))
# print(ts.shift(1, freq='90T'))


# 通过偏移量对日期进行位移
# pandas的日期偏移量还可以用在datetime或Timestamp对象上
# now = datetime(2011, 11, 17)
# print(now + 3 * Day())
# 如果加的是锚点偏移量，第一次增量会将原日期向前滚动到符合频率规则的下一个日期
# print(now + MonthEnd())
# print(now + MonthEnd(2))
# 通过锚点偏移量的rollforward和rollback方法，可显式地将日期向前或向后"滚动"
# offset = MonthEnd()
# print(offset.rollforward(now))
# print(offset.rollback(now))
# 日期偏移量还有一个巧妙的用法，即结合groupby使用这两个滚动方法
# ts = Series(randn(20), index=pd.date_range('1/15/2000', periods=20, freq='4d'))
# print(ts.groupby(offset.rollforward).mean())
# 当然，更简单更快速地实现该功能的办法是使用resample
# print(ts.resample('M', how='mean'))