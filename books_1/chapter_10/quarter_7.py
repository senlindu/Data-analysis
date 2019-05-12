import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from pandas.tseries.offsets import Hour, Minute, Day, MonthEnd
import matplotlib.pyplot as plt


# 时间序列绘图
# pandas时间序列的绘图功能在日期格式化方面比matplotlib原生的要好
# 从Yahoo!Finamce下载了几只美国股票的一些价格数据
close_px_all = pd.read_csv('e:/examples/stock_px.csv', parse_dates=True,
                           index_col=0)
close_px = close_px_all[['AAPL', 'MSFT', 'XOM']]
close_px = close_px.resample('B', fill_method='ffill')
# print(close_px)
# 对其中任意一列调用plot即可生成一张简单的图表
# close_px['AAPL'].plot()

# 当对DataFrame调用plot时，所有时间序列都会被绘制在一个subplot上，并有
# 一张图例说明哪个是哪个
# 这里只绘制了2009年的数据，月份和年度都被格式化到了X轴上
# close_px.ix['2009'].plot()
# 展示苹果公司在2011年1月到3月间的每日股价
# close_px['AAPL'].ix['01-2011':'03-2011'].plot()
# 季度型频率的数据会用季度标记进行格式化
# appl_q = close_px['AAPL'].resample('Q-DEC', fill_method='ffill')
# appl_q.ix['2009':].plot()
# pandas时间序列在绘图方面还有一个特点：当右键点击并拖拉时，日期会动态展开或
# 收缩，且绘图窗口中的时间区间会被重新格式化
# 只有在交互模式下使用matplotlib才会有此效果
# plt.show()
