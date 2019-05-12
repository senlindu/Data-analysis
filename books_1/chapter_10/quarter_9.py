import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from pandas.tseries.offsets import Hour, Minute, Day, MonthEnd
import matplotlib.pyplot as plt


# 性能和内存使用方面的注意事项
# Timestamp和Period都是以64位整数表示的
# 对于每个数据点，其时间戳需要占用8字节的内存
# 含有一百万个float64数据点的时间序列需要占用大约16MB的空间
# 由于pandas会尽量在多个时间序列之间共享索引，所以创建现有时间序列的视图不会占有更多内存
# 低频率索引会存放在一个中心缓存中，所以任何固定频率的索引都是该日期缓存的视图
# 如果你有一个很大的低频率时间序列，索引所占用的内存空间将不会很大

# 性能方面，pandas对数据对齐和重采样运算进行了高度优化
# 例如，将一亿个数据点聚合为OHLC
# rng = pd.date_range('1/1/2000', periods=10000000, freq='10ms')
# ts = Series(randn(len(rng)), index=rng)
# print(ts)
# print(ts.resample('15min', how='ohlc'))
# %timeit print(ts.resample('15min', how='ohlc'))
# 运行时间跟聚合结果的相对大小有一定关系，越高频率的聚合所耗费的时间越多
# rng = pd.date_range('1/1/2000', periods=10000000, freq='1s')
# ts = Series(randn(len(rng)), index=rng)
# print(ts)
# %timeit print(ts.resample('15s', how='ohlc'))
# 