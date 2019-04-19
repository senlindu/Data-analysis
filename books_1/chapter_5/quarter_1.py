import numpy as np
import pandas as pd
from pandas import Series, DataFrame

# pandas含有使数据分析工作变得更快更简单的高级数据结构和操作工具
# pandas是基于numpy构建的，让以numpy为中心的应用变得更加简单
# 特点：
# 1、具备按轴自动或显式数据对齐功能的数据结构。可以防止许多由于数据未
# 对齐以及来自不同数据源（索引方式不同）的数据而导致的常见错误
# 2、集成时间序列功能
# 3、既能处理时间序列数据也能处理非时间序列数据的数据结构
# 数学运算和约简（比如对某个轴求和）可以根据不同的元数据（轴编号）执行
# 灵活处理缺失数据
# 合并及其他出现在常见数据库中的关系型运算
#
# pandas的数据结构介绍
# 要使用pandas，你首先要熟悉它的两个主要数据结构：Series和DataFrame
#
# Series
# Series是一种类似于一维数组的对象，由一组数据（各种numpy数据类型）以及
# 一组与之相关的数据标签（即索引）组成
# 仅由一组数据即可产生最简单的Series
# obj = Series([4, 7, -5, 3])
# print(obj)
# Series的字符串表现形式为：索引在左边，值在右边
# 由于我们没有为数据指定索引，于是会自动创建一个0到N-1的整数型索引
# 你可以通过Series的values和index属性获取其数组表示形式和索引对象
# print(obj.values)
# print(obj.index)
# 通常，我们希望所创建的Series带有一个可以对各个数据点进行标记的索引
# obj2 = Series([4, 7, -5, 3], index=['d', 'b', 'a', 'c'])
# print(obj2)
# print(obj2.index)
# 与普通numpy数组相比，你可以通过索引的方式选取Series中的单个或一组值
# print(obj2['a'])
# obj2['d'] = 6
# print(obj2[['c', 'a', 'd']])
# numpy数组运算（根据布尔型数组进行过滤、标量乘法、应用数学函数等）
# 都会保留索引和值之间的链接
# print(obj2)
# print(obj2[obj2 > 0])
# print(obj2 * 2)
# print(np.exp(obj2))
# 还可以将Series看成一个定长的有序字典，因为它是索引值到数据值的一个映射
# 它可以用在许多原本需要字典参数的函数中
# print('b' in obj2)
# print('e' in obj2)
# 如果数据被存放在一个Python字典中，也可以直接通过这个字典来创建Series
# sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
# obj3 = Series(sdata)
# print(obj3)
# 如果只传入一个字典，则结果Series中的索引就是原字典的键（有序排列）
# states = ['California', 'Ohio', 'Oregon', 'Texas']
# obj4 = Series(sdata, index=states)
# print(obj4)
# NaN表示缺失或NA值
# pandas的isnull和notnull函数可用于检测缺失数据
# print(pd.isnull(obj4))
# print(pd.notnull(obj4))
# Series也有类似的实例方法
# print(obj4.isnull())
# Series最重要的一个功能是：在算术运算中会自动对齐不同索引的数据
# print(obj3 + obj4)
# Series对象本身及其索引都有一个name属性，该属性跟pandas其他的关键功能关系非常密切
# obj4.name = 'population'
# obj4.index.name = 'state'
# print(obj4)
# Series的索引可以通过赋值的方式就地修改
# obj.index = ['Bob', 'Steve', 'Jeff', 'Ryan']
# print(obj)


# DataFrame
# DataFrame是一个表格型的数据结构，含有一组有序的列，
# 每列可以是不同的值类型（数值，字符串，布尔型等）
# DataFrame既有行索引也有列索引，
# 可以被看做由Series组成的字典（共用同一个索引）
# 跟其他类似的数据结构相比，DataFrame中面向行和
# 面向列的操作基本上是平衡的
# DataFrame中的数据时以一个或
# 多个二维块存放的（而不是列表、字典或别的一维数据结构）
# 你扔可以轻松地将其表示为更高维度的数据（层次化索引的表格型结构），
# 这是pandas中许多高级数据处理功能的关键要素
#
#
# 构建DataFrame的办法由很多，最常用的一种是直接传入一个由
# 等长列表或numpy数组组成的字典
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
frame = DataFrame(data)
# 结果DataFrame会自动加上索引（跟Series一样），且全部列会被有序排列
# print(frame)
# 如果指定了列序列，则DataFrame的列就会按照指定顺序进行排列
# print(DataFrame(data, columns=['year', 'state', 'pop']))
# 跟Series一样，如果传入的列在数据中找不到，就会产生NA值
frame2 = DataFrame(data, columns=['year', 'state', 'pop', 'debt'],
                   index=['one', 'two', 'three', 'four', 'five'])
