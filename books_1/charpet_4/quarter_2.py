import numpy as np
import matplotlib.pyplot as plt


# 通用函数： 快速的元素级数组函数

# 通用函数（即ufunc）是一种对ndarray中的数据执行元素级运算的函数
# 你可以将其看做简单函数（接受一个或多个标量值，并产生一个或多个标量值）的矢量化包装器

# 许多ufunc都是简单的元素级变体，如sqrt和exp
# arr = np.arange(10)
# np.sqrt(arr)
# np.exp(arr)
# 另外一些（如add或maximum）接受两个数组（因此也叫二元），并返回一个结果数组
# x = randn(8)
# y = randn(8)
# x
# y
# np.maximum(x, y)
# 虽然并不常见，但有些ufunc可以返回多个数组
# modf就是一个，是内置函数divmod的矢量化版本，用于浮点数数组的小数和整数部分
# arr = randn(7) * 5
# np.modf(arr)
#
# 一元ufunc和二元ufunc
# 一元ufunc_1.png
# 一元ufunc_2.png
# 一元ufunc_3.png
# 二元ufunc_1.png
# 二元ufunc_2.png
#
# 利用数组进行数据处理
#
# numpy数组使你可以将许多种数据处理任务表述为简洁的数组表达式（否则需要编写循环）
# 用数组表达式代替循环的做法，通常被称为矢量化
# 矢量化数组运算要比等价的纯Python方式快上一两个数量级，甚至更多，尤其是各种数值计算
# 广播是一种针对矢量化计算的强大手段
#
# 假设我们想要在一组值（网格型）上计算函数sqrt(x^2 + y^2)
# np.meshgrid函数接受两个一维数组，并产生两个二维矩阵（对应于两个数组中所有的（x, y）对）
# points = np.arange(-5, 5, 0.01)  # 1000个间隔相等的点
# xs, ys = np.meshgrid(points, points)
# print(ys)

# 现在，对该函数的求值运算就好办了，把这两个数组当做两个浮点数那样编写表达式即可
# z = np.sqrt(xs ** 2 + ys ** 2)
# print(z)
# plt.imshow(z, cmap=plt.cm.gray)
# plt.colorbar()
# plt.title("Image plot of $\sqrt{x^2 + y^2}$ for a grid of values")
# plt.show()


# 将条件逻辑表述为数组运算
#
# numpy.where函数是三元表达式x if condition else y的矢量化版本
# 假设我们有一个布尔数组和两个值数组
# xarr = np.array([1.1, 1.2, 1.3, 1.4, 1.5])
# yarr = np.array([2.1, 2.2, 2.3, 2.4, 2.5])
# cond = np.array([True, False, True, True, False])

# 假设我们想要根据cond中的值选取xarr和yarr的值，当cond中的值为True时，选取xarr的值
# 否则从yarr中选取
# 俩表推导式的写法
# result = [(x if c else y) for x, y, c in zip(xarr, yarr, cond)]
# print(result)
# 但是有两个问题：
# 1.对大数组的处理速度不是很快（因为所有工作都是由纯Python完成的）
# 2.无法用于多维数组
#
# 使用np.where
# result = np.where(cond, xarr, yarr)
# print(result)

# np.where的第二个和第三个参数不必是数组，都可以是标量值
# 在数据分析工作中，where通常用于根据另一个数组而产生一个新的数组
# 假设有一个由随机数据组成的矩阵，你希望将所有正值替换为2，将所有负值替换为-2
# 弱利用np.where，则会非常简单
# arr = np.random.randn(4, 4)
# print(arr)
# print(np.where(arr > 0, 2, -2))
# 只将正值转换为2
# print(np.where(arr > 0, 2, arr))
# 传递给where的数组大小可以不相等，甚至可以是标量值
# 我有两个布尔型数组cond1和cond2，希望根据4中不同的布尔值组合实现不同的赋值操作
# result = 【】
# for i in range(n):
# 	if cond1[i] and cond2[i]:
# 		result.append(0)
# 	elif cond1[i]:
# 		result.append(1)
# 	elif cond2[i]:
# 		result.append(2)
# 	else:
# 		result.append(3)
# 这个for循环可以被改写为一个嵌套的where表达式
# np.where(cond1&cond2, 0, np.where(cond1, 1, np.where(cond2, 2, 3)))
# 还可以利用布尔值在计算过程中可以被当做0或1处理，写成如下
# result= 1 * （cond1 -cond2）+ 2 * (cond2 & -cond1) + 3 * -(cond1 | cond2)
#
# 数学和统计方法
# 可以通过数组上的一组数学函数对整个数组或某个轴向的数据进行统计计算
# sum、mean以及标准差std等聚合计算（通常叫约简）既可以当做数组的实例方法调用
# 也可以当做顶级numpy函数使用
# arr = np.random.randn(5, 4)  # 正态分布的数据
# print(arr.mean())
# print(np.mean(arr))
# print(arr.sum())
# mean和sum这类函数可以接受一个axis参数（用于计算该轴向上的统计值），最终结果是一个少一维的数组
# print(arr.mean(axis=1))
# print(arr.sum(0))
# 其他如cumsum和cumprod之类的方法则不聚合，而是产生一个由中间结果组成的数组
#
# arr = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
# print(arr.cumsum(0))
# print(arr.cumprod(1))
#
# 基本数组统计方法
# 基本数组统计方法_1.png
# 基本数组统计方法_2.png
#
# 用于布尔型数组的方法
#
# 在上面的方法中，布尔值会被强制转换为1和0，因此，sum经常被用来对布尔数组中的true值计数
# arr = np.random.randn(100)
# print((arr > 0).sum())
# 还有两个方法any和all，它们对布尔型数组非常有用
# any用于测试数组中是否存在一个或多个true
# all检查数组中所有值是否都是true
# bools = np.array([False, False, True, False])
# print(bools.any())
# print(bools.all())
# 这两个方法也能用于非布尔型数组，所有非0元素均被当做true
#
# 排序
# 跟Python内置的列表类型一样，numpy数组也可以通过sort方法就地排序
# arr = np.random.randn(8)
# print(arr)
# arr.sort()
# print(arr)
# 多维数组可以在任何一个轴向上进行排序，只需将轴编号传给sort即可
# arr = np.random.randn(5, 3)
# print(arr)
# arr.sort(1)
# print(arr)
#
# 顶级方法np.sort返回的是数组的已排序副本，而就地排序则会修改数组本身。
# 计算数组分位数最简单的办法就是对其进行排序，然后选取特定位置的值
# large_arr = np.random.randn(1000)
# large_arr.sort()
# print(large_arr[int(0.05 * len(large_arr))]) #5%分位数
#
#
# 唯一化以及其他的集合逻辑
# numpy提供了一些针对一维ndarray的基本集合运算
# 最常用的是np.unique，找出数组中的唯一值并返回已排序额结果
# names = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
# print(np.unique(names))
# ints = np.array([3, 3, 3, 2, 2, 1, 1, 4, 4])
# print(np.unique(ints))
# 与np.unique等价的纯Python代码比较
# sorted(set(names))
# 另一个函数np.in1d用于测试一个数组中的值在另一个数组中的成员资格，返回一个布尔型数组
# values = np.array([6, 0, 0, 3, 2, 5, 6])
# print(np.in1d(values, [2, 3, 6]))
#
# 数组的集合运算
# 数组的集合运算.png