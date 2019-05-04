import numpy as np
import pandas as pd
from pandas import DataFrame, Series


# 数据转换
# 另一类重要操作则是过滤、清理以及其他的转换工作


#  移除重复数据
#  DataFrame中常常会出现重复行
# data = DataFrame({'k1': ['one'] * 3 + ['two'] * 4,
#                   'k2': [1, 1, 2, 3, 3, 4, 4]})
# print(data)
# DataFrame的duplicated方法返回一个布尔型Series，表示各行是否是重复行
# print(data.duplicated())
# 还有一个与此相关的drop_duplicates方法，它用于返回一个移除了重复行的DataFrame
# print(data.drop_duplicates())
# 这两个方法默认会判断全部列，你也可以指定部分列进行重复项判断。
# 假设你还有一列值，且只希望根据k1列过滤重复项
# data['v1'] = range(7)
# print(data.drop_duplicates(['k1']))
# duplicated和drop_duplicates默认保留的是第一个出现的值组合
# 传入take_last=True则保留最后一个
# take_last改为'last'
# print(data.drop_duplicates(['k1', 'k2'], 'last'))

# 利用函数或映射进行数据转换
# 在对数据集进行转换时，你可能希望根据数组，Series或DataFrame列中的值来实现该转换工作。
# data = DataFrame({'food': ['bacon', 'pulled pork', 'bacon', 'Pastrami',
#                            'corned beef', 'Bacon', 'pastrami', 'honey ham', 'nova lox'],
#                   'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
# print(data)
# 假设你想要添加一列表示该肉类食物来源的动物类型。我们先编写一个肉类到动物的映射
# meat_to_animal = {'bacon': 'pig', 'pulled pork': 'pig', 'pastrami': 'cow',
#                   'corned beef': 'cow', 'honey ham': 'pig', 'nova lox': 'salmon'}
# Series的map方法可以接受一个函数或映射关系的字典型对象，但是有一个小问题，即有些肉类首字母大写，
# 有一些没有。还需要将各个值转换为小写
# data['animal'] = data['food'].map(str.lower).map(meat_to_animal)
# print(data)
# 也可以传入一个能够完成全部这些工作的函数
# print(data['food'].map(lambda x: meat_to_animal[x.lower()]))
# 使用map是一种实现元素级转换以及其他数据清理工作的便捷方式


# 替换值
# 使用fillna方法填充缺失数据可以看做值替换的一种特殊情况
# 虽然前面提到的map可以用于修改对象的数据子集，而replace则提供了一种实现该
# 功能的更简单、更灵活的方式
# data = Series([1., -999., 2., -999., -1000., 3.])
# print(data)
# -999这个值可能是一个表示缺失数据的标记值。要将其替换为pandas能够理解的NA值，
# 我们可以利用replace来产生一个新的Series
# print(data.replace(-999, np.nan))
# 如果你希望一次性替换多个值，可以传入一个由待替换值组成的列表以及一个替换值
# print(data.replace([-999, -1000], np.nan))
# 如果希望对不同的值进行不同的替换，则传入一个由替换关系组成的列表即可
# print(data.replace([-999, -1000], [np.nan, 0]))
# 传入的参数也可以是字典
# print(data.replace({-999:np.nan, -1000:0}))


# 重命名轴索引
# 跟Series中的值一样，轴标签也可以通过函数或映射进行转换，从而得到一个新对象
# 轴还可以就地修改，而无需新建一个数据结构
# data = DataFrame(np.arange(12).reshape((3, 4)),
#                  index=['Ohio', 'Colorado', 'New York'],
#                  columns=['one', 'two', 'three', 'four'])
# 跟Series一样，轴标签也有一个map方法
# print(data.index.map(str.upper))
# 你可以将其赋值给index，这样就可以对DataFrame进行就地修改
# data.index = data.index.map(str.upper)
# print(data)
# 如果想要创建数据集的转换版（而不是修改原始数据），比较实用的方法是rename
# print(data.rename(index=str.title, columns=str.upper))
# 特别说明一下，rename可以结合字典型对象实现对部分轴标签的更新
# print(data.rename(index={'OHIO': 'INDIANA'},
#                   columns={'three': 'peekaboo'}))
# rename帮我们实现了：复制DataFrame并对其索引和列标签进行赋值
# 如果希望就地修改某个数据集，传入inplace=True即可
# 总是返回DataFrame的引用
# _ = data.rename(index={'OHIO': 'INDIANA'}, inplace=True)
# print(data)


