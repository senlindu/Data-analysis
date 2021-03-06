

# python解释器
# Python是一种解释型语言，Python解释器是通过"一次执行一条语句"的方式运行程序的
# Python科学计算程序员更趋向于IPython


# 基础知识

# 语言语义
# Python语言的设计特点是重视可读性、简洁性以及明确性

# 缩进，而不是大括号
# 冒号表示一段缩进代码的开始，其后的所有代码都必须缩进相同的量
# Python语言的一个重要特点就是其对象模型的一致性
# 函数的调用需要用到圆括号以及0个或多个参数
# 在Python中对变量赋值时，你其实在创建等号右侧对象的一个引用
# 当你将对象以参数的形式传入函数时，其实只是传入了一个引用而已，不会发生任何复制
# 通过isinstance函数，可以检查一个对象是否是某个特定类型的实例
# isinstance可以接受由类型组成的元组
# Python中的对象通常既有属性又有方法
# 它们可以通过obj.attribute_name这样的语法进行访问
# 还可以利用getattr函数通过名称进行访问
# isiterable()可以返回是否可迭代的结果
# 二元运算符.png
# Python是一种非常严格的语言，几乎在任何时候，计算过程和表达式都是立即求值的
# 字符串和元组是不可变的
# 标准的Python标量类型.png
# 字符串最左边引号的前面加上r，表示所有字符应该按照原本的样子进行解释
# Python内置的datetime模块提供了datetime、date以及time等类型
# strftime方法用于将datetime格式化为字符串
# 字符串可以通过strptime函数转换为datetime对象
# pass是Python中的空操作语句，可以被用在那些没有任何功能的代码块中

# range函数用于产生一组间隔平均的整数
# 可以指定起始值、结束值以及步长等信息
# 对于非常长的范围，建议使用xrange，其参数跟range一样，但它不会预先产生所有的值，并
# 将它们保存到列表中，而是返回一个用于逐个产生整数的迭代器
# Python3 中range始终返回迭代器


# 数据结构和序列

# 元组
# 元组是一种一维的、定长的、不可变的Python对象序列
# 最简单的创建方式是一组逗号隔开的值
# tup = 4, 5, 6
# 在更复杂的表达式中定义元组时，常常需要用圆括号将值围起来
# nested_tup = (4, 5, 6), (7, 8)
# 通过调用tuple，任何序列或迭代器都可以被转换为元组
# print(tuple([4, 0, 2]))
# tup = tuple('string')
# print(tup)
# 元组的元素也可以通过方括号([])进行访问，也是从0开始索引的
# 虽然存储在元组中的对象本身可能是可变的，但一旦创建完毕，存放在各个插槽中的
# 对象就不能再被修改了
# 元组可以通过加号运算符连接起来以产生更长的元组
# 跟列表一样，对一个元组乘以一个整数，相当于是连接该元组的多个副本
# print(('foo', 'bar') * 4)
# 注意，对象本身是不会被复制的，这里涉及的只是它们的引用而已

# 元组拆包
# 如果对元组型变量表达式进行赋值，Python就会尝试将等号右侧的值进行拆包
# tup = (4, 5, 6)
# a, b, c = tup
# print(b)
# 即使是嵌套元组也能被拆包
# 利用该功能可以非常轻松地交换变量名
# 变量拆包功能常用于对元组或列表组成的序列进行迭代
# 另一种常见用法是处理从函数中返回的多个值

# 元组方法
# 由于元组的大小和内存不能被修改，所以其实例方法很少，最有用的是count，
# 用于计算指定值的出现次数



# 列表
# 跟元组相比，列表是变长的，而且其内容也是可以修改的
# 可以通过方括号或list函数进行定义
# 列表和元组在语义上是差不多的，都是一维序列，因此它们在许多函数中是可以互换的

# 添加和移除元素
# 通过append方法，可以将元素添加到列表的末尾
# 利用insert可以将元素插入到列表的指定位置
# b_list.insert(1, 'red')
# insert的逆运算是pop，用于移除并返回指定索引处的元素
# b_list.pop(2)
# remove用于按值删除元素，找到第一个符合要求的值然后将其从列表中删除
# b_list.remove('foo')
# 通过in关键字，可以判断列表中是否含有某个值
# 注意，判断列表中是否含有某个值的操作比字典和集合慢的多，因为进行线性扫描，
# 另外两个则可以瞬间完成判断(基于哈希表)

