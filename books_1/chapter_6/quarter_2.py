import numpy as np
import pandas as pd


# 二进制数据格式
# 实现数据的二进制格式存储最简单的办法之一是使用Python内置的pickle序列化
# pandas对象都有一个用于将数据以pickle形式保存到磁盘上的save方法
frame = pd.read_csv('e:/examples/ex1.csv')
# print(frame)
# save改为to_pickle
# frame.to_pickle('frame_pickle')
# 也可以通过另一个很好用的pickle函数pandas.load将数据读回到Python
# load给为read_pickle
# print(pd.read_pickle('frame_pickle'))


# 使用HDF5格式
# 很多工具多能实现高效读写磁盘上以二进制格式存储的科学数据
# HDF5就是其中一个流行的工业级库，是一个C库，带有许多语言的接口
# HDF5中的HDF指的是层次型数据格式
# 每个HDF5文件都含有一个文件系统式的节点结构，使你能够存储多个
# 数据集并支持元数据
# HDF5支持多种压缩器的即时压缩，还能更高效地存储重复模式数据
# 对于那些非常大的无法直接放入内存的数据集，HDF5就是不错的选择，
# 可以高效地分块读写

# python中的HDF5库由两个接口(PyTables和h5py),它们各自采取了不同的问题
# 解决方式
# h5py提供了一种直接而高级的HDF5 API访问接口，而PyTables则抽象了HDF5的
# 许多细节以提供多种灵活的数据容器、表索引、查询功能以及对核外计算技术的
# 某些支持

# pandas有一个最小化的类似于字典的HDFStore类，通过PyTables存储pandas对象
store = pd.HDFStore('mydata.h5')
store['obj1'] = frame
store['obj1_col'] = frame['a']
print(store)
# HDF5中的对象可以通过与字典一样的方式进行获取
print(store['obj1'])
# 如果需要处理海量数据，可以好好研究下PyTables和h5py
# 由于许多数据分析问题都是IO密集型而不是CPU密集型，利用HDF5这样
# 的工具能显著提升应用程序的效率
# 警告：HDF5不是数据库。最适合一次写多次读的数据集
# 如果同时发生多个写操作，文件就可能会被破坏


# 读取Microsoft Excel文件
# pandas的ExcelFile类支持读取存储在Excel 2003（或更高版本）
# 的表格型数据
# 由于ExcelFile用到了xlrd和openpyxl包，所以需要先安装它们
# 通过传入一个xsl或xlsx文件的路径即可创建一个ExcelFile实例
    xls_file = pd.ExcelFile('data.xls')
    # 存放在某个工作表中的数据可以通过parse读取到DataFrame中
    table = xls_file.parse('Sheet1')