# 离散化和面元划分
# 为了便于分析，连续数据常常被离散化或拆分为“面元”
# 假设有一组人员数据，而你希望将它们划分为不同的年龄组
# ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
# 接下来将这些数据划分为“18到25”，“26到35”，“35到60”以及“60以上”几个面元
# 要实现该功能，你需要使用pandas的cut函数
# bins = [18, 25, 35, 60, 100]
# cats = pd.cut(ages, bins)
# print(cats)
# pandas返回的是一个特殊的Categorical对象，你可以将其看做一组表示面元名称的字符串
# 实际上，它含有一个表示不同分类名称的levels数组以及一个为年龄数据进行标号的labels属性
# print(cats.labels)
# levels改为categories
# print(cats.categories)
# print(pd.value_counts(cats))
# 跟“区间”的数学符号一样，圆括号表示开端，而方括号表示闭端（包括）
# 哪边是闭端可以通过right=False进行修改
# print(pd.cut(ages, [18, 26, 36, 61, 100], right=False))
# 你也可以设置自己的面元名称，将labels选项设置为一个列表或数组即可
# group_name = ['Youth', 'YoungAdult', 'MiddleAged', 'Senior']
# print(pd.cut(ages, bins, labels=group_name))
# 如果向cut传入的是面元的数量而不是确切的面元边界，则它会根据数据的最小值和最大值
# 计算等长面元。
# 将一些均匀分布的数据分为四组
# data = np.random.rand(20)
# print(pd.cut(data, 4, precision=2))
# qcut是一个非常类似于cut的函数，它可以根据样本分位数对数据进行面元划分
# 根据数据的分布情况，cut可能无法使各个面元中含有相同数量的数据点
# 而qcut由于使用的是样本分位数，因此可以得到大小基本相等的面元
# data = np.random.randn(1000)
# cats = pd.cut(data, 4)
# print(cats)
# print(pd.value_counts(cats))
# 跟cut一样，也可以设置自定义的分位数（0到1之间的数值，包含端点）
# print(pd.qcut(data, [0, 0.1, 0.5, 0.9, 1.]))
# 这俩个离散化函数对分量和分组分析非常重要


# 检测和过滤异常值
# 异常值的过滤或变换运算在很大程度上其实就是数组运算
# 含有正态分布的DataFrame
# np.random.seed(12345)
# data = DataFrame(np.random.randn(1000, 4))
# print(data.describe)
# 假设你想要找出某列中绝对值大小超过3的值
# col = data[3]
# print(col[np.abs(col) > 3])
# 要选出全部含有“超过3或-3的值”的行，你可以利用布尔型DataFrame以及any方法
# print(data[(np.abs(data) > 3).any(1)])
# 根据这些条件，即可轻松地对值进行设置
# 下面的代码可以将值限制在区间-3到3以内
# data[np.abs(data) > 3] = np.sign(data) * 3
# print(data.describe)
# np.sign这个ufunc返回的是一个由1和-1组成的数组，表示原始值的符号


# 排列和随机采样
# 利用np.random.permutation函数可以轻松实现对Series或DataFrame的列的排列工作
# （permuting, 随机重排列）。通过需要排列的轴的长度调用permutation，可产生一个
# 表示新顺序的整数数组
# df = DataFrame(np.arange(5 * 4).reshape(5, 4))
# sampler = np.random.permutation(5)
# print(sampler)
# 然后就可以在基于ix的索引操作或take函数中使用该数组了
# print(df)
# print(df.take(sampler))
# 如果不想用替换的方式选取随机子集，则可以使用permutation：从permutation返回的数组中
# 切下前k个元素，其中k为期望的子集大小。虽然有很多高效的算法可以实现非替换式采样，但手边
# 就有的工具为什么不用呢？
# print(df.take(np.random.permutation(len(df))[:3]))
# 要通过替换的方式产生样本，最快的方式是通过np.random.randint得到一组随机整数
# bag = np.array([5, 7, -1, 6, 4])
# sampler = np.random.randint(0, len(bag), size=10)
# print(sampler)
# draws = bag.take(sampler)
# print(draws)


# 计算指标/哑变量
# 另一种常用语统计建模或机器学习的转换方式是：将分类变量转换为哑变量矩阵或指标矩阵
# 如果DataFrame的某一列中含有k个不同的值，则可以派生出一个k列矩阵或DataFrame（
# 其值全为1和0）
# pandas有一个get_dummies函数可以实现该功能
df = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'b'],
                'data1': range(6)})
print(df)
print(pd.get_dummies(df['key']))
# 有时候，你可能想给指标DataFrame的列加上一个前缀，以便能够跟其他数据进行合并
# get_dummies的prefix参数可以实现该功能
dummies = pd.get_dummies(df['key'], prefix='key')
df_with_dummy = df[['data1']].join(dummies)
print(df_with_dummy)
# 如果DataFrame中的某行同属于多个分类，则事情就会有点复杂
# 回到本书前面那个MovieLens 1M数据集上
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('e:/datasets/movielens/movies.dat', sep='::',
                       header=None, names=mnames)
print(movies[:10])
# 要为每个genre添加指标变量就需要做一些数据规整操作
# 首先，我们从数据集中抽取出不同的genre值（注意巧用set.union）
genre_iter = (set(x.split('|')) for x in movies.genres)
genres = sorted(set.union(*genre_iter))
# 现在从一个全零DataFrame开始构建指标DataFrame
dummies = DataFrame(np.zeros((len(movies), len(genres))), columns=genres)
# 接下来，迭代每一部电影并将dummies各行的项设置为1
for i, gen in enumerate(moveis.genres):
    dummies.ix[i, gen.split('|')] = 1
# 然后，再将其余movies合并起来
moveis_windic = movies.join(dummies.add_prefix('Genre_'))
print(moveis_windic.ix[0])
# 注意，对于很大的数据，用这种方式构建多成员指标变量就会变得非常慢
# 肯定需要编写一个能够利用DataFrame内部机制的更低级的函数才行
# 一个对统计应用有用的秘诀是，结合get_dummies和诸如cut之类的离散化函数
values = np.random.rand(10)
print(values)
bins = [0, 0.2, 0.4, 0.6, 0.8, 1]
print(pd.get_dummies(pd.cut(values, bins)))
