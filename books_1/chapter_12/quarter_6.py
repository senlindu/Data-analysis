

# 更多有关排序的话题
# 跟Python内置的列表一样，ndarray的sort实例方法也是就地排序，
# 也就是说，数组内容的重新排列是不会产生新数组的
# arr = randn(6)
# arr.sort()
# print(arr)
# 如果目标数组只是一个视图，则原始数组将会被修改
# arr = randn(3, 5)
# print(arr)
# arr[:, 0].sort()
# print(arr)
# 相反，numpy.sort会为原数组创建一个已排序副本，它所接受逇参数跟ndarray.sort一样
# arr = randn(5)
# print(arr)
# np.sort(arr)
# print(arr)
# 这两个排序方法都可以接受一个axis参数，以便沿指定轴向对各块数据进行单独排序
# arr = randn(3, 5)
# print(arr)
# arr.sort(axis=1)
# print(arr)
# 这两个排序方法都不可以被设置为降序
# values[::-1]可以返回一个反序的列表，对ndarray也是如此
# print(arr[:, ::-1])


# 间接排序：argsort和lexsort
# 根据一个或多个键对数据集进行排序
# values = np.array([5, 0, 1, 3, 2])
# indexer = values.argsort()
# print(indexer)
# print(values[indexer])
# 根据数组的第一行对其进行排序
# arr = randn(3, 5)
# arr[0] = values
# print(arr)
# print(arr[:, arr[0].argsort()])
# lexsort跟argsort差不多，只不过它可以一次性对多个键数组执行间接排序(字典序)
# first_name = np.array(['Bob', 'Steve', 'Bill', 'Barbara'])
# last_name = np.array(['Jones', 'Arnold', 'Arnold', 'Jones', 'Walters'])
# sorter = np.lexsort((first_name, last_name))
# print(zip(last_name[sorter], first_name[sorter]))
# lexsort键的应用顺序是从最后一个传入的算起


# 其他排序算法
# 稳定的排序算法会保持等价元素的相对位置
# 对于相对位置具有实际意义的那些间接排序而言，这一点非常重要
# values = np.array(['2:first', '2:second', '1:first', '1:second', '1:third'])
# key = np.array([2, 2, 1, 1, 1])
# indexer = key.argsort(kind='mergesort')
# print(indexer)
# print(values.take(indexer))
# mergesort是唯一的稳定排序，保证有O(nlogn)的性能(空间复杂度)，但是其平均性能比默认的
# quicksort要差
# 数组排序算法.png


# numpy.searchsorted：在有序数组中查找元素
# searchsorted是一个在有序数组上执行二分查找的数组方法，只要将值插入到它返回的
# 那个位置就能维持数组的有序性
# arr = np.array([0, 1, 7, 12, 15])
# print(arr.searchsorted(9))
# print(arr.searchsorted([0, 8, 11, 16]))
# 对于元素0，searchsorted会返回0
# 这是因为其默认行为是返回相等值组的左侧索引
# arr = np.array([0, 0, 0, 1, 1, 1, 1])
# print(arr.searchsorted([0, 1]))
# print(arr.searchsorted([0, 1], side='right'))
# searchsorted的另一个用法， 假设我们有一个数据数组，还有一个表示面元边界的数组
# 我们希望用它将数据数组拆分开
# data = np.floor(np.random.uniform(0, 1000, size=50))
# bins = np.array([0, 100, 1000, 5000, 10000])
# print(data)
# 为了得到各数据点所属区间的编号，可以直接使用searchsorted
# labels = bins.searchsorted(data)
# print(labels)
# 通过pandas的groupby使用该结果即可非常轻松地对原数据集进行拆分
# print(Series(data).groupby(labels).mean())
# 注意，其实numpy的digitize函数也可用于计算这种面元编号
# print(np.digitize(data, bins))
# 