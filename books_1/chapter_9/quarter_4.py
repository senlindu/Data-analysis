import numpy as np 
import pandas as pd 
from pandas import DataFrame, Series 
from numpy.random import randn, rand 


# 透视表和交叉表
# 透视表是各种电子表格程序和其他数据分析软件中一种常见的数据汇总工具
# 它根据一个或多个键对数据进行聚合，并根据行和列上的分组键将数据分配
# 到各个矩形区域中。
# 在Python和pandas中，可以通过groupby功能以及重塑运算制作透视表
# DataFrame有一个pivot_table方法，此外还有一个顶级的pandas.pivot_table
# 函数
# 除能为groupby提供便利之外，pivot_table还可以添加分项小计


# 假设想要根据sex和smoker计算分组平均数（pivot_table的默认聚合类型）
# 并将sex和smoker放到行上
tips.pivot_table(rows=['sex', 'smoker'])
# 假设我们只想聚合tip_pct和size，而且想根据day进行分组
# 将smoker放到列上，把day放到行上
print(tips.pivot_table(['tip_pct', 'size'], rows=['sex', 'day'],
	                   cols='smoker'))
# 还可以对这个表作进一步处理，传入margins=True添加分项小计。这将会添加标签
# 为All的行和列，其值对应于单个等级中所有数据的分组统计
# ALL值为平均数：不单独考虑烟民和非烟民，不单独考虑行分组两个级别中的任何
# 单项
print(tips.pivot_table(['tip_pct', 'size'],
	                   rows=['sex', 'day'],
	                   cols='smoker', margins=True))
# 要使用其他的聚合函数，将其传给aggfunc即可
# 使用count或len可以得到有关分组大小的交叉表
print(tips.pivot_table('tip_pct',
	                  rows=['sex', 'smoker'],
	                  cols='day',
	                  aggfunc=len,
	                  margins=True))
# 如果存在空的组合（NA），可能会希望设置一个fill_value
print(tips.pivot_table('size', 
	                   rows=['time', 'sex', 'smoker'],
	                   cols='day',
	                   aggfunc='sum',
	                   fill_value=0))


# pivot_table参数说明
# pivot_table参数.png


# 交叉表：crosstab
# 交叉表是一种用于计算分组频率的特殊透视表
# 范例数据取自交叉表的Wikipedia页
# 想要根据性别和用手习惯对这段数据进行统计汇总
# 虽然可以用pivot_table实现，但pandas.crosstable函数会更方便
# print(pd.crosstab(data.Gender, data.Handedness, margins=True))
# crosstab的前两个参数可以是数组、Series或数组列表
# print(pd.crosstab([tips.time, tips.day], tips.smoker, margins=True))
# 