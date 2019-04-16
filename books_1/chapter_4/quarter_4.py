import numpy as np
from numpy.linalg import inv, qr

# 线性代数
# 线性代数（矩阵乘法、矩阵分解、行列式以及其他方阵数学等）是任何数组库的重要组成部分
# numpy提供了一个用于矩阵乘法的dot函数（既是一个数组方法也是numpy命名空间中的一个函数）
# x = np.array([[1., 2., 3.], [4., 5., 6]])
# y = np.array([[6., 23.], [-1, 7], [8, 9]])
# print(x)
# print(y)
# print(x.dot(y)) # 相当于np.dot(x, y)
#
# 一个二维数组跟一个大小合适的一维数组的矩阵点积运算之后将得到一个一维数组
# print(np.dot(x, np.ones(3)))
#
# numpy.linalg中有一组标准的矩阵分解运算以及诸如求逆和行列式之类的东西
# X = np.random.randn(5, 5)
# mat = X.T.dot(X)
# print(inv(mat))
# print(mat.dot(inv(mat)))
# q, r = qr(mat)
# print(q)
# print(r)

# 常用的numpy.linalg函数
# numpy-linalg.png
#
# 随机数生成
# numpy.random模块对Python内置的random进行了补充，增加了一些用于高效
# 生成多种概率分布的样本值的函数
# 你可以使用normal来得到一个标准正态分布的4*4样本数组
# samples = np.random.normal(size=(4, 4))
# print(samples)
# 而Python内置的random模块则只能一次生成一个样本值
# 如果需要产生大量样本值，numpy.random快乐不止一个数量级
# IPYTHON
# from random import normalvariate
# N = 1000000
# %timeit samples = [normalvariate(0, 1) for _ in xrange(N)]
# %timeit np.random.normal(size=N)
# 
# numpy.random函数
# numpy-random_1.png
# numpy-random_2.png
