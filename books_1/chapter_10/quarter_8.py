import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from pandas.tseries.offsets import Hour, Minute, Day, MonthEnd
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore


# 移动窗口函数
# 在移动窗口(可以带有指数衰减权数)上计算的各种统计函数也是一类常见于时间序列的数组变换
# 称它们为移动窗口函数，其中还包括哪些窗口不定长的函数(如指数加权移动平均)
# 跟其他统计函数一样，移动窗口函数也会自动排除缺失值
# rolling_mean是其中最简单的一个
# 接受一个TimeSeries或DataFrame以及一个window(表示期数)
close_px_all = pd.read_csv('e:/examples/stock_px.csv', parse_dates=True,
                           index_col=0)
close_px = close_px_all[['AAPL', 'MSFT', 'XOM']]
# close_px.AAPL.plot()
# rolling_mean更新为df.rolling(window)
# close_px.AAPL.rolling(250).mean().plot()
# plt.show()
# 默认情况下，诸如rolling这样的函数需要指定数量的非NA观测值
# 可以修改该行为以解决缺失数据的问题
# 在时间序列开始处尚不足窗口期的那些数据就是个特例
# appl_std250 = close_px.AAPL.rolling(250, min_periods=10).std()
# print(appl_std250[5:12])
# appl_std250.plot()
# 要计算扩展窗口平均，你可以将扩展窗口看做一个特殊的窗口，其长度与时间序列一样，但
# 只需一期(或多期)即可计算一个值
# expanding_mean = lambda x: x.rolling(len(x), min_periods=1).mean()
# 对DataFrame调用rolling函数会转换应用到所有的列上
# close_px.rolling(60).mean().plot(logy=True)


# 移动窗口和指数加权函数
# 注意：pd.rolling_ 已经更新为df.rolling().mean()
# 移动窗口和指数加权函数.png


# 指数加权函数
# 另一种使用固定大小窗口及相等权数观测值的办法是，定义一个衰减因子常量，以便使
# 近期的观测值拥有更大的权数
# 用数学术语讲，如果mat是时间t的移动平均结果，x是时间序列，结果中的各个值可用
# mat = a * ma(t-1) + (a-1) * x(-t)进行计算，其中a是衰减因子
# 衰减因子的定义方式有很多，比较流行的是使用时间间隔，它可以使结果兼容与窗口大小等于
# 时间间隔的简单移动窗口函数

# 由于指数加权统计会赋予近期的观测值更大的权数，因此相对于等权统计，能适应更快的变化
# 例如，对比苹果公司股价的60日移动平均和span=60的指数加权移动平均
# fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=True, figsize=(12, 7))
# aapl_px = close_px.AAPL['2005':'2009']
# ma60 = aapl_px.rolling(60, min_periods=50).mean()
# ewmX更新为ewm().X()
# ewma60 = aapl_px.ewm(span=60).mean()
# aapl_px.plot(style='k-', ax=axes[0])
# ma60.plot(style='k--', ax=axes[0])
# aapl_px.plot(style='k-', ax=axes[1])
# ewma60.plot(style='k--', ax=axes[1])
# axes[0].set_title('Simple MA')
# axes[1].set_title('Exponentially-weighted MA')
# plt.show()


# 二元移动窗口函数
# 有些统计运算(如相关系数和协方差)需要在两个时间序列上执行
# 例如，金融分析师常常对某只股票对某个参考指数的相关系数感兴趣
# 我们可以通过计算百分比变化并使用rolling_corr的方式得到该结果
spx_px = close_px_all['SPX']
spx_rets = spx_px / spx_px.shift(1) - 1
returns = close_px.pct_change()
# corr = returns.AAPL.rolling(125, min_periods=100).corr(spx_rets)
# corr.plot()
# plt.show()
# 假设你想要一次性计算多只股票与标准普尔500指数的相关系数
# 传入一个TimeSeries和一个DataFrame，rolling_corr就会自动计算TimeSeries与DataFrame
# 各列的相关系数
# corr = returns.rolling(125, min_periods=100).corr(spx_rets)
# corr.plot()
# plt.show()


# 用户定义的移动窗口函数
# rolling_apply函数使你能够在移动窗口上应用自己设计的数组函数
# 唯一的要求就是，该函数能从数组的各个片段中产生单个值
# 当我们使用rolling_quantile计算样本分位数时，可能对样本中特定值的百分等级感兴趣
# scipy.stats.percentileofscore函数就能达到这个目的
def score_at_2percent(x): return percentileofscore(x, 0.02)


result = returns.AAPL.rolling(250).apply(score_at_2percent, raw=True)
result.plot()
plt.show()
