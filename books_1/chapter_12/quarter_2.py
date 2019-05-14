

# 高级数组操作

# 数组重塑
# 从一个形状转换为另一个形状，只需向数组的实例方法reshape传入一个表示新形状的元组即可实现该目的
# arr = np.arange(8)
# print(arr)
# print(arr.reshape((4, 2)))
# 多维数组也能被重塑
# print(arr.reshape((4, 2)).reshape((2, 4)))
# 作为参数的形状的其中一维可以是-1， 它表示维度的大小由数据本身推断而来
# arr = np.arange(15)
# print(arr.reshape((5, -1)))
# 由于数组的shape属性是一个元组，因此它也可以被传入reshape
# other_arr = np.ones((3, 5))
# print(other_arr.shape)
# print(arr.reshape(other_arr.shape))
# 与reshape将一维数组转换为多维数组的运算过程相反的运算通常称为扁平化或散开
# arr = np.arange(15).reshape((5, 3))
# print(arr)
# print(arr.ravel)
# 如果没有必要，ravel不会产生源数据的副本
# flatten方法的行为类似于ravel，只不过它总是返回数据的副本
# print(arr.flatten())
# 数组可以被重塑或散开为别的顺序


# C和Fortran顺序
# numpy允许你更为灵活地控制数据在内存中的布局
# 默认情况下，numpy数组是按行优先顺序创建的、在空间方面，这就意味着，对一个二维数组，
# 每行中的数据项是被存放在相邻内存位置上的
# 另一种顺序是列优先顺序，意味着每列中的数据项是被存放在杏林内存位置上的

# 行和列优先顺序又分别被称为C和Fortran顺序

# 像reshape和reval这样的函数，都可以接受一个表示数组数据存放顺序的order参数
# 一般可以是'C'或'F'
# arr = np.arange(12).reshape((3, 4))
# print(arr)
# print(arr.ravel())
# print(arr.ravel('F'))
# 二维或更高维数组的重塑过程比较令人费解
# C和Fortran顺序的关键区别就是维度的行进顺序
# 1、C/行优先顺序：先经过更高的维度(例如，轴1会先于轴0被处理)
# 2、Fortran/列优先顺序：后经过更高的维度(例如，轴0会先于轴1被处理)


# 数组的合并和拆分
# numpy.concatenate可以被指定轴将一个由数组组成的序列(如元组、列表等)连接到一起
# arr1 = np.array([[1, 2, 3], [4, 5, 6]])
# arr2 = np.array([[7, 8, 9], [10, 11, 12]])
# print(np.concatenate([arr1, arr2], axis=0))
# print(np.concatenate([arr1, arr2], axis=1))
# C-F重塑.png
# 对于常见的连接操作，numpy提供了一些比较方便的方法(如vstack和hstack)
# print(np.vstack((arr1, arr2)))
# print(np.hstack((arr1, arr2)))
# 与此相反，split用于将一个数组沿指定轴拆分为多个数组
# arr = randn(5, 2)
# print(arr)
# first, second, third = np.split(arr, [1, 3])
# print(first)
# print(second)
# print(third)


# 数组连接函数
# 数组连接函数.png


# 堆叠辅助类： r_和c_
# numpy命名空间中有两个特殊的对象--r_和c_，它们可以使数组的堆叠操作更为简洁
# arr = np.arange(6)
# arr1 = arr.reshape((3, 2))
# arr2 = randn(3, 2)
# print(np.r_[arr1, arr2])
# print(np.c_[np.r_[arr1, arr2], arr])
# 此外，还可以将切片翻译为数组
# print(np.c_[1:6, -10:-5])


# 元素的重复操作:tile和repeat
# numpy中很少需要对数组进行重复，主要是因为广播能更好地满足该需求
# 对数组进行重复以产生更大数组的工具主要是repeat和tile这两个函数
# repeat会将数组中的各个元素重复一定次数，从而产生一个更大的数组
# arr = np.arange(3)
# print(arr.repeat(3))
# 默认情况下，如果传入的是一个整数，则各元素就都会重复那么多次
# 如果传入的是一组整数，则各元素就可以重复不同的次数
# print(arr.repeat([2, 3, 4]))
# 对于多维数组，还可以让它们的元素沿指定轴重复
# arr = randn(2, 2)
# print(arr)
# print(arr.repeat(2, axis=0))
# 注意，如果没有设置轴向，则数组会被扁平化，可能不是你想要的结果
# 在对多维数组进行重复时，也可以传入一组整数，这样就会使各切片重复不同的次数
# print(arr.repeat([2, 3], axis=0))
# print(arr.repeat([2, 3], axis=1))
# tile的功能是沿指定轴向堆叠数组的副本
# print(arr)
# print(np.tile(arr, 2))
# 第二个参数是瓷砖的数量
# 对于标量，瓷砖是水平铺设的，而不是垂直铺设的
# 它可以是一个表示"铺设"布局的元组
# print(arr)
# print(np.tile(arr, (2, 1)))
# print(np.tile(arr, (3, 2)))


# 花式索引的等价函数:take和put
# 获取和设置数组子集的一个办法是通过整数数组使用花式索引
# arr = np.arange(10) * 100
# inds = [7, 1, 2, 6]
# print(arr[inds])
# ndarray有两个方法专门用于获取和设置单个轴向上的选区
# print(arr.take(inds))
# print(arr.put(inds, 42))
# print(arr)
# arr.put(inds, [40, 41, 42, 43])
# print(arr)
# 要在其他轴上使用take，只需传入axis关键字即可
# inds = [2, 0, 2, 1]
# arr = randn(2, 4)
# print(arr)
# print(arr.take(inds, axis=1))
# put不接受axis参数，只会在数组的扁平化版本上进行索引