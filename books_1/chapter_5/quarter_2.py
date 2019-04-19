import numpy as np
import pandas as pd
from pandas import DataFrame, Series

# 基本功能
# 介绍操作Series和DataFrame中的数据的基本手段
#
# 重新索引
# pandas对象的一个重要方法是reindex，其作用是创建一个适应
# 新索引的新对象
# obj = Series([4.5, 7.2, -5.3, 3.6], index=['d', 'b', 'a', 'c'])
# print(obj)
# 调用该Series的reindex将会根据新索引进行重排
# 如果某个索引值当前不存在，就引入缺失值
# obj2 = obj.reindex(['a', 'b', 'c', 'd', 'e'])
# print(obj2)
# print(obj.reindex(['a', 'b', 'c', 'd', 'e'], fill_value=0))
# 对于时间序列这样的有序数据，重新索引时可能需要做一些插值处理
# method选项即可达到此目的，例如使用ffill可以实现前向值填充
# obj3 = Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
# print(obj3)
# print(obj3.reindex(range(6), method='ffill'))
# 有时我们需要比前向和后向填充更为精准的插值方式
# method选项
# method插值方式.png
#
# 对于DataFrame，reindex可以修改行索引、列或两个都修改
# 如果仅传入一个序列，则会重新索引行
# frame = DataFrame(np.arange(9).reshape((3, 3)),
# index=['a', 'c', 'd'], columns=['Ohio', 'Texas', 'California'])
# print(frame)
# frame2 = frame.reindex(['a', 'b', 'c', 'd'])
# print(frame2)
# 使用columns关键字即可重新索引列
# states = ['Texas', 'Utah', 'California']
# print(frame.reindex(columns=states))
# 也可以同时对行和列进行重新索引，而插值则只能按行应用（即轴0）
# print(frame.reindex(index=['a', 'b', 'c', 'd'], columns=states, method='ffill'))
# error:index must be monotonic increasing or decreasing
# 改写为下面写法
# print(frame.reindex(index=['a', 'b', 'c', 'd'], columns=states).ffill())
# 利用ix的标签索引功能，重新索引任务可以变得更简洁
# print(frame.ix[['a', 'b', 'c', 'd'], states])
# reindex函数的参数
# reindex函数的参数.png
#
#
# 丢弃指定轴上的项
# 丢弃某条轴上的一个或多个项很简单，只要有一个索引数组或列表即可
# 由于需要执行一些数据整理和集合逻辑，所以drop方法返回的是一个
# 在指定轴上删除了指定值的新对象
# obj = Series(np.arange(5), index=['a', 'b', 'c', 'd', 'e'])
# new_obj = obj.drop('c')
# print(obj)
# print(new_obj)
# print(obj.drop(['d', 'c']))
# 对于DataFrame，可以删除任意轴上的索引值
# data = DataFrame(np.arange(16).reshape((4, 4)),
#                  index=['Ohio', 'Colorado', 'Utah', 'New York'],
#                  columns=['one', 'two', 'three', 'four'])
# print(data)
# print(data.drop(['Colorado', 'Ohio']))
# print(data.drop('two', axis=1))
# print(data.drop(['two', 'four'], axis=1))


