from numpy import ndarray, float64_t

# 性能建议
# 需要注意的事项
# 1、将Python循环和条件循环转换为数组运算和布尔数组运算
# 2、尽量使用广播
# 3、避免复制数据，尽量使用数组视图(即切片)
# 4、利用ufunc及其各种方法
# 如果单用numpy无论如何都达不到所需的性能指标，就可以考虑一下用C、Fortran或Cython

# 连续内存的重要性
# 运算过程中访问连续内存块一般是最快的，，因为内存子系统会将适当的内存块缓存到
# 超高速的L1或L2 CPU Cache中
# 一个数组的内存布局是连续的，就是说元素是以它们在数组中出现的顺序存储在内存中的
# 默认情况下，numpy数组是以C型连续的方式创建的
# 通过ndarray的flags属性即可查看这些信息
# arr_c = np.ones((1000, 1000), order='C')
# arr_f = np.ones((1000, 1000), order='F') 
# print(arr_c.flags)
# print(arr_f.flags)
# print(arr_f.flags.f_contiguous)
# 对两个数组的行进行求和计算，理论上，arr_c会比arr_f快，因为arr_c的行在内存中是连续的
# %timeit arr_c.sum(1)
# %timeit arr_f.sum(1)
# 如果数组的内存顺序不符合你的要求，使用copy并传入'C'或'F'即可解决该问题
# arr_f.copy('C').flags
# 注意，在构造数组的视图时，其结果不一定是连续的
# arr_c[:50].flags.contiguous
# print(arr_c[:, :50].flags)


# 其他加速手段：Cython、f2py、C
# Cython项目实现的代码运行速度很快(可能需要与C或C++库交互，但无需编写纯粹的C代码)
def sum_elements(ndarray[float64_t arr]):
	cdef Py_ssize_t i, n = len(arr)
	cdef float64_t result = 0
	for i in range(n):
		result += arr[i]
	return result
# Cython处理这段代码时，先将其翻译为C代码，然后编译这些C代码并创建一个Python扩展
# Cython是一种诱人的高性能计算方式，因为编写Cython代码只比编写纯Python代码多花一
# 点时间而已，而且还能跟numpy紧密结合
# 一般的工作流程是，得到能在Python中运行的算法，然后再将其翻译为Cython
# 