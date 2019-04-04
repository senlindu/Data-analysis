import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series
# 数据分析的几大类任务

# 与外界进行交互
# 读写各种各样的文件格式和数据库

# 准备
# 对数据进行清理、修整、整合、规范化、重塑、切片切块、变形等处理以便进行分析

# 转换
# 对数据集做一些数学和统计运算以产生新的数据集。比如说，根据分组变量对一个大表进行聚合

# 建模和计算
# 将数据跟统计模型、机器学习算法或其他计算工具来联系起来

# 展示
# 创建交互式的或静态的图片或文字摘要

# 来自bit.ly的1.usa.gov数据
# 每行的格式为json
# path = 'E:/Data-analysis/books_1/datasets/bitly_usagov/example.txt'
# print(open(path).readline())

# python有许多内置或第三方模块可以将json字符串转换成Python字典对象。
# 使用json模块及其loads函数逐行加载已经下载好的数据文件
path = 'E:/Data-analysis/books_1/datasets/bitly_usagov/example.txt'
records = [json.loads(line) for line in open(path)]
# print(records)
# 上面最后那行表达式，叫做列表推导式，是一种在一组字符串（或一组别的对象）
# 上执行一条相同操作（json.loads）的简洁形式
# print(records[0])
# python的索引是从0开始的，不像其他某些语言从1开始（如R）
# 以字符串的形式给出想要访问的键就可以得到当前记录中相应的值了
# print(records[0]['tz'])

# 用纯Python代码对时区进行计数
# 假设我们想要知道该数据集中最常出现的是哪个时区（即tz字段）
# time_zones = [rec['tz'] for rec in records]
# print(time_zones)
# KeyError: 'tz'
# 数据中不是所有的记录都有时区字段
time_zones = [rec['tz'] for rec in records if 'tz' in rec]
# print(time_zones[:20])

# 可以看到有些是未知的（null）
# 对时区进行计数
# 第一种，只使用标准Python库（较难）
# 遍历时区的过程中将计数值保存在字典里

# 为了代码的高重用性，写成函数
# 一种比较复杂的函数


def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts

# 如果对Python标准库非常了解


def get_counts2(sequence):
    # 所有的值均会被初始化为0
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts


# counts = get_counts2(time_zones)
# print(counts)
# print(counts['America/New_York'])
# print(len(time_zones))
# 如果想要得到前10位的时区及其计数值，需要用到一些关于字典的处理技巧


def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]


# print(top_counts(counts))
# 也可以在Python标准库里找到collection.Counter类，能使这个任务变得更简单
counts = Counter(time_zones)
# print(counts.most_common(10))

# 第二种，使用pandas（较简单）
# DataFrame是pandas中最重要的数据结构，用于将数据表示为一个表格
frame = DataFrame(records)
# 在IPython中frame的输出形式是摘要视图，主要用于较大的DataFrame对象
# frame['tz']所返回的Series对象中有一个value_counts方法，该方法可以得到所需的信息
# print(frame['tz'][:10])
# tz_counts = frame['tz'].value_counts()
# print(tz_counts[:10])

# 我们利用绘图库（matplotlib）为这段数据生成一张图片
# 需要先给记录中未知或缺失的时区填上一个替代值
# fillna函数可以替换缺失值（NA），而未知值（空字符串）则可以通过布尔型数组索引加以替换
clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
# print(tz_counts[:10])

# 利用counts对象的plot方法既可得到一张水平条形图
# 在Ipython中执行该语句，然后需要plt.show()语句才能显示图像
# tz_counts[:10].plot(kind='barh', rot=0)

# 在编译系统的文件中加入"shell": "true"，就可以通过ctrl+B执行画图
# N = 50
# x = np.random.rand(N)
# y = np.random.rand(N)
# colors = np.random.rand(N)
# area = np.pi * (15 * np.random.rand(N))**2
# plt.scatter(x, y, s=area, c=colors, alpha=0.5)
# plt.show()

# 我们还可以对这种数据进行很多处理
# a字段含有执行URL短缩操作的浏览器、设备、应用程序的相关信息
# print(frame['a'][1])
# 将这些“agent”字符串中的所有信息都解析出来是一件挺郁闷的工作
# 不过只要掌握了Python内置的字符串函数和正则表达式，事情就好办了
results = Series([x.split()[0] for x in frame.a.dropna()])
# print(results[:5])
# print(results.value_counts()[:8])
# 假设你想按Windows和非Windows用户对时区统计信息进行分解
# 假定只要agent字符串中含有"windows"就认为是Windows用户
# 由于有的agent缺失，首先将它们从数据中移除
cframe = frame[frame.a.notnull()]
# 其次根据a值计算出各行是否是Windows
operating_system = np.where(cframe['a'].str.contains('Windows'),'Windows','Not Windows')
# print(operating_system[:5])
# 接下来根据时区和新得到的操作系统列表对数据进行分组
by_tz_os = cframe.groupby(['tz', operating_system])
# 通过size对分组结果进行计数（类似于value_counts函数），并用unstack对技术结果进行重塑
aggc_counts = by_tz_os.size().unstack().fillna(0)
# print(aggc_counts[:10])
# 选取最常出现的时区
# 根据agg_counts中的行数构造了一个间接索引数组
# 用于按升序排列
indexer = aggc_counts.sum(1).argsort()
# print(indexer[:10])

# 通过take按照这个顺序截取了最后10行
count_subset = aggc_counts.take(indexer)[-10:]
# print(count_subset)
# 生成一张条形图，使用stacked=True来生成一张堆积条形图
# count_subset.plot(kind='barh', stacked=True)
# plt.show()
# 由于这张图中不太容易看清楚较小分组中Windows用户的相对比例
# 因此我们可以将各行规范化为“总计为1”并重新绘图
normed_subset = count_subset.div(count_subset.sum(1), axis=0)
normed_subset.plot(kind='barh', stacked=True)
plt.show()