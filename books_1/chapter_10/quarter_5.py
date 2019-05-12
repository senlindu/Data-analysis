import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from pandas.tseries.offsets import Hour, Minute, Day, MonthEnd


# 时期及其算术运算
# 时期表示的是时间区间，比如数日、数月、数季、数年等
# period类所表示的就是这种类型，其构造函数需要用到一个字符串或整数，以及表中的频率
# p = pd.Period(2007, freq='A-DEC')
# print(p)
# 这个period对象表示的是从2007年1月1日到2007年12月31日之间的整段时间
# 只需对Period对象加上或减去一个整数即可达到根据其频率进行位移的效果
# print(p + 5)
# print(p - 2)
# 如果两个Period对象拥有相同的频率，则他们的差就是它们之间的单位数量
# print(pd.Period('2014', freq='A-DEC') - p)
# period_range函数可用于创建规则的时期范围
# rng = pd.period_range('1/1/2000', '6/30/2000', freq='M')
# print(rng)
# PeriodIndex类保存了一组Period，可以在任何pandas数据结构中被用作轴索引
# print(Series(randn(6), index=rng))
# PeriodIndex类的构造函数还允许直接使用一组字符串
# value = ['2001Q3', '2002Q2', '20030Q1']
# index = pd.PeriodIndex(values, freq='Q-DEC')
# print(index)


# 时期的频率转换
# Period和PeriodIndex对象都可以通过其asfreq方法被转换成别的频率
# 假设我们有一个年度时期，希望将其转换为当年年初或年末的一个月度时期
# p = pd.Period('2007', freq='A-DEC')
# print(p.asfreq('M', how='start'))
# print(p.asfreq('M', how='end'))
# 你可以将Period('2007', 'A-DEC')看做一个被划分为多个月度时期的时间段中的游标
# p = pd.Period('2007', freq='A-JUN')
# print(p.asfreq('M', 'start')
# print(p.asfreq('M', 'end'))
# 在将高频率转换为低频率时，超时期是由子时期所属的位置决定的
# 例如，在A-JUN频率中，月份"2007年8月"实际上是属于周期"2008年"的
# p = pd.Period('2007-08', 'M')
# print(p.asfreq('A-JUN'))
# PeriodIndex或TimeSeries的频率转换也是如此
# rng = pd.period_range('2006', '2009', freq='A-DEC')
# ts = Series(randn(len(rng)), index=rng)
# print(ts)
# print(ts.asfreq('M', how='start'))
# print(ts.asfreq('M', how='end'))

# Period频率转换示例.png


# 按季度计算的时期频率
# 许多季度型数据都会涉及“财年末的概念，通常是一年12个月中某月的最后一个日历日或工作日
# 时期“2014Q4”根据财年末的不同会有不同的含义
# pandas支持12种可能的季度型频率，即Q-JAN到Q-DEC
# p = pd.Period('2014Q4', freq='Q-JAN')
# print(p)
# 在以1月结束的财年中，2012Q4是从11月到1月(将其转换为日型频率就明白了)
# print(p.asfreq('D', 'start'))
# print(p.asfreq('D', 'end'))
# 因此，Period之间的算术运算会非常简单
# 要获取该季度倒数第二个工作日下午4点的时间戳
# p4pm = (p.asfreq('B', 'e') - 1).asfreq('T', 's') + 16 * 60
# print(p4pm)
# print(p4pm.to_timestamp())


# 不同季度型频率之间的转换.png

# period_range还可用于生成季度型范围
# 季度型范围的算术运算也跟上面是一样的
# rng = pd.period_range('2011Q3', '2012Q4', freq='Q-JAN')
# ts = Series(np.arange(len(rng)), index=rng)
# print(ts)
# new_rng = (rng.asfreq('B', 'e') - 1).asfreq('T', 's') + 16 * 60
# ts.index = new_rng.to_timestamp()
# print(ts)


# 将Timestamp转换为Period(及其反向过程)
# 通过使用to_period方法，可以将由时间戳索引的Series和DataFrame对象转换为以时期索引
# rng = pd.date_range('1/1/2000', periods=3, freq='M')
# ts = Series(randn(3), index=rng)
# pts = ts.to_period()
# print(ts)
# print(pts)
# 由于时期指的是非重叠时间区间，因此对于给定的频率，一个时间戳只能属于一个时期
# 新PeriodIndex的频率默认是从时间戳推断而来的，也可以指定任何别的频率
# 结果中允许存在重复时期
# rng = pd.date_range('1/29/2000', periods=6, freq='D')
# ts2 = Series(randn(6), index=rng)
# print(ts2.to_period('M'))
# 要转换为时间戳，使用to_timestamp即可
# pts = ts.to_period()
# print(pts)
# print(pts.to_timestamp(how='end'))


# 通过数组创建PeriodIndex
# 固定频率的数据集通常会将时间信息分开存放在多个列中
# 下面这个宏观经济数据集中，年度和季度就分别存放在不同的列中
# data = pd.read_csv('e:/examples/macrodata.csv')
# print(data.year)
# print(data.quarter)
# 将这两个数组以及一个频率传入PeriodIndex，就可以将它们合并成DataFrame的一个索引
# index = pd.PeriodIndex(year=data.yaer, quarter=data.quarter, freq='Q-DEC')
# print(index)
# data.index = index
# print(data.infl)
# 