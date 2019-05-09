import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand


# 数据聚合
# 对于聚合，指的是任何能够从数组产生标量值的数据转换过程
# 聚合运算都有就地计算数据集统计信息的优化实现
# 可以使用自定义的聚合运算，还可以调用分组对象上已经定义好的任何方法
# quantile可以计算Series或DataFrame列的样本分位数
# df = DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
#                 'key2': ['one', 'two', 'one', 'two', 'one'],
#                 'data1': randn(5),
#                 'data2': randn(5)})
# print(df)
# grouped = df.groupby('key1')
# print(grouped['data1'].quantile(0.9))
# 虽然quantile并没有明确地实现与GroupBy，但是一个Series方法
# 实际上，GroupBy会高效地对Series进行切片，然后对各片调用
# piece.quantile(0.9),最后将这些结果组装成最终结果
# 如果要使用你自己的聚合函数，只需将其传入aggregate或agg方法既可


def peak_to_peak(arr):
    return arr.max() - arr.min()


# print(grouped.agg(peak_to_peak))
# 注意：有些方法也是可以用在这里的，即使严格来讲，它们并非聚合运算
# print(grouped.describe())


# 经过优化的groupby方法
# groupby方法.png

# 更高级的聚合功能
# tips = pd.read_csv('e:/examples/tips.csv')
# print(tips)
# 添加“消费占总额百分比”的列
# tips['tip_pct'] = tips['tip'] / tips['total_bill']
# print(tips[:6])


# 面向列的多函数应用
# 对Series或DataFrame列的聚合运算其实就是使用aggregate（使用自定义函数）
# 或调用诸如mean、std之类的方法
# 你可能希望对不同的列使用不同的聚合函数，或一次应用多个函数
tips = pd.read_csv('e:/examples/tips.csv')
tips['tip_pct'] = tips['tip'] / tips['total_bill']
# print(tips)
grouped = tips.groupby(['sex', 'smoker'])
# 可以将函数名以字符串的形式传入
grouped_pct = grouped['tip_pct']
# print(grouped_pct.agg('mean'))
# 如果传入一组函数或函数名，得到的DataFrame的列就会以相应的函数命名
# print(grouped_pct.agg(['mean', 'std', peak_to_peak]))
# 并非一定要接受GroupBy自动给出的那些列名。特别是lambda函数
# 如果传入一个由(name, function)元组组成的列表，则各元组的第一个元素
# 就会被用作DataFrame的列名
grouped_pct.agg(['foo', 'mean'], ('bar', np.std))
# 对于DataFrame，你可以定义一组应用于全部列的函数，或不同的列应用不同
# 的函数
function = ['count', 'mean', 'max']
result = grouped['tip_pct', 'total_bill'].agg(function)
print(result)
# 如上，结果DataFrame拥有层次化的列，相当于分别对各列进行聚合，然后用
# concat将结果组装到一起(列名用作keys参数)
# print(result['tip_pct'])
# 也可以传入带有自定义名称的元组列表
ftuples = [('Durchschnitt', 'mean'), ('Abweichung', np.var)]
grouped['tip_pct', 'total_bill'].agg(ftuples)
# 假设你想要对不同的列应用不同的函数
# 具体的办法是向agg传入一个从列名映射到函数的字典
grouped.agg({'tip':np.max, 'size':'sum'})
grouped.agg({'tip_pct':['min', 'max', 'mean', 'std'],
	'size':'sum'})
# 只有将多个函数应用到至少一列时，DataFrame才会拥有层次化的列


# 以"无索引"的形式返回聚合数据
# 并不总是聚合数据都有由唯一的分组键组成的索引，可以向groupby
# 传入as_index=False以禁用该功能
tips.groupby(['sex', 'smoker'], as_index=False).mean()
# 对结果调用reset_index也能得到这种形式的结果
# 警告：这种用法比较缺乏灵活性
