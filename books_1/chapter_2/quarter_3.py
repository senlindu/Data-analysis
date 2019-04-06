import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt

# Git Your branch is ahead of 'origin/master' by X commits解决方法
# git reset --hard origin/master
# 在本地领先远程仓库的cache中删除掉那个需要上传的大文件
# git rm --cached YOR-GIANT-FILE
# git commit --amend -CHEAD

# 1880年-2010年间全美婴儿姓名
# 美国社会保障总署提供了一份从1880年到2010年的婴儿名字频率数据
# bnames = ['name', 'sex', 'births']
# babynames = pd.read_table('E:/Data-analysis/books_1/datasets/babynames/yob1880.txt',
#                          sep = ",", header = None, names = bnames, engine = 'python')
# print(babynames[:10])
# 你可以用这个数据集做很多事
# 1、计算指定名字的年度比例
# 2、计算某个名字的相对排名
# 3、计算各年度最流行的名字，以及增长或减少最快的名字
# 4、分析名字趋势：元音、辅音、长度、总体多样性、拼写变化、首尾字母等
# 5、分析外源性趋势：圣经中的名字、名人、人口结构变化等
# 由于这是一个非常标准的以逗号隔开的格式，可以用pandas.read_csv将其加载到DataFrame
# names1880=pd.read_csv('E:/Data-analysis/books_1/datasets/babynames/yob1880.txt',
#                  names=bnames)
# print(names1880)
# 这些文件中仅含有当年出现超过5次的名字
# 可以用births列的sex分组小计表示该年度的births总计
# print(names1880.groupby('sex').births.sum())
# 由于该数据集按年度被分隔了多个文件，所以第一件事就是将所有数据都组装到
# 一个DataFrame里面，并加上一个year字段
# 使用pandas.concat即可达到这个目的
years = range(1880, 2011)
pieces = []
columns = ['name', 'sex', 'births']
for year in years:
    path = 'E:/Data-analysis/books_1/datasets/babynames/yob%d.txt' % year
    frame = pd.read_csv(path, names=columns)

    frame['year'] = year
    pieces.append(frame)
# 将所有数据整合到单个DataFrame中
names = pd.concat(pieces, ignore_index=True)

# 1、concat默认是按行将多个DataFrame组合到一起的
# 2、必须制定ignore_index=True,因为我们不希望保留read_csv所返回的原始行号
# print(names)

# 可以利用groupby或pivot_table在year和sex级别上对其进行聚合
total_births = names.pivot_table('births', index='year',
                                 columns='sex', aggfunc=sum)
# print(total_births.tail())
# total_births.plot(title="Total births by sex and year")
# plt.show()

# 插入一个prop列，用于存放指定名字的婴儿数相对于总出生数的比例
# prop值为0.02表示每100名婴儿中有2名取了当前的名字
# 我们先按year和sex分组，然后再将新列加到各个分组上


def add_prop(group):
    # 整数除法会向下圆整
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group


names = names.groupby(['year', 'sex']).apply(add_prop)
# print(names)
# 执行这样的分组处理时，一般都应该做一些有效性检查，比如验证所有分组的prop的总和是否为1
# 由于这是一个浮点型数据，所以我们应该用np.allclose来检查这个分组总计值是否足够近似于1
# print(np.allclose(names.groupby(['year','sex']).prop.sum(), 1))
# 为了便于实现更进一步的分析，我需要取出该数据的一个子集：每对sex/year组合的前1000个名字
# 又是一个分组操作


def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]


grouped = names.groupby(['year', 'sex'])
top1000 = grouped.apply(get_top1000)
# print(top1000)

# 也可以这样
# pieces = []
# for year, group in names.groupby(['year', 'sex']):
#     pieces.append(group.sort_values(by='births', ascending=False)[:1000])
# top1000 = pd.concat(pieces, ignore_index=True)
# 分析命名趋势
# 将前1000个名字分为男女两个部分
boys = top1000[top1000.sex == 'M']
girls = top1000[top1000.sex == 'F']
total_births = top1000.pivot_table('births', index='year',
                                   columns='name', aggfunc=sum)
# print(total_births)
# subset = total_births[['John', 'Harry', 'Mary', 'Marilyn']]
# subset.plot(subplots=True, figsize=(12, 10), grid=False,
# title="Number of births per year")
# plt.show()

# 评估命名多样性的增长
# 一个办法是计算最流行的1000个名字所占的比例，按year和sex进行聚合并绘图
table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
# table.plot(title='Sum of table1000.prop by year and sex',
# yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))
# plt.show()
# 计算占总出生人数前50%的不同名字的数量，这个数字不太好计算
# 只考虑2010年男孩的名字
df = boys[boys.year == 2010]
# print(df)
# 在对prop降序排列之后，我们想知道前面多少个名字的人数加起来才够50%
# 1、使用for循环实现
# 2、numpy方式
# 先计算prop的累计和cumsum，然后再通过searchsorted方法
# 找出0.5应该被插入在哪个位置才能保证不破坏顺序
prop_cumsum = df.sort_values(by='prop', ascending=False).prop.cumsum()
# print(prop_cumsum[:10])
# print(prop_cumsum.searchsorted(0.5))
# 由于索引是从0开始，需要给结果加1
df = boys[boys.year == 1900]
in1900 = df.sort_values(by='prop', ascending=False).prop.cumsum()
# print(in1900.searchsorted(0.5) + 1)
# 对所有year/sex组合执行这个计算
# 按这两个字段进行groupby处理，然后用一个函数计算各分组的这个值


def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().searchsorted(q) + 1


diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
diversity = diversity.unstack('sex')
# diversity这个DataFrame拥有两个时间序列（每个性别各一个，按年度索引）
# print(diversity.head())
# diversity.plot(title="Number of popular names in top 50%")
# plt.show()
# 最后一个字母  的变革
# 首先将全部出生数据在年度、性别以及末尾字母上进行了聚合


def get_last_letter(x): return x[-1]


last_letters = names.name.map(get_last_letter)
last_letters.name = 'last_letter'
table = names.pivot_table('births', index=last_letters,
                          columns=['sex', 'year'], aggfunc=sum)
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
# print(subtable.head())
# 按总出生数对该表进行规范化处理，以便计算出各性别各末字母占总出生人数的比例
subtable.sum()
letter_prop = subtable / subtable.sum().astype(float)
fig, axes = plt.subplots(2, 1, figsize=(10, 8))
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)
# plt.show()
# 回到之前创建的那个完整表，按年度和性别对其进行怪范化处理，并在男孩名字中选取几个字母
# 最后进行转置以便将各个列做成一个时间序列
letter_prop = table / table.sum().astype(float)
dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T
# print(dny_ts.head())
# 使用上面的DataFrame绘制一张趋势图
dny_ts.plot()
# plt.show()
# 编程女孩名字的男孩名字（以及相反的情况）
# 例如Lesley或Leslie
# 回到top1000数据集，找出其中以“lesl”开头的一组名字
all_names = top1000.name.unique()
mask = np.array(['lesl' in x.lower() for x in all_names])
lesley_like = all_names[mask]
# print(lesley_like)
# 利用这个结果过滤其他的名字，并按名字分组计算出生数以查看相对频率
filtered = top1000[top1000.name.isin(lesley_like)]
filtered.groupby('name').births.sum()
# 按照性别和年度进行聚合，并按年度进行规范化处理
table = filtered.pivot_table('births', index='year',
                             columns='sex', aggfunc='sum')
table = table.div(table.sum(1), axis=0)
table.tail()
table.plot(style={'M': 'k-', 'F': 'k--'})
plt.show()
