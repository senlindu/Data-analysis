

# 结构化和记录式数组
# 结构化数组是一种特殊的ndarray，其中的各个元素可以被看做C语言中的结构体或SQL表中
# 带有多个命名字段的行
# dtype = [('x', np.float64), ('y', np.int32)]
# sarr = np.array([(1.5, 6), (np.pi, -2)], dtype=dtype)
# print(sarr)
# 定义结构化dtype的方式有很多，最典型的办法是元组列表，各元组的格式为
# (field_name, field_data_type)
# 数组的元素就成了元组式的对象，该对象中各个元素可以像字典那样进行访问
# print(sarr[0])
# print(sarr[0]['y'])
# 字段名保存在dtype.names属性中，在访问结构化数组的某个字段时，返回的是该数据的视图，
# 所以不会发生数据复制
# print(sarr['x'])


# 嵌套dtype和多维字段
# 在定义结构化dtype时，你可以再设置一个形状(可以是一个整数，也可以是一个元组)
# dtype = [('x', np.int64, 3), ('y', np.int32)]
# arr = np.zeros(4, dtype=dtype)
# print(arr)
# 在这种情况下，各个记录的x字段所表示的是一个长度为3的数组
# print(arr[0]['x'])
# 访问arr['x']即可得到一个二维数组，而不是前面那个例子中的一维数组
# print(arr['x'])
# 这使得我们能用单个数组的内存块存放复杂的嵌套结构
# 嵌套dtype
# dtype = [('x', [('a', 'f8'), ('b', 'f4')]), ('y', np.int32)]
# data = np.array([((1, 2), 5), ((3, 4), 6)], dtype=dtype)
# print(data['x'])
# print(data['y'])
# print(data['x']['a'])
# 可变形状的字段和嵌套记录是一种非常强大的功能
# pandas的DataFrame并不直接支持该功能，但它的分层索引机制跟这个差不多


# 为什么要用结构化数组
# 跟pandas的DataFrame相比，numpy的结构化数组是一种相对较低级的工具
# 它可以将单个内存块解释为带有任意复杂嵌套列的表格型结构
# 由于数组中的每个元素在内存中都被表示为固定的字节数，所以结构化数组能够提供
# 非常快速高效的磁盘数据读写、网络传输等功能
# 另一种常见用法是，将数据文件写成定长记录字节流，这是C和C++代码中常见的数据序列化手段
# 知足要知道文件的格式，就可以用np.fromfile将数据读入内存


# 结构化数组操作：numpy.lib.recfunctions
# 适用于结构化数组的函数没有DataFrame那么多
# numpy模块numpy.lib.recfunctions中有一些用于增删字段或执行基本连接运算的工具
# 这些工具，一般都需要创建一个新数组以便对dtype进行修改
# 