# 合并列表
# 跟元组一样，用加号将两个列表加起来即可实现合并
# 对一个已定义的列表，可以用extend方法一次性添加多个元素
# x = [4, None, 'foo']
# x.extend([7, 8, (2, 3)])
# 注意，列表的合并是一种相当费资源的操作，因为必须创建一个新列表并将所有对象复制过去
# 而用extend将元素附加到现有列表，就会好很多

# 排序
# 调用列表的sort方法可以实现就地排序
# sort有几个不错的选项，一个是次要排序键，即一个能够产生可用于排序的值的函数
# 例如，通过长度对一组字符串进行排序
# b = ['saw', 'small', 'He', 'foxes', 'six']
# b.sort(key=len)
# print(b)

# 二分搜索及维护有序列表
# 内置的bisect模块实现了二分查找以及对有序列表的插入操作
# bisect.bisect可以找出新元素应该被插入到哪个位置才能保持原列表的有序性，而
# bisect.insort则确实地将新元素插入到那个位置上去

# 切片
# 通过切片标记法，可以选取序列类型的子集，其基本形式由索引运算符以及传入其中的
# start:stop构成
# 切片还可以被赋值为一段序列
# seq[3:4] = [6, 3]
# 由于start索引处的元素是被包括在内的，而stop索引处的元素是未被包括在内的，
# 所以结果中的元素数量是stop-start
# start或stop都是可以省略的，此时它们分别默认序列的起始处和结尾处
# 负数索引从序列的末尾开始切片
# 还可以在第二个冒号后面加上步长，比如每隔一位取出一个元素
# seq[::2]
# 使用-1是一个很巧妙的方法，可以实现列表或元组的反序

# 内置的序列函数
# enumerate
# 在对一个序列进行迭代时，常常需要跟踪当前项的索引
# i = 0
# for value in collection:
#     i += 1
# 由于这种事情很常见，所以就内置了一个enumerate函数，可以逐个返回序列的(i, value)元组
for i, value in enumerate(collection):
	pass
# 在对数据进行索引时，enumerate还有一种不错的使用模式，即求取一个将序列值(假定是唯一的)
# 映射到其所在位置的字典
# some_list = ['foo', 'bar', 'baz']
# mapping = dict((v, i) for i, v in enumerate(some_list))
# print(mapping)

# sorted
# sorted函数可以将任何序列返回一个新的有序列表
# sorted([])
# 常常将sorted和set结合起来使用以得到一个由序列中的唯一元素组成的有序列表

# zip
# zip用于将多个序列(列表、元组)中的元素"配对"，从而产生一个新的元组列表
# zip可以接受任意数量的序列，最终得到的元组数量由最短的序列决定
# zip最常见的用法是同时迭代多个序列，还可以结合enumerate一起使用
for i, (a, b) in enumerate(zip(seq1, seq2)):
	print('%d:%s, %s' % (i, a, b))
# 对于已压缩的序列，zip还有一个很巧妙的用法，即对该序列进行解压
# 其实就是将一组行转换为一组列
pitchers = [('Nolan', 'Ryan'), ('Roger', 'Clemens'), ('Schilling', 'Curt')]
first_name, last_name = zip(*pitchers)

# reversed
# reversed用于按逆序迭代序列中的元素


# 字典
# 更常见的名字是哈希映射或相联数组
# 是一种大小可变的键值对集，其中的键和值都是Python对象
# 创建字典的方式之一是：使用大括号{}并用冒号分隔键和值
# 访问(插入以及设置)元素的语法跟列表和元组是一样的
# 可以用in判断字典中是否存在某个键
# 使用del关键字或pop方法，可以删除值
# keys和values方法分别用于获取键和值的列表，虽然键值对没有特定的顺序，但这两个函数
# 会以相同的顺序输出键和值
# Python3中这两个函数返回的是迭代器
# 利用update方法，一个字典可以被合并到另一个字典中去

# 从序列类型创建字典
# 可以直接用dict类型函数直接处理二元元组列表