# 索引、选取和过滤
# Series索引（obj[...]）的工作方式类似于numpy数组的索引，
# 只不过Series的索引值不只是整数
# obj = Series(np.arange(4.), index=['a', 'b', 'c', 'd'])
# print(obj)
# print(obj['b'])
# print(obj[1])
# print(obj[2:4])
# print(obj[['b', 'a', 'd']])
# print(obj[[1, 3]])
# print(obj[obj < 2])
# 利用标签的切片运算与普通的Python切片运算不同，其末端是包含的
# print(obj['b':'c'])
# 设置方式也很简单
# obj['b':'c'] = 5
# print(obj)
# 对DataFrame进行索引其实就是获取一个或多个列
# data = DataFrame(np.arange(16).reshape((4, 4)),
#                  index=['Ohio', 'Colorado', 'Utah', 'New York'],
#                  columns=['one', 'two', 'three', 'four'])
# print(data)
# print(data['two'])
# print(data[['three', 'one']])
# 这种索引方式由几个特殊的情况
# 首先通过切片或布尔型数组选取行
# print(data[:2])
# print(data[data['three'] > 5])
# 另一种用法是通过布尔型DataFrame进行索引
# print(data < 5)
# data[data < 5] = 0
# print(data)
# 为了在DataFrame的行上进行标签索引，引入了专门的索引字段ix
# ix使你可以通过numpy式的标记法以及轴标签从DataFrame中选取
# 行和列的子集
# print(data.ix['Colorado', ['two', 'three']])
# print(data.ix[['Colorado', 'Utah'], [3, 0, 1]])
# print(data.ix[2])
# print(data.ix[:'Utah', 'two'])
# print(data.ix[data.three > 5, :3])
# 对pandas对象中的数据的选取和重排方式有很多
#
# DataFrame的索引选项
# DataFrame的索引选项_1.png
# DataFrame的索引选项_2.png
#
#
# 算术和数据对齐
# pandas最重要的一个功能是，它可以对不同索引的对象进行算术运算
# 在将对象相加时，如果存在不同的索引对，则结果的索引就是该索引对
# 的并集
# s1 = Series([7.3, -2.5, 3.4, 1.5], index=['a', 'c', 'd', 'e'])
# s2 = Series([-2.1, 3.6, -1.5, 4, 3.1], index=['a', 'c', 'e', 'f', 'g'])
# print(s1)
# print(s2)
# print(s1 + s2)
# 自动的数据对齐操作在不重叠的索引出引入了NA值
# 缺失值会在算术运算过程中传播
# 对于DataFrame，对齐操作会同时发生在行和列上
# df1 = DataFrame(np.arange(9).reshape((3, 3)),
#                 columns=list('bcd'),
#                 index=['Ohio', 'Texas', 'Colorado'])
# df2 = DataFrame(np.arange(12).reshape((4, 3)),
#                 columns=list('bde'),
#                 index=['Utah', 'Ohio', 'Texas', 'Oregon'])
# print(df1)
# print(df2)
# 把他们相加后将会返回一个新的DataFrame，其索引和列为原来两个DataFrame的并集
# print(df1 + df2)


# 在算术方法中填充值
# 在对不同索引的随想进行算术运算时，你可能希望当一个对象中某个轴
# 标签在另一个对象中找不到时填充一个特殊值
# df1 = DataFrame(np.arange(12).reshape((3, 4)), columns=list('abcd'))
# df2 = DataFrame(np.arange(20).reshape((4, 5)), columns=list('abcde'))
# print(df1)
# print(df2)
# 将它们相加时，没有重叠的位置就会产生NA值
# print(df1 + df2)
# 使用df1的add方法，传入df2以及一个fill_value参数
# print(df1.add(df2, fill_value=0))
# 与此类似，在对Series或DataFrame重新索引时，也可以指定一个填充值
# print(df1.reindex(columns=df2.columns, fill_value=0))

# 灵活的运算方法
# 灵活的运算方法.png
#
# DataFrame和Series之间的运算
# 跟numpy数组一样，DataFrame与Series之间算术运算也是由明确规定的
# 计算一个二维数组与其某行之间的差
# arr = np.arange(12).reshape((3, 4))
# print(arr)
# print(arr[0])
# print(arr - arr[0])
# 这就叫做广播
# DataFrame和Series之间的运算差不多也是如此
# frame = DataFrame(np.arange(12).reshape((4, 3)),
#                   columns=list('bde'),
#                   index=['Utah', 'Ohio', 'Texas', 'Oregon'])
# series = frame.ix[0]
# print(frame)
# print(series)
# 默认情况下，DataFrame和Series之间的算术运算会将Series的索引匹配
# 到DataFrame的列，然后沿着行一直向下传播
# print(frame - series)
# 如果某个索引值在DataFrame的列或Series的索引中找不到，
# 则参与运算的两个对象就会被重新索引以形成并集
# series2 = Series(range(3), index=['b', 'e', 'f'])
# print(frame + series2)
# 如果你希望匹配行且在列上广播，则必须使用算术运算方法
# series3 = frame['d']
# print(frame)
# print(series3)
# print(frame.sub(series3, axis=0))
# 传入的轴号就是希望匹配的轴


