

# 广播
# 广播指的是不同形状的数组之间的算术运算的执行方式
# 它是一种非常强大的功能，但也容易令人误解
# 将标量值跟数组合并时就会发生最简单的广播
# arr = np.arange(5)
# print(arr)
# print(arr * 4)
# 在这个乘法运算中，标量值4被广播到了其他所有的元素上
# 我们通过减去列平均值的方式对数组的每一列进行距平化处理
# arr = randn(4, 3)
# print(arr.mean(0))
# demeaned = arr - arr.mean(0)
# print(demeaned)
# print(demeaned.mean(0))
# 用广播的方式对行进行距平化处理会稍微麻烦一些
# 只要遵循一定的规则，低纬度的值是可以被广播到数组的任意维度的
# 一维数组在轴0上的广播.png

# 广播的原则 
# 如果两个数组的后缘维度(即从末尾开始算起的维度)的周长度相符或其中一方的长度为1，则认为它们
# 是广播兼容的。广播会在缺失和长度为1的维度上进行


# 假设对各行减去那个平均值，由于arr.mean(0)的长度为3， 所以它可以在轴轴0向上进行传播
# 因为arr的后缘维度是3， 所以它们是兼容的
# 根据该原则，要在轴1向上做减法(各行减去行平均值)，较小的那个数组的形状必须是(4，1)
# print(arr)
# row_means = arr.mean(1)
# row_means.reshape((4, 1))
# demeaned = arr - row_means.reshape((4, 1))
# print(demeaned.mean(1))
# 二维数组在轴1上的广播.png
# 三维数组在轴0上的广播.png


# 沿其他轴向广播
# 高维度数组的广播更难以理解，实际上它也是遵循广播原则的
# print(arr - arr.mean(1))
# 人们经常需要通过算术运算过程将较低维度的数组在除0轴以外的其他轴向上广播
# 根据广播的原则，较小的数组的"广播维"必须为1
# 在上面那个行距平化的例子中，意味着要将行平均值的形状变成(4, 1)而不是(4,)
# print(arr - arr.mean(1). reshape((4, 1)))
# 对于三维的情况，在三维的任何一维上广播其实也就是将数据重塑为兼容的形状而已
# 能在该三维数组上广播的二维数组.png
# 于是就有了一个非常普遍的问题，即专门为了广播而添加一个长度为1的新轴
# 虽然reshape是一个办法，但插入轴需要构造一个表示新形状的元组
# numpy数组提供了一种通过索引机制插入轴的特殊语法
# 通过特殊的np.newaxis属性以及"全"切片来插入新轴
# arr = np.zeros((4, 4))
# arr_3d = arr[:, np.newaxis, :]
# print(arr_3d.shape)
# arr_1d = np.random.normal(size=3)
# print(arr_1d[:, np.newaxis])
# print(arr_1d[np.newaxis, :])
# 如果我们有一个三维数组，并希望对轴2进行距平化，只需编写下面的代码
# arr = randn(3, 4, 5)
# depth_means = arr.mean(2)
# print(depth_means)
# demeaned = arr- depth_meansp[:, :, np.newaxis]
# print(demeaned.mean(2))
# 在对指定轴进行距平化时，有既通用又不牺牲性能的方法，需要一些索引方面的技巧
def demean_axis(arr, axis=0):
	means = arr.mean(axis)
	# 下面这些一般化的东西类似于N维的[:, :, np.newaxis]
	# indexer = [slice(None)] * arr.ndim
	# indexer[axis] = np.newaxis
	# return arr - means[indexer]


# 通过广播设置数组的值
# 算术运算所遵循的广播原则同样也适用于通过索引机制设置数组值的操作
# arr = np.zeros((4, 3))
# arr[:] = 5
# print(arr)
# 用一个一维数组设置目标数组的各列
# 保证形状兼容即可
# col = np.array([1.28, -0.42, 0.44, 1.6])
# arr[:] = col[:, np.newaxis]
# print(arr)
# arr[:2] = [[-1.37], [0.509]]
# print(arr)
# 