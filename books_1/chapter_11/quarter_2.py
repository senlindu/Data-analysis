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

# 分组变换和分析
# N = 1000


def rands(N):
    choices = string.ascii_uppercase
    return ''.join([random.choice(choices) for _ in xrange(n)])


tickers = np.array([rands(5) for _ in xrange(N)])
# 然后创建一个含有3列的DataFrame来承载这些假想数据，不过只选择部分股票组成该投资组合
# M = 500
# df = DataFrame({'Momentum' : randn(M) / 200 + 0.03,
#                'Value' : randn(M) / 200 +0.08,
#                'ShortInterst' : randn(M) / 200 - 0.02},
#                index=tickers[:M])
# 接下来，我们为这些股票随机创建一个行业分类
# 我只选用了两个行业，并将映射关系保存在Series中
# ind_names = np.array(['FINANCIAL', 'TECH'])
# sampler = randint(0, len(ind_names), N)
# industries = Series(ind_names[sampler], index=tickers,
#              name='industry')
# 现在，我们就可以根据行业分类进行分组并执行分组聚合和变换了
# by_industry = df.groupby(industries)
# print(by_industry.mean())
# print(by_industry.decribe())
# 要对这些按行业分组的投资组合进行各种变换，可以编写自定义的变换函数
# 例如行业内标准化处理，广泛用于股票资产投资组合的构建过程
# 行业内标准化处理


def zscore(group):
    return (group - group.mean()) / group.std()


df_stand = by_industry.apply(zscore)
# 这里处理之后，各行业的平均值为0， 标准差为1
# print(df_stand.groupby(industried).agg(['mean', 'std'])
# 内置变换函数(如rank)的用法会更简洁一些
# 行业内降序排名
# ind_rank = by_industry.rank(ascending=False)
# print(ind_rank.groupby(industries).agg(['min', 'max']))
# 在股票投资组合的定量分析中，"排名和标准化"是一种很常见的变换运算组合
# 通过将rank和zscore链接在一起即可完成整个变换过程
# 行业内排名和标准化
# print(by_industry.apply(lambda x: zscore(x.rank())))


# 分组因子暴露
# 因子分析是投资组合定量管理中的一种技术
# 投资组合的持有量和性能(收益与损失)可以被分解为一个或多个表示投资组合权重的因子(
# 风险因子就是其中之一)
# 例如，某只股票的价格与某个基准的协动性被称作其贝塔风险系数(beta，一种常见的风险因子)
# 以一个人为构成的投资组合为例进行讲解，它由三个随机生成的因子(通常称为因子载荷)和一些权重构成
# fac1, fac2, fac3 = rand(3, 1000)
# ticker_subset = tickers.take(permutation(N)[:1000])
# 因子加权和以及噪声
# port = Series(0.7 * fac1 - 1.2 * fac2 + 0.3 * fac3 + rand(1000),
#           index=ticker_subset)
# factors = DataFrame({'f1':fac1, 'f2':fac2, 'f3':fac3},
#          index=ticker_subset)
# 各因子与投资组合之间的矢量相关性可能说明不了什么问题
# print(factors.corrwith(port))
# 计算因子暴露的标准方式是最小二乘回归
# 使用pandas.ols即可计算出整个投资组合的暴露
# print(pd.ols(y=port, x=factors).beta)
# 由于没有给投资组合添加过多的随机噪声，所以原始的因子权重基本上可算是恢复出来了
# 还可以通过groupby计算各行业的暴露量，为了达到这个目的，编写了一个函数
def beta_exposure(chunk, factors=None):
    return pd.ols(y=chunk, x=factors).beta
# 然后根据行业进行分组，并应用该函数，传入因子载荷的DataFrame
# by_ind = port.groupby(industries)
# exposures = by_ind.apply(beta_exposure, factors=factors)
# print(exposure.unstack())


# 十分位和四分位分析
# 基于样本分位数的分析是金融分析师们的另一个重要工具
# 例如，股票投资组合的性能可以根据各股的市盈率被划分入四分位(四个大小相等的块)
# 通过pandas.qcut和groupby可以非常轻松地实现分位数分析
# 利用跟随策略或动量交易策略通过SPY交易所交易基金买卖标准普尔500指数
# data = web.get_data_yahoo('SPY', '2006-01-01')
# print(data)
# 计算日收益率，编写一个用于将收益率变换为趋势信号(通过滞后移动形成)的函数
# px = data['Adj Close']
# returns = px.pct_change()
def to_index(rets):
    index = (1 + rets).cumprod()
    first_loc = max(index.notnull().argmax() - 1, 0)
    index_valules[first_loc] = 1
    return index


def trend_signal(rets, lookback, lag):
    signal = rets.rolling(lookback, min_periods=lookback - 5).sum()
    return signal.shift(lag)
# 通过该函数，可以创建和测试一种根据每周五动量信号进行交易的交易策略
# signal = trend_signal(returns, 100, 3)
# trade_friday = signal.resample()'W-FRI'.resample('B', fill_method='ffill')
# trade_rets = trade_friday.shift(1) * returns
# 然后将该策略的收益率转换为一个收益指数，并绘制一张图表
# to_index(trade_rets).plot()
# plt.show()
# 假如你希望将该策略的性能按不同大小的交易期波幅进行划分
# 年度标准差是计算波幅的一种简单办法，我们可以通过计算夏普比率来
# 观察不同波动机制下的风险收益率
# vol = returns.rolling(250, min_periods=200) * np.sqrt(250)


def sharpe(rets, ann=250):
    return rets.mean() / rets.std() * np.sqrt(ann)

# 现在，利用qcut将vol划分为四等份，并用sharpen进行聚合
# print(trade_rets.groupby(pd.qcut(vol, 4)).agg(sharpe))
# 该策略在波幅最高时性能最好
#