# 默认值
# 其实dict的get和pop方法可以接受一个可供返回的默认值
# value = some_dict.get(key, default_value)
# 如果key不存在，则get默认返回None，而pop则会引发一个异常
# 在设置值的时候，常常会将字典中的值处理成别的集类型(比如列表)
# setfault方法
# 内置的collections模块有一个叫做defaultdict的类，它可以使该过程更简单
# 传入一个类型或函数即可创建出一个defaultdict
# defaultdict的初始化器只需要一个可调用对象，并不需要明确的类型

# 字典键的有效类型
# 字典的值可以是任何Python对象，但键必须是不可变对象
# 通过hash函数，你可以判断某个对象是否是可哈希的
# 如果要将列表当做键，最简单的办法就是将其转换成元组


# 集合
# 集合是由唯一元素组成的无序集，你可以将其看成是只有键而没有值的字典
# 集合的创建方式有二：set函数或用大括号包起来的集合字面量
# 集合支持各种数学集合运算，如并、交、差以及对称差
# 还可以判断issubset和issuperset判断一个集合是否是另一个集合的子集或超集
# Python的集合运算.png


# 列表、集合以及字典的推导式
# 只需一条简洁的表达式，即可对一组元素进行过滤，并对得到的元素进行转换变形
# [expr for val in collection if condition]
# 过滤器条件可以省略，只留下表达式
# 集合字典的推导式是该思想的一种自然延伸，语法差不多，只不过产生的是集合和字典而已
# 字典的推导式的基本形式如下：
# dict_comp = {key-expr:value-expr for value in collection if condition}
# 集合推导式与列表推导式非常相似，唯一的区别就是它用的是花括号而不是方括号
# set_comp = {expr for value in collection if condition}
# 字典还可以这样构造
# loc_mapping = dict((val, idx) for idx, val in enumerate(strings))


# 嵌套列表推导式
# 假设有一个由男孩名列表和女孩名列表组成的列表
# 假设找出带有两个以上含有字母X的名字，并将他们放入新列表
# 可以使用简单的for循环实现，也可以使用推导式
# result = [name for names in all_data for name in names if name.count('e') >= 2]
# 推导式中for的部分是按嵌套顺序排列的，而过滤条件则还跟之前一样放在后面


# 函数
# 函数可以有一些位置参数和一些关键字参数
# 关键字参数通常用于指定默认值或可选参数
# 函数参数的主要限制在于：关键字参数必须位于位置参数之后
# 函数可以返回多个值
# 函数可以赋值给一个变量，也可以返回字典
# 可以将需要在一组给定字符串上执行的所有运算做成一个列表
# 还可以将函数用作其他函数的参数

# 闭包：返回函数的函数
# 闭包就是由其他函数动态生成并返回的函数，其关键性质是，被返回的函数可以访问
# 其创建者的局部命名空间中的变量
def make_closure(a):
	def closure():
		print('I know the secret: %d' % a)
	return closure
# 闭包和标准Python函数之间的区别在于，即使其创建者已经执行完毕，闭包仍能继续访问
# 其创建者的局部命名空间
# 虽然闭包的内部状态一般都是静态的，但也允许使用可变对象
# 但要注意，虽然可以修改任何内部状态对象，但不能绑定外层函数作用域中的变量
# 一个解决办法是，修改字典或列表，而不是绑定变量

# 柯里化：部分参数应用
# 通过"部分参数应用"从现有函数派生出新函数的技术
# 内置的functools模块可以用partial函数将此过程简化
# add_five = partial(add_numbers, 5)

# 生成器
# 生成器是构造新的可迭代对象的一种简单方式
# 函数执行之后，生成器会以延迟的方式返回一个值序列
# 要创建一个生成器，只需将函数中的return替换为yeils即可
# 直到你从该生成器中请求元素，它才会开始执行其代码

# 生成器表达式
# 生成器表达式时构造生成器的最简单方式
# 创建方式为，把列表推导式两端的方括号改为圆括号

# itertools模块
# 这个模块中有一组用于许多常见数据算法的生成器
# 常用itertools函数.png

# 文件和操作系统
# 使用内置的open函数以及一个相对或绝对的文件路径
# 默认情况下，文件是以只读模式('r')打开的
# Python文件模式.png
# 要将文本写入文件，可以使用该文件的write或writelines方法
# 重要的Python文件方法或属性.png