import numpy as np
import matplotlib.pyplot as plt

# 用于数组的文件输入输出
# numpy能够读写磁盘上的文本数据或二进制数据
#
#
# 将数组以二进制格式保存到磁盘
# np.load和np.save是读写磁盘数组数据的两个主要函数
# 默认情况下，数组是以未压缩的原始二进制格式保存在扩展名为.npy的文件中的
# arr = np.arange(10)
# np.save('some_array', arr)
# 如果文件路径末尾没有扩展名.npy，则该扩展名会被自动加上，然后就可以通过
# np.load读取磁盘上的数组
# arr = np.load('some_array.npy')
# print(arr)
#
# 通过np.savez可以将多个数组保存到一个压缩文件中，将数组以关键字参数
# 的形式传入即可
# arr = np.arange(10)
# np.savez('arr_archive.npz', a=arr, b=arr)
# 加载.npz文件时，你会得到一个类似字典的对象，该对象会对各个数组进行延迟加载
# arch = np.load('arr_archive.npz')
# print(arch)
# print(arch['b'])
# 
# 存取文本文件
# 从文件中加载文本是一个非常标准的任务
# 主要介绍pandas的read_csv和read_table函数
# 有时，我们需要用np.loadtxt或更加专门化的np.genformtxt将数据加载到普通的numpy数组中
# 这些函数都有许多选项可供使用：指定各种分隔符、针对特定列的转换器函数、
# 需要跳过的行数等。
# 以一个简单的逗号分隔文件（CSV）为例
# arr = np.loadtxt('filename.txt', delimiter=',')
# np.savetxt执行的是相反的操作，将数组写到以某种分隔符隔开的文本文件中
# genfromtxt跟loadtxt差不多，只不过它面向的是结构化数组和缺失数据处理
# 

