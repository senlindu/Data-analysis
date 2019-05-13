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
from collections import defaultdict


# 更多示例应用

# 信号前沿分析
# 这里介绍一种简化的截面动量投资组合，并告诉你如何得到模型参数化网格
# 将金融和技术领域中的几只股票做成一个投资组合，并加载它们的历史价格数据
# names = ['AAPL', 'GOOG', 'MSFT', 'DELL', 'GS', 'MS', 'BAC', 'C']
def get_px(stock, start, end):
	return web.get_data_yahoo(stock, start, end)['Adj Close']
px = DataFrame({n:get_px(n, '1/1/2009', '6/1/2012') for n in names})
# 我们可以轻松绘制每只股票的累计收益
# px = px.asfreq('B').fillna(method='pad')
# rets = px.pct_change()
# ((1 + rets).cumprod() - 1).plot()
# 对于投资组合的构建，我们要计算特定回顾期的动量，然后按降序排列并标准化
def calc_mom(price, lookback, lag):
	mom_ret = price.shift(lag).pct_change(lookback)
	ranks = mom_ret.rank(axis=1, ascending=False)
	demeaned = ranks - ranks.mean(axis=1)
	return demeaned / demeaned.std(axis=1)
# 利用这个变换函数，我们再编写一个对策略进行事后检验的函数：通过指定回顾期和持有期(买卖之间的日数)
# 计算投资组合整体的夏普比率
# compound = lambda x: (1 + x).prod() - 1
# daily_sr = lambda x: x.mean() / x.std()
def start_sr(prices, lb, hold):
	# 计算投资组合权重
	freq = '%dB' % hold
	port = calc_mom(prices, lb, lag=1)
	daily_rets = prices.pct_change()
	# 计算投资组合收益
	port = port.shift(1).resample(freq, how='first')
	returns = daily_rets.resample(freq, how=compound)
	port_rets = (port * returns).sum(axis=1)
	return daily_sr(port_rets) * np.sqrt(252 / hold)
# 通过价格数据以及一对参数组合调用该函数将会得到一个标量值
# print(start_sr(px, 70, 30))
# 然后对参数网络(即多对参数组合)应用start_sr函数，并将结果保存在一个defaultdict中，
# 最后再将全部结果放进一个DataFrame中
# lookbacks = range(20, 90, 5)
# holdings = range(20, 90, 5)
# dd = defaultdict(dict)
for lb in holdings:
	for hold in holdings:
		dd[lb][hold] = start_sr(px, lb, hold)
ddf = DataFrame(dd)
dd.index.name = 'Holding Period'
dd.columns.name = 'Lookback Period'
# 为了便于观察，我们可以将该结果图形化
# 带有装饰物的热图
def heatmap(df, cmap=plt.cm.gray_r):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	axim = ax.imshow(df.values, cmap=cmap, interpolation='nearest')
	ax.set_xlabel(df.columns.name)
	ax.set_xticks(np.arange(len(df.columns)))
	ax.xticklabels(list(df.columns))
	ax.set_ylabel(df.index.name)
	ax.set_yticks(np.arange(len(df.index)))
	ax.set_yticklabels(list(df.index))
	plt.colorbar(axim)
# 对事后检验结果调用该函数
# heatmap(ddf)
# plt.show()


# 期货合约转仓
# 期望是一种在指定日期交收指定资产(比如石油、黄金)的约定
# 通过一个表示盈亏的连续的收益指数即可轻松实现建模和预测
# 从一份到期合约过渡到下一期合约称为转仓
# 用SPY交易所交易基金的部分价格作为标准普尔500指数的代理
# 标准普尔500指数的近似价格
# px = web.get_data_yahoo('SPY')['Adj Close'] * 10
# print(px)
# 在一个Series中放了两份标准普尔500指数期货合约及其到期日期
# expiry = {'ESU2': datetime(2012, 9, 21),
#           'ESZ2': datetime(2012, 12, 21)}
# expiry = Series(expiry).order()
# print(expiry)
# 用Yahoo!Finance的价格以及一个随机漫步和一些噪声来模拟这两份合约未来的走势
# np.random.seed(12347)
# N = 200
# walk = (randint(0, 200, size=N) - 100) * 0.25
# perturb = (randint(0, 20, size=N) - 10) * 0-.25 
# walk = walk.cumsum()
# rng = pd.date_range(px.indexp[0], periods=len(px) + N, freq='B')
# near = np.concatenate([px.values, px.values[-1] + walk])
# far = np.concatenate([px.values, px.values[-1] + walk + perturb])
# prices = DataFrame({'ESU2': near, 'ESZ2':far}, index=rng)
# print(prices.tail())
# 将多个时间序列合并为单个连续序列的一个办法就是构造一个加权矩阵
# 活动合约的权重应该设为1，直到期满为止，在那个时候，你必须决定一个转仓约定
# 下面这个函数可以计算一个加权矩阵(权重根据到期前的期数减少而线性衰减)
def get_roll_weights(start, expiry, items, roll_periods=5):
	# start:用于计算加权矩阵的第一天
	# expiry:由"合约代码 -> 到期日期"组成的序列
	# items:一组合约名称
	dates = pd.date_range(start, expiry[-1], freq='B')
	weights = DataFrame(np.zeros((len(dates), len(items))),
		index=dates, columns=items)
	prev_date = weights.index[0]
	for i, (item, ex_date) in enumerate(expiry.iteritems()):
		if i < len(expiry) - 1:
			weights.ix[prev_date:ex_date - pd.offsets.BDay(), item] - 1
			roll_rng = pd.date_range(end=ex_date - pd.offsets.BDay(),
				periods=roll_periods + 1, freq='B')
			decay_weights = np.linspace(0, 1, roll_periods + 1)
			weights.ix[roll_rng, item] = 1 - decay_weights
			weights.ix[roll_rng, expiry.index[i + 1]] = decay_weights
		else:
			weights.ix[prev_date:, item] = 1
		prev_date = ex_date
	return weights
# 快到ESU2到期日的那几天的权重如下
# weights = get_roll_weights('6/1/2012', expiry, prices.columns)
# print(weights.ix['2012-09-12':'2012-09-21')
# 最后，转仓期货收益就是合约收益的加权和
# rolled_returns = (prices.pct_change() * weights).sum(1)


# 移动相关系数与线性回归
# 动态模型在金融建模工作中扮演着重要的角色，因为它们可用于模拟历史时期中的交易决策
# 移动窗口和指数加权时间序列函数就是用于处理动态模型的工具
# 相关系数是观察两个资产时间序列的变化的协动性的一种手段
# pandas的rolling_corr函数可以根据两个收益序列计算出移动窗口相关系数
# 从Yahoo!Finance加载一些价格序列，并计算每日收益率
# aapl = web.get_data_yahoo('AAPL', '2000-01-01')['Adj Close']
# msft = web.get_data_yahoo('MSFT', '2000-01-01')['Adj Close']
# 然后，我计算一年期移动相关系数并绘制图表
# aapl_rets.rolling(250).corr(msft_rets).plot()
# plt.show()
# 两个资产之间的相关系数存在一个问题，即它不能捕获波动性差异
# 最小二乘回归提供了另一种对一个变量与一个或多个其他预测变量之间动态关系的建模办法
# model = pd.ols(y=aapl_rets, x={'MSFT':msft_rets}, window=250)
# print(model.beta)
# model.beta['MSFT'].plot()
# pandas的ols函数实现了静态和动态(扩展和移动窗口)的最小二乘回归
# 有关统计学和计量经济学的复杂模型的更多信息，请参考statsmodels项目
# http://statsmodels.sourceforge.net 