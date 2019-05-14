

# numpy的matrix类
# numpy的线性代数语法比较繁琐，其中一个原因是，矩阵操作需要用到numpy.dot
# X = np.array([],[],[],[])
# print(X[:, 0])
# y = X[:, :1]
# print(X)
# print(y)
# print(np.dot(y.T, np.dot(X, y)))
# numpy提供了一个matrix类，其索引行为更像MATLAB，单行或列会以二维形式返回，且使用星号(*)
# 的乘法直接就是矩阵乘法
# Xm = np.matrix(X)
# ym = Xm[:, 0]
# print(Xm)
# print(ym)
# print(ym.T * Xm * ym)
# matrix还有一个特殊的属性I，其功能是返回矩阵的逆
# print(Xm.I * I)
# 不建议使用numpy.matrix替代正规的ndarray，因为它们的应用面较窄
# 对于个别带有大量线性代数运算的函数，可以将函数转换为matrix类型，然后
# 在返回之前用np.asarray(不会复制任何数据)将其转换回正规的ndarray
# 