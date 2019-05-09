import numpy as np
import pandas as pd
from pandas import DataFrame, Series
from numpy.random import randn, rand, permutation
import statsmodels.api as sm


# 分组级运算和转换
# 聚合只不过是分组运算的其中一种而已，它是数据转换的一个特例
# transform和apply方法，能够执行更多其他的分组运算
# 假设为一个DataFrame添加一个用于存放各索引分组平均值的列
# 一个办法是先聚合再合并
df = DataFrame({'key1': ['a', 'a', 'b', 'b', 'a'],
                'key2': ['one', 'two', 'one', 'two', 'one'],
                'data1': randn(5),
                'data2': randn(5)})
# print(df)
k1_means = df.groupby('key1').mean().add_prefix('mean_')
# print(k1_means)
# print(pd.merge(df, k1_means, left_on='key1', right_index=True))
# 虽然这样也行，但是不太灵活，可以将该过程看做利用np.mean函数对两个数据列
# 进行转换。
# 使用transform方法
people = DataFrame(randn(5, 5),
                   columns=['a', 'b', 'c', 'd', 'e'],
                   index=['Joe', 'Steve', 'Wes', 'Jim', 'Travis'])
key = ['one', 'two', 'one', 'two', 'one']
# print(peole.groupby(key).mean())
# print(people.groupby(key).transform(np.mean))
# transform会将一个函数应用到各个分组，然后将结果放置到适当的位置上
# 如果各分组产生的是一个标量值，则该值就会被广播出去
# 如果希望从各组中减去平均值，为此，我们先创建一个距平化函数，然后将
# 其传给transform


def demean(arr):
    return arr - arr.mean()


demeaned = people.groupby(key).transform(demean)
# print(demeaned)
# 可以检查一下demeaned现在的分组平均值是否为0
# print(demeaned.groupby(key).mean())
# 分组距平化还可以通过apply实现


# apply:一般性的“拆分-应用-合并”
# 跟aggregate一样，transform也是一个有着严格条件的特殊函数：传入的
# 函数只能产生两种结果，要么产生一个可以广播的标量值，要么产生一个相同
# 大小的数组
# 最一般化的groupby方法是apply
# apply会将待处理的对象拆分成多个片段，然后对各片段调用传入的函数，最后
# 尝试将各片段组合到一起
# 假设你想要根据分组选出最高的5个tip_pct值
# 编写一个选取指定列具有最大值的行的函数


def top(df, n=5, column='tip_pct'):
    return df.sort_index(by=column)[-n:]

# print(top(tips, n=6))
# 现在，如果对smoker分组并用该函数调用apply，就会得到
# print(tips.groupby('smoker').apply(top))
# top函数会在DataFrame的各个片段上调用，然后结果由pandas.concat
# 组装到一起，并以分组名称进行了标记
# 最终结果就有了一个层次化索引，其内层索引值来自原DataFrame


# 如果传给apply的函数能够接受其他参数或关键字，则可以将这些内容放在
# 函数名后面一并传入
# print(tips.groupby(['smoker', 'day']).apply(top, n=1, column='total_bill'))
# result = tips.groupby('smoker')['tip_pct'].describe()
# print(result)
# print(result.unstack('smoker'))
# 在groupby中，当你调用诸如describe之类的方法时，实际上只是应用了
# 下面两条代码的快捷方式而已
# f = lambda x: x.describe()
# grouped.apply(f)


# 禁止分组键
# 从上面的例子中可以看到，分组键会跟原始对象的索引共同构成结果对象
# 中的层次化索引
# 将group_keys=False传入groupby即可禁止该效果
# print(tips.groupby('smoker', group_key=False).apply(top))


# 分位数和桶分析
# pandas有一些能根据指定面元或样本分位数将数据拆分成多块的工具
# 将这些函数与groupby结合起来，就能非常轻松地实现对数据集的桶或
# 分位数分析了
frame = DataFrame({'data1': randn(1000), 'data2': randn(1000)})
factor = pd.cut(frame.data1, 4)
# print(factor[:10])
# 由cut返回的Factor对象可直接用于groupby
# 因此可以如下对data2做一些统计计算


def get_stats(group):
    return {'min': group.min(),
            'max': group.max(),
            'count': group.count(),
            'mean': group.mean()}


grouped = frame.data2.groupby(factor)
print(grouped.apply(get_stats).unstack())
# 这些都是长度相等的桶。要根据样本分位数得到大小相等的桶，使用qcut
# 传入labels=False即可只获得分位数的编号
# 返回分位数编号
# grouping = pd.qcut(frame.data1, 10, labels=False)
# grouped = frame.data2.groupby(grouping)
# print(grouped.apply(get_stats).unstack())


