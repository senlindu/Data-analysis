import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand, permutation, randint
from datetime import datetime, timedelta, time
from dateutil.parser import parse
from pandas.tseries.offsets import Hour, Minute, Day, MonthEnd
import matplotlib.pyplot as plt
import pandas.io.data as web
import random
import random.seed(0)
import string


# 金融和经济数据应用
# 使用"截面"表示某个时间点的数据
# 多个数据项在多个时间点的截面数据就构成了一个面板
# 面板数据既可以被表示为层次化索引的DataFrame，也可以被表示为三维的Panel pandas对象


# 数据规整化方面的话题

# 时间序列以及截面对齐
# 两个相关的时间序列的索引可能没有很好的对齐，或两个DataFrame对象可能含有不匹配的列或行
# pandas可以在算术运算中自动对齐数据
# 下面两个DataFrame，分别含有股票价格和成交量的时间序列
# print(prices)
# print(volume)
# 假设你想要用所有有效数据计算一个成交量加权平均价格
# 由于pandas会在算术运算过程中自动将数据对齐，并在sum这样的函数中排除缺失数据
# print(prices * volume)
# vwap = (prices * volume).sum() / volume.sum()
# print(vwap)
# print(vwap.dropna())
# 由于SPX在volume中找不到，所以你随时可以显式地将其丢弃
# 如果希望手工对齐，可以使用DataFrame的align方法，返回一个元组，含有两个对象的重索引版本
# print(prices.align(volume, join='inner'))
# 另一个不可或缺的功能是，通过一组索引可能不同的Series构建一个DataFrame
# s1 = Series(range(3), index=['a', 'b', 'c'])
# s2 = Series(range(4), index=['d', 'b', 'c', 'e'])
# s3 = Series(range(3), index=['f', 'a', 'c'])
# print(DataFrame({'one':s1, 'two':s2, 'three':s3}))
# 跟前面一样，这里也可以显式定义结果的索引(丢弃其余的数据)
# print(DataFrame({'one':s1, 'two':s2, 'three':s3}, index=list('face')))


# 频率不同的时间序列的运算
# 经济学时间序列常常有着按年、季、月、日计算的或其他更特殊的频率
# 频率转换和重对齐的两大主要工具是resample和reindex方法
# resample用于即使那个数据转换到固定频率，而reindex则用于使数据符合一个新索引
# 它们都支持插值(如前向填充)逻辑
ts1 = Series(randn(3),
             index=pd.date_range('2012-6-13', periods=3, freq='W-WED'))
print(ts1)
# 如果将其重采样到工作日(星期一到星期五)频率，则那些没有数据的日子就会出现一个空洞
# print(ts1.resample('B'))
# 当然，只需将fill_method设置为'ffill'即可用前面的值填充这些空白
# 处理较低频率的数据时常常这么干，因为最终结果中各时间点都有一个最新的有效值
# print(ts1.resample('B', fill_method='ffill'))
# 在实际工作中，将较低频率的数据升采样到较高的规整频率是一种不错的解决方案，但是
# 对于更一般化的不规整时间序列可能就不太合适了
dates = pd.DatetimeIndex(['2012-6-12', '2012-6-17', '2012-6-18',
                          '2012-6-21', '2012-6-22', '2012-6-29'])
ts2 = Series(randn(6), index=dates)
print(ts2)
# 如果要将ts1中最当前值(即前向填充)加到ts2上
# 一个办法是将两者重采样为规整频率后再相加，但是如果想维持ts2中的日期索引，则reindex
# 会是一种更好的解决方案
# print(ts1.reindex(ts2.index, method='ffill'))
# print(ts2 + ts1.reindex(ts2.index, method='ffill'))


# 使用Period
# Period(表示时间区间)提供了另一种处理不同频率时间序列的办法，尤其是那些有着特殊规范
# 的以年或季度为频率的金融或经济序列
# 比如，一个公司可能会发布其以6月结尾的财年的每季度盈利报告，即频率为Q-JUN
# gdp = Series([1.78, 1.94, 2.08, 2.01, 2.15, 2.31, 2.46],
#        index=pd.period_range('1984Q2', periods=7, freq='Q-SEP'))
# infl = Series([0.025, 0.045, 0.037, 0.04],
#        index=pd.period_range('1982', periods=4, freq='A-DEC'))
# print(gdp)
# print(infl)
# 跟Timestamp的时间序列不同，由Period索引的两个不同频率的时间序列之间的运算必须进行
# 显式转换。
# 假设已知infl值是在每年年末观测的，可以将其转换到Q-SEP以得到该频率下的正确时期
# infl_q = infl.asfreq('Q-SEP', how='end')
# print(infl_q)
# 然后这个时间序列就可以被重索引了(使用前向填充以匹配gdp)
# print(infl_q.reindex(gdp.index, method='ffill'))


