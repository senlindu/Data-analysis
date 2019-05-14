

# 高级数组输入输出
# 内存映像使你能处理在内存中放不下的数据集
# 内存映像文件时一种将磁盘上的非常大的二进制数据文件当做内存中的数组进行处理的方式
# numpy实现了一个类似于ndarray的memmap对象，它允许将大文件分成小段进行读写，而不是一次性
# 将整个数组读入内存
# memmap也拥有跟普通数组一样的方法
# 基本上只要是能用于ndarray的算法就也能用于memmap

# 使用函数np.memmap并传入一个文件路径、数据类型、形状以及文件模式，即可创建一个新的memmap
# mmap = np.memmap('mymmap', dtype='float64', mode='w+', shape=(10000, 10000))
# print(mmap)
# 对memmap切片将会返回磁盘上的数据的视图
# section = mmap[:5]
# 如果将数据赋值给这些视图：数据会先被缓存在内存中，调用flush即可将其写入磁盘
# section[:] = np.random=randn(5, 10000)
# mmap.flush()
# print(mmap)
# del mmap
# 只要某个内存映像超出了作用域，它就会被垃圾回收器回收，之前对其所做的任何修改
# 都会被写入磁盘
# 当打开一个已经存在的内存映像时，仍然㤇指明数据类型和形状，因为磁盘上的那个文件
# 只是一块二进制数据而已，没有任何元数据
# mmap = np.memmap('mymmap', dtype='float64',shape=(10000, 10000))
# print(mmap)
# 由于内存映像其实就是一个存放在磁盘上的ndarray，所以完全可以使用前面介绍的结构化dtype


# HDF5及其他数组存储方式
# PyTables和h5py这两个Python项目可以将numpy的数组数据存储在高效且可压缩的HDF5格式
# PyTables提供了一些用于结构化数组的高级查询功能，而且还能添加列索引以提升查询速度
# 