# 函数应用和映射
# numpy的ufuncs(元素级数组方法)也可用于操作pandas对象
# frame = DataFrame(np.random.randn(4, 3),
#                   columns=list('bde'),
#                   index=['Utah', 'Ohio', 'Texas', 'Oregon'])
# print(frame)
# print(np.abs(frame))
# 另一个常见的操作是，将函数应用到由各行或列所形成的一维数组上
# DataFrame的apply方法既可实现此功能
# f = lambda x: x.max() - x.min()
# print(frame.apply(f))
# print(frame.apply(f, axis=1))
# 许多最为常见的数组统计功能都能被实现成DataFrame方法（如sum和mean）
# 因此无需使用apply方法
# 出标量值外，传递给apply的函数还可以返回由多个值组成的Series


# def f(x):
#     return Series([x.min(), x.max()], index=['min', 'max'])


# print(frame.apply(f))
# 此外，元素级的Python函数也是可以用的
# 假如你想得到frame中各个浮点值的格式化字符串，使用applymap即可


# def format(x): return '%.2f' % x


# print(frame.applymap(format))
# 之所以叫做applymap，是因为Series有一个用于应用元素级函数的map方法
# print(frame['e'].map(format))


# 排序和排名
# 根据条件对数据集排序也是一种重要的内置运算
# 要对行或列索引进行排序，可使用sort_index方法，它将返回
# 一个已排序的新对象
# obj = Series(range(4), index=['d', 'a', 'b', 'c'])
# print(obj.sort_index())
# 而对于DataFrame，则可以根据任意一个轴上的索引进行排序
# frame = DataFrame(np.arange(8).reshape((2, 4)),
#                   columns=['d', 'a', 'b', 'c'],
#                   index=['three', 'one'])
# print(frame.sort_index())
# print(frame.sort_index(axis=1))
# 数据默认是按升序排序的，也可以降序排序
# print(frame.sort_index(axis=1, ascending=False))
# 若要按值对Series进行排序，可使用其order方法
# python3.6 之后没有order方法，可使用sort_value
# obj = Series([4, 7, -3, 2])
# print(obj.sort_values())
# 在排序时，任何缺失值默认都会被放到Series的末尾
# obj = Series([4, np.nan, 7, np.nan, -3, 2])
# print(obj.sort_values())
# 在DataFrame上，你可能希望根据一个或多个列中的值进行排序
# 将一个或多个列的名字传递给by选项即可达到目的
# frame = DataFrame({'b': [4, 7, -3, 2], 'a': [0, 1, 0, 1]})
# print(frame)
# 需要使用sort_values
# print(frame.sort_values(by='b'))
# 要根据多个列进行排序，传入名称的列表即可
# print(frame.sort_values(by=['a', 'b']))

# 排名(ranking)跟排序关系密切，且它会增设一个排名值（从1开始，
# 一直到数组中有效数据的数量）。它跟numpy.argsort产生的间接排序
# 索引差不多，只不过它可以根据某种规则破坏平级关系。
# Series和DataFrame的rank方法。
# 默认情况下，rank是通过“为各组分配一个平均排名”的方式破坏平级关系的
# obj = Series([7, -5, 7, 4, 2, 0, 4])
# print(obj.rank())
# 也可以根据值在原数据中出现的顺序给出排名
# print(obj.rank(method='first'))
# 当然你也可以按降序进行排名
# print(obj.rank(ascending=False, method='max'))
# DataFrame可以在行或列上计算排名
# frame = DataFrame({'b':[4.3, 7, -3, 2],
# 	'a':[0, 1, 0, 1], 'c':[-2, 5, 8, -2.5]})
# print(frame)
# print(frame.rank(axis=1))

# 排名时用于破坏平级关系的method选项
# 排名破坏平级关系method选项.png


# 带有重复值的轴索引
# 虽然许多pandas函数都要求标签唯一，但这并不是强制性的
# 下面就是带有重复索引值的Series
# obj = Series(range(5), index=['a', 'a', 'b', 'b', 'c'])
# print(obj)
# 索引的is_unique属性可以告诉你它的值是否是唯一的
# print(obj.index.is_unique)
# 对于带有重复值的索引，数据的选取的行为将会有些不同
# 如果某个索引对应多个值，则返回一个Series；
# 对应单个值的，则返回一个标量值
# print(obj['a'])
# print(obj['c'])
# 对DataFrame的行进行索引时也是如此
# df = DataFrame(np.random.randn(4, 3),
#                index=['a', 'a', 'b', 'b'])
# print(df)
# print(df.ix['b'])
