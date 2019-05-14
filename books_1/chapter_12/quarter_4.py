

# ufunc高级应用

# ufunc实例方法
# numpy的各个二元ufunc都有一些用于执行特定矢量化运算的特殊方法

# reduce接受一个数组参数，并通过一系列的二元运算对其值进行聚合(可指明轴向)
# 例如，对数组中各个元素求和
# arr = np.arange(10)
# print(np.add.reduce(arr))
# print(arr.sum())
# 起始值取决于ufunc(对于add的情况，就是0)
# 如果设置了轴号，约简运算就会沿该轴向执行
# 使用np.logical_and检查数组各行中的值是否是有序的
# arr = randn(5, 5)
# print(arr[::2].sort(1))
# print(arr[:, :-1] < arr[:, 1:])
# print(arr.logical_and.reduce(arr[:, :-1] < arr[:, 1:], axis=1))
# logical_and.reduce跟all方法是等价的
# accumulate跟reduce的关系就像cumsum跟sum的关系那样，它产生一个跟原数组大小相同的中间
# "累计"值数组
# arr = np.arange(15).reshape((3, 5))
# print(np.add.accumulate(arr, axis=1))
# outer用于计算两个数组的叉集
# arr = np.arange(3).repeat([1, 2, 2])
# print(arr)
# print(np.multipy.outer(arr, np.arange(5)))
# outer输出结果的维度是两个输入数据的维度之和
# result = np.subtract.outer(randn(3, 4), randn(5))
# print(result.shape)
# 最后一个方法reduceat用于计算"局部约简"，其实就是一个对数据各切片进行聚合的groupby运算
# 虽然其灵活性不如pandas的groupby功能，但在适当情况下运算会非常快
# 它接受一组用于指示如何对值进行拆分和聚合的"面元边界"
# arr = np.arange(10)
# print(np.add.reduce(arr, [0, 5, 8]))
# 最终结果是在arr[0:5], arr[5:8]以及arr[8:]上执行的约简
# arr = np.multiply.outer(np.arange(4), np.arange(5))
# print(arr)
# print(np.add.reduceat(arr, [0, 2, 4], axis=1))
# ufunc方法.png


# 自定义ufunc
# 有两个工具可以让你将自定义函数像ufunc那样使用
# numpy.frompyfunc接受一个Python函数以及两个分别表示输入输出参数数量的整数
def add_elements(x, y):
	return x + y
# add_them = np.frompyfunc(add_elements, 2, 1)
# print(add_them(np.arange(8), np.arange(8)))
# 用frompyfunc创建的函数总是返回Python对象数组，不是很方便
# 另一个办法，即numpy.vectorize，在类型推断方面更智能一些
# add_them = np.vectorize(add_elements, otypes=[np.float64])
# print(add_them(np.arange(8), np.arange(8)))
# 这两个函数非常慢，因为在计算每个元素时都要执行一次Python函数调用
# arr = randn(10000)
# %timeit print(add_them(arr, arr))
# 