# print(frame2)
# print(frame2.columns)
# 通过类似字典标记的方式或属性的方式，可以将DataFrame的列获取为一个Series
# print(frame2['state'])
# print(frame2.year)
# 注意：返回的Series拥有原DataFrame相同的索引，且其name属性也已经被相应地
# 设置好了。行也可以通过位置或名称的方式获取，比如用索引字段ix
# print(frame2.ix['three'])
# 列可以通过赋值的方式进行修改
# 例如，我们可以给那个空的“debt”列赋上一个标量值或一组值
frame2['debt'] = 16.5
frame2['debt'] = np.arange(5.)
# print(frame2)
# 将列表或数组赋值给某个列时，其长度必须跟DataFrame的长度相匹配
# 如果赋值的是一个Series，就会精确匹配DataFrame的索引，所有的空位
# 都将被填上缺失值
val = Series([-1.2, -1.5, -1.7], index=['two', 'four', 'five'])
frame2['debt'] = val
# print(frame2)
# 为不存在的列赋值会创建一个新列。
# 关键字del用于删除列
frame2['eastern'] = frame2.state == 'Ohio'
# print(frame2)
del frame2['eastern']
# print(frame2.columns)
# 通过索引方式返回的列只是相应数据的视图而已，并不是副本
# 对返回的Series所做的任何就地修改全都会反映到源DataFrame上
# 通过Series的copy方法既可显式地复制列
#
# 另一种常见的数据形式是嵌套字典（也就是字典的字典）
pop = {'Nevada': {2001: 2.4, 2002: 2.9},
       'Ohio': {2000: 1.5, 2001: 1.7, 2002: 3.6}}
# 如果将它传给DataFrame，就会被解释为：外层字典的键作为列，
# 内层键则作为行索引
frame3 = DataFrame(pop)
# print(frame3)
# 也可以对该结果进行转置
# print(frame3.T)
# 内层字典的键会被合并、排序以形成最终的索引。
# 如果显式指定了索引，则不会这样
# print(DataFrame(pop, index=[2001, 2002, 2003]))
# 由Series组成的字典差不多也是一样的用法
pdata = {'Ohio': frame3['Ohio'][:-1],
         'Nevada': frame3['Nevada'][:2]}
# print(DataFrame(pdata))


# DataFrame可以输入的数据
# DataFrame可以输入的数据.png
#
# 如果设置了DataFrame的index和columns的name属性，
# 则这些信息也会显示出来
frame3.index.name = 'year'
frame3.columns.name = 'state'
# print(frame3)
# 跟Series一样，values属性也会以二维ndarray的形式返回DataFrame中的数据
# print(frame3.values)
# 如果DataFrame各列的数据类型不同，则值数组的数据类型就会选用能兼容所有列的数据类型
# print(frame2.values)


# 索引对象
# pandas的索引对象负责管理轴标签和掐他元数据（比如轴名称）
# 构建Series或DataFrame时，所用到的任何数组或其他序列的标签
# 都会被转换成一个index
obj = Series(range(3), index=['a', 'b', 'c'])
index = obj.index
# print(index)
# print(index[1:])
# index对象时不可修改的，因此用户不能对其进行修改
# 不可修改性非常重要，因为这样才能使index对象在多个数据结构之间安全共享
index = pd.Index(np.arange(3))
obj2 = Series([1.5, -2.5, 0], index=index)
# print(obj2.index is index)
# Index甚至可以被继承从而实现特别的轴索引功能
# Index对象.png
#
# Index的功能也类似一个固定大小的集合
# print(frame3)
# print('Ohio' in frame3.columns)
# print(2003 in frame3.index)
# 每个索引都有一些方法和属性，它们可用于设置逻辑并回答有关该索引所
# 包含的数据的常见问题
# Index的方法和属性
# Index的方法和属性.png
# 