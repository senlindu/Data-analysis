import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse

# 时间序列
# 不管在哪个领域中，时间序列数据都是一种重要的结构化数据形式
# 在多个时间点观察或测量到的任何事物都可以形成一段时间序列
# 很多时间序列是固定频率的，即数据点是根据规律定期出现的
# 时间㤡也可以是不定期的
# 时间序列数据的意义取决于具体的应用场景，主要有以下几种：
# 1、时间戳，特定的时刻
# 2、固定时期，如2019年5月或2020年全年
# 3、时间间隔，由起始和结束时间戳表示。时期可以被看做间隔的特例
# 4、实验或过程时间，每个时间点都是相对于特定起始时间的一个度量。例如，
# 从放入烤箱时起，每秒钟饼干的直径

# 最简单也最常见的实践序列都是用时间戳进行索引的
# pandas提供了一组标准的时间序列处理工具和数据算法


# 日期和时间数据类型及工具
# Python标准库包含用于日期和时间数据的数据类型，而且还有日历方面的功能
# 我们主要用到datetime、time、以及calendar模块
# datetime.datetime是用得最多的数据类型
# now = datetime.now()
# print(now)
# print(now.year)
# print(now.month)
# print(now.day)
# datetime以毫秒形式存储日期和时间
# datetime.timedelta表示两个datetime对象之间的时间差
# delta = datetime(2019, 1, 7) - datetime(2009, 6, 24, 8, 15)
# print(delta)
# print(delta.days)
# print(delta.seconds)
# 可以给datetime对象加上（或减去）一个或多个timedelta，就会产生一个新对象
# start = datetime(2019, 5, 10)
# print(start + timedelta(12))
# print(start - 2 * timedelta(12))


# datetime模块中的数据类型
# datetime数据类型.png


# 字符串和datetime的相互转换
# 利用str或strftime方法(传入一个格式化字符串)，datetime对象和pandas的
# Timestamp对象可以被格式化为字符串
# stamp = datetime(2019, 5, 10)
# print(str(stamp))
# print(stamp.strftime('%Y-%m-%d'))
# datetime.strptime也可以用这些格式化编码将字符串转换为日期
# value = '2019-05-10'
# print(datetime.strptime(value, '%Y-%m-%d'))
datestrs = ['7/6/2011', '8/6/2011']
# print([datetime.strptime(x, '%m/%d/%Y') for x in datestrs])
# datetime.strptime是通过已知格式进行日期解析的最佳方式
# 对于一些常见的日期格式，可以用dateutil这个第三方包中的parser.parse方法
# print(parse('2019-5-10'))
# dateutil可以解析几乎所有人类能够理解的日期表示形式
# print(parse('May 31, 1997 10:45 PM'))
# 在国际通用的格式中，日通常出现在月的前面，传入dayfirst=True即可解决这个问题
# print(parse('6/12/2011', dayfirst=True))
# pandas通常是用于处理成组日期的，不管这些日期是DataFrame的轴索引还是列
# to_datetime方法可以解析多种不同的日期表示形式
# 对标准日期格式的解析非常快
# print(datestrs)
# print(pd.to_datetime(datestrs))
# 还可以处理缺失值(None, 空字符串等)
idx = pd.to_datetime(datestrs + [None])
print(idx)
print(idx[2])
print(pd.isnull(idx))
# NaT是pandas中时间戳数据的NA值


# datetime格式定义
# datetime格式定义_1.png
# datetime格式定义_2.png
# datetime对象还有一些特定于当钱环境的格式化选项

# 特定于当前环境的日期格式
# 特定当钱环境的日期格式.png
