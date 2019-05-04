import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import re

# 字符串操作
# Python能够成为流行的数据处理语言，部分原因是其简单易用的字符串和文本处理功能
# 大部分文本运算都直接做成了字符串对象的内置方法
# 对于更复杂的模式匹配和文本操作，则可能需要用到正则表达式，
# pandas对此进行了加强，使你能够对整组数据应用字符串表达式和正则表达式，而且能处理烦人的缺失数据


# 字符串对象方法
# 对于大部分字符串处理应用而言，内置的字符串方法已经能够满足要求了
# 以逗号分隔的字符串可以用split拆分成数段
# val = 'a,b,   guido'
# print(val.split(','))
# split常常结合strip（用于修剪空白符（包括换行符））一起使用
# pieces = [x.strip() for x in val.split(',')]
# print(pieces)
# 利用加法，可以将这些子字符串以双冒号分隔符的形式连接起来
# first, second, third = pieces
# print(first + '::' + second + '::' + third)
# 但这种方式并不是很实用
# 一种更快更符合Python风格的方法是，向字符串“::”的join方法传入一个列表或元组
# print('::'.join(pieces))
# 另一类方法关注的是子串定位
# 检测子串的最佳方式是利用Python的in关键字(当然还可以使用index和find)
# print('guido' in val)
# print(val.index(','))
# print(val.find(':'))
# 注意find和index的区别：如果找不到字符串，index将会引发一个异常（而不是返回-1）
# val.index(':')
# 此外还有一个count函数，它可以返回指定子串的出现次数
# print(val.count(','))
# replace用于将指定模式替换为另一种模式。也常常用于删除模式，传入空字符串
# print(val.replace(',', '::'))
# print(val.replace(',', ''))
# 这些运算大部分都能使用正则表达式实现


# python内置字符串方法
# Python内置字符串方法_1.png
# Python内置字符串方法_2.png


# 正则表达式
# 正则表达式(regex)提供了一种灵活的在文本中搜索或匹配字符串模式的方式
# 正则表达式是根据正则表达式语言编写的字符串
# Python内置的re模块负责对字符串应用正则表达式
# re模块的函数可以分为三个大类：模式匹配、替换以及拆分
# 一个regex描述了需要在文本中定位的一种模式，它可以用于许多目的
# 假设想要拆分一个字符串，分隔符为数量不定的一组空白符（制表符、空格、换行符）
# 描述一个或多个空白符的regex是/s+
# text = "foo bar\t baz   \tqux"
# print(re.split('\s+', text))
# 调用re.split('\s+', text)时，正则表达式会先被编译，然后再在text上调用其split方法
# 你可以用re.compile自己编译regex以得到一个可重用的regex对象
# regex = re.compile('\s+')
# print(regex.split(text))
# 如果只希望得到匹配regex的所有模式，则可以使用findall方法
# print(regex.findall(text))
# 如果你打算对许多字符串应用同一条正则表达式，强烈建议通过re.compile创建regex对象
# 这样将可以节省大量的CPU时间、
# match和search跟findall功能类似
# findall返回的是字符串中所有的匹配项，而search则只返回第一个匹配项
# match更加严格，它只匹配字符串的首部
# text = 'Dave dave@google.com'  \
#        'Steve steve@gmail.com'  \
#        'Rob rob@gmail.com'  \
#        'Ryan ryan@yahoo.com'
# print(text)
# pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A=Z]{2,4}')
# re.IGNORECASE的作用是使正则表达式对大小写不敏感
# regex = re.compile(pattern, flags=re.IGNORECASE)
# 对text使用findall将得到一组电子邮件地址
# print(regex.findall(text))
# search返回的是文本中第一个电子邮件地址（以特殊的匹配项对象形式返回）
# 对于上面那个regex，匹配项对象只能告诉我们模式在原字符串中的起始和结束位置
# m = regex.search(text)
# print(m)
# print(text[m.start():m.end()])
# regex.match则将返回None，因为它只匹配出现在字符串开头的模式
# print(regex.match(text))
# 另外还有一个sub方法，它会将匹配到的模式替换为指定字符串，并返回所得到的新字符串
# print(regex.sub('REDACTED', text))
# 假设你不仅想要找出电子邮件地址，还想将各个地址分成3个部分：用户名、域名以及域后缀
# 要实现此功能，只需将待分段的模式的各部分用圆括号包起来即可
# pattern = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.(A-Z){2,4}')
# regex = re.compile(pattern, flags=IGNORECASE)
# 由这种正则表达式所产生的匹配项对象，可以通过其groups方法返回一个由模式各段组成的元组
# m = regex.match('wesm@bright.net')
# print(m.groups())
# 对于带有分组功能的模式，findall会返回一个元组列表
# print(regex.findall(text))
# sub还能通过诸如\1、\2之类的特殊符号访问各匹配项中的分组
# print(regex.sub(r'Username: \1, Domain:: \2, Suffix: \3, text'))
# Python中还有许多的正则表达式，但大部分都超出了本书的范围
# 为各个匹配分组加上一个名称
# regex = re.compile(r'(?P<username>[A-Z0-9._%+-]+)'\
# 	              '@' \
# 	              '(?P<domain>[A-Z0-9.-]+)' \
# 	              '\.' \
# 	              '(?p<suffix>[A-Z]{2,4})', flags=re.IGNORECASE|re.VERBOSE)
# 由这种正则表达式所产生的匹配项对象可以得到一个简单易用的带有分组名称的字典
# m = regex.match('wesm@bright.net')
# print(m.groupdict())



# 正则表达式方法
# 正则表达式方法.png

# pandas中矢量化的字符串函数
# 清理待分析的散乱数据时，常常需要做一些字符串规整化工作
# 含有字符串的列有时还含有缺失数据
data = {'Dave':'dave@google.com', 'Steve':'steve@gmail.com',
       'Rob':'rob@gmail.com', 'Wes':np.nan}
data = Series(data)
print(data)
print(data.isnull())
# 通过data.map，所有字符串和正则表达式方法都能被应用于（传入lambda表达式或其他函数）
# 各个值，但是如果存在NA就会报错。Series有一些能够跳过NA值的字符串操作方法。
# 通过Series的str属性即可访问这些方法
# 通过str.contains检查各个电子邮件地址是否含有“gmail”
print(data.str.contains('gmail'))
# 这里也可以使用正则表达式，还可以加上任意re选项（如IGNORECASE）
print(pattern)
print(data.str.findall(pattern, flags=re.IGNORECASE))
# 有两个办法可以实现矢量化的元素获取操作：要么使用str.get，要么在str属性上使用索引
matches = data.str.match(pattern, flags=re.IGNORECASE)
print(matches)
print(matches.str.get(1))
print(matches.str[0])
# 你可以利用下面这种代码对字符串进行子串截取
print(data.str[:5])



# 矢量化的字符串方法
# 矢量化的字符串方法.png