# 时间和"最当前"数据选取
# 假设你有一个很长的盘中市场数据时间序列，现在希望抽取其中每天特定时间的价格数据
# 如果数据不规整(观测值没有精确地落在期望的时间点上)，该怎么办？
# 如果不够小心仔细的话，很容易导致错误的数据规整化
# 生成一个交易日内的日期范围和时间序列
# rng = pd.date_range('2012-06-01 09:30', '2012-06-01 15:59', freq='T')
# 生成5天的时间点(9:30-15:59之间的值)
# rng = rng.append([rng + pd.offsets.BDay(i) for i in range(1, 4)])
# ts = Series(np.arange(len(rng), dtype=float), index=rng)
# print(ts)
# 利用Python的datetime.time对象进行索引即可抽取出这些时间点上的值
# print(ts[time(10, 0)])
# 实际上，该操作用到了实例方法at_time(各时间序列以及类似的DataFrame对象都有）
# print(ts.at_time(time(10, 0))
# 还有一个between_time方法，用于选取两个Time对象之间的值
# print(ts.between_time(time(10, 0), time(10, 1)))
# 可能刚好就没有任何数据落在某个具体的时间上(比如上午10点)
# 你可能希望得到上午10点之前最后出现的那个值
# 将该时间序列的大部分内容随机设置为NA
# indexer = np.sort(permutation(len(ts))[700:])
# irr_ts = ts.copy()
# irr_ts[indexer] = np.nan
# print(irr_ts['2012-06-01 09:50':'2012-06-01 10:00'])
# 如果将一组Timestamp传入asof方法，就能得到这些时间点处(或其之前最近)的有效值(非NA)
# 我们构造一个日期范围(每天上午10点)，然后将其传入asof
# selection = pd.date_range('2012-06-01 10:00', periods=4, freq='B')
# print(irr_ts.asof(selection))


# 拼接多个数据源
# 在金融或经济领域中，还有另外几个经常出现的情况
# 1、在一个特定的时间点上，从一个数据源切换到另一个数据源
# 2、用另一个时间序列对当前时间序列中的缺失值"打补丁"
# 3、将数据中的符号(国家、资产代码等)替换为实际数据
# 对于第一种情况，在特定时刻从一个时间序列切换到另一个，其实就是用pandas.concat
# 将两个TimeSeries或DataFrame对象合并到一起
# data1 = DataFrame(np.ones((6, 3), dtype=float),
#         columns=['a', 'b', 'c'],
#         index=pd.date_range('6/12/2012', periods=6))
# data2 = DataFrame(np.ones((6, 3), dtype=float) * 2,
#         columns=['a', 'b', 'c'],
#         index=pd.date_range('6/13/2012', periods=6))
# spliced = pd.concat([data1.ix[:'2012-06-14'], data2.ix['2012-06-15':]])
# print(spliced)
# 假设data1缺失了data2中存在的某个时间序列
# data2 = DataFrame(np.ones((6, 4), dtype=float) * 2,
#          columns=['a', 'b', 'c', 'd'],
#          index=pd.date_range('6/13/2012', periods=6))
# spliced = pd.concat([data1.ix[:'2012-06-14'], data2.ix['2012-06-15':]])
# print(spliced)
# combine_first可以引入合并点之前的数据，这样也就扩展了'd'项的历史
# spliced_filled = spliced.combine_first(data2)
# print(spliced_filled)
# 由于data2没有关于2012-06-12的数据，所以也就没有值被填充到那一天
# DataFrame也有一个类似的update，它可以实现就地更新
# 如果只想填充空洞，则必须传入overwrite=False才行
# spliced.update(data2, overwrite=False)
# print(spliced)
# 上面所讲的这些技术都可实现将数据中的符号替换为实际数据，但有时利用DataFrame的
# 索引机制直接对列进行设置会更简单一些
# cp_spliced = spliced.copy()
# cp_spliced[['a', 'c']] = data1[['a', 'c']]
# print(cp_spliced)


# 收益指数和累计收益
# 在金融领域，收益通常指的是某资产价格的百分比变化
# 下面是2011年到2012年间苹果公司的股票价格数据
# price = web.get_data_yahoo('AAPL', '2011-01-01')['Adj Close']
# print(price[-5:])
# 对于苹果公司的股票，计算两个时间点之间的累计百分比回报只需计算价格的百分比变化即可
# print(price['2011-10-03'] / price['2011-3-01' -1]
# 利用cumprod计算出一个简单的收益指数
# returns = price.pct_change()
# ret_index = (1 + returns).cumprod()
# ret_index[0] = 1
# print(ret_index)
# 得到收益指数之后，计算指定日期内的累计收益就很简单了
# m_returns = ret_index.resample('BM', how='last').pct_change()
# print(m_returns['2012'])
# m_rets = (1 + returns).resample('M', how='prod', kind='period') - 1
# print(m_rets['2012'])
# 如果知道了股息的派发日和支付率，就可以将它们计入到每日总收益中
# returns[dividend_dates] += dividend_pcts
