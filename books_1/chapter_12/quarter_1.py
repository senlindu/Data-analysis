


# numpy高级应用

# ndarray对象的内部机理
# numpy的ndarray提供了一种将同质数据块(可以是连续或跨越的)解释为多维数据对象的方式
# 数据类型决定了数据的解释方式，比如浮点数、整数、布尔值等

# ndarray如此强大的部分原因是所有数组对象都是数据块的一个跨度视图
# ndarray不只是一块内存和一个dtype，还有跨度信息，这使得数组能以各种步幅在内存中移动
# ndarray内部由以下内容组成：
# 1、一个指向数组(一个系统内存块)的指针
# 2、数据类型或dtype
# 3、一个表示数组形状的元组，例如一个10*5的数组，其形状为(10,5)
# 4、一个跨度元组，其中的整数指的是为了前进到当前维度下一个元素需要跨过的字节数
# 例如，一个典型的3*4*5的float64数组，其跨度为(160, 40, 8)
# np.ones((3, 4, 5), dtype=np.float64).strides
# 虽然numpy用户很少对数组的跨度信息感兴趣，但它们却是构建非复制式数组视图的重要因素
# 跨度甚至可以是负数，这样会使数组在内存中向后移动，比如在切片obj[::-1]或obj[:, ::-1]中就是这样的

# ndarray内部结构.png


# numpy数据类型体系
# dtype都有一个超类(np.integer和np.floating)，可以跟np.issubdtype函数结合使用
# ints = np.ones(10, dtype=np.uint16)
# floats = np.ones(10, dtype=np.float32) 
# print(np.issubdtype(ints.dtype, np.integer))
# print(np.issubdtype(floats.dtype, np.floating))
# 调用dtype的mro方法即可查看其所有的父类
# print(np.float64.mro())

# numpy的dtype体系.png