# 示例：用特定于分组的值填充缺失值
# 对于缺失数据的清理工作，有时你会用dropna将其滤除，有时希望能用一个
# 固定值或由数据集本身衍生出来的值去填充NA值
# 使用fillna这个工具
s = Series(randn(6))
s[::2] = np.nan
print(s)
s.fillna(s.mean())
# 补充，“长度相等的桶”指的是“区间大小相等”
# “大小相等的桶”指的是“数据点数量相等”
# 假设需要对不同的分组填充不同的值
# 将数据分组，并使用apply和一个能够对各数据块调用fillna的函数即可
states = ['Ohio', 'New York', 'Vermont', 'Florida',
          'Oregon', 'Neveda', 'California', 'Idaho']
group_key = ['East'] * 4 + ['West'] * 4
data = Series(randn(8), index=states)
data[['Vermont', 'Neveda', 'Idaho']] = np.nan
print(data)
print(data.groupby(group_key).mean())
# 我们可以用分组平均值去填充NA值


def fill_mean(g): return g.fillna(g.mean)


print(data.groupby(group_key).apply(fill_mean))
# 此外，也可以在代码中预定义各组的填充值
# 由于分组具有一个name属性，可以用
fill_values = {'East': 0.5, 'West': -1}


def fill_func(g): return g.fillna(fill_values[g.name])


print(data.groupby(group_key).apply(fill_func))


# 示例：随机采样和排列
# 假设你想要从一个大数据集中随机抽取样本以进行蒙特卡罗模拟或其他分析工作
# 抽取的方式很多，其中一些效率会比其他的高很多
# 一个办法，选取np.random.permutation(N)的前N个元素，其中N为完整数据
# 的大小，K为期望的样本大小
# 红桃（Heartts） 黑桃（Spades） 梅花（Clubs） 方片（Diamonds）
suits = ['H', 'S', 'C', 'D']
card_val = (range(1, 11) + [10] * 3) * 4
base_names = ['A'] + range(2, 11) + ['J', 'K', 'Q']
cards = []
for suit in ['H', 'S', 'C', 'D']:
    cards.extend(str(num) + suit for num in base_names)

deck = Series(card_val, index=cards)
# 现在有一个长度为52的Series，其索引为牌名，值则是21点或其他游戏中
# 用于计分的点数
print(deck[:13])
# 现在从整副牌中抽出5张


def draw(deck, n=5):
    return deck.take(permutation(len(deck))[:n])


print(draw(deck))
# 假设想要从每种花色中随机抽取两张牌
# 由于花色是牌名的最后一个字符，可以据此进行分组，并使用apply


def get_suit(card): return card[-1]


print(deck.groupby(get_suit).apply(draw, n=2))
# 另一种办法
print(deck.groupby(get_suit, group_keys=False).apply(draw, n=2))


# 示例：分组加权平均数和相关系数
# 根据groupby的“拆分-应用-合并”范式，DataFrame的列与列之间或两个Series
# 之间的运算成为一种标准作业
df = DataFrame({'category': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b'],
                'data': randn(8),
                'weights': rand(8)})
print(df)
# 然后利用category计算分组加权平均数
grouped = df.groupby('category')


def get_wavg(g): return np.average(g['data'], weights=g['weights'])


print(grouped.apply(get_wavg))
# 来自Yahoo!Finance的数据集
close_px = pd.read_csv('e:/examples/stock_px.csv', parse_dates=True, index_col=0)
print(close_px)
print(close_px[-4:])
# 计算一个由日收益率与SPX之间的年度相关系数组成的DataFrame
rets = close_px.pct_change().dropna()


def spx_corr(x): return x.corrwith(x['SPX'])


by_year = rets.groupby(lambda x: x.year)
print(by_year.apply(spx_corr))
# 也可以计算列与列之间的相关系数
# 苹果与微软的年度相关系数
print(by_year.apply(lambda g: g['AAPL'].corr(g['MSFT'])))


# 示例：面向分组的线性回归
# 可以用groupby执行更为复杂的分组统计分析，只要函数返回的是pandas对象
# 或标量值即可
# 定义regress函数（利用statsmodels库）对各数据块执行普通最小二乘法回归


def regress(data, yvar, xvars):
    Y = data[yvar]
    X = data[xvars]
    X['intercept'] = 1.
    result = sm.OLS(Y, X).fit()
    return result.params


# 现在，按年计算AAPL对SPX收益率的线性回归
print(by_year.apply(regress, 'AAPL', ['SPX']))
