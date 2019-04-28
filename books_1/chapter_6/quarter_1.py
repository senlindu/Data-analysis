import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import sys
import csv
import json
from lxml.html import parse
# urllib2 改为 urllib.request
from urllib.request import urlopen
from pandas.io.parsers import TextParser
from lxml import objectify

# 输入输出通常可以划分为几个大类
# 读取文本文件和其他更高效的磁盘存储格式
# 加载数据库中的数据
# 利用web Api操作网络资源


# 读写文本格式的数据
# 因为其简单的文本交互语法，直观的数据结构，以及诸如元组打包解包之类的便利
# 功能，Python在文本和文件处理方面已经成为一门招人喜欢的语言
# pandas提供了一些用于将表格型数据读取为DataFrame对象的函数
# read_csv和read_table可能是用的最多的

# pandas中的解析函数
# pandas中的解析函数.png
# 这些函数的选项可以划分为以下几个大类
# 索引：将一个或多个列当做返回的DataFrame处理，以及是否从文件、
# 用户获取列名
# 类型推断和数据转换： 包括用户定义值的转换、缺失值标记列表等
# 日期解析： 包括组合功能，比如将分散在多个列中的日期时间信息组合成
# 结果中单个列
# 迭代： 支持对大文件进行逐块迭代
# 不规整数据问题：跳过一些行、页脚、注释或其他一些不重要的东西（比如
# 由成千上万个逗号隔开的数值数据）

# 类型推断是这些函数中最重要的功能之一
# 你不需要指定列的类型到底是数值、整数、布尔型，还是字符串
# 日期和其他自定义类型的处理需要多花点功夫才行
# 以逗号分隔的（csv）文本文件
# 由于以逗号分隔，使用read_csv将其读入一个DataFrame
# df = pd.read_csv('E:/examples/ex1.csv')
# print(df)
# 我们也可以用read_table，只是需要指定分隔符而已
# print(pd.read_table('E:/examples/ex1.csv', sep=','))
# 并不是所有文件都有标题行
# !type 'E:/examples/ex2.csv'
# 读入此文件的办法有两个
# 让pandas为其分配默认的列名
# print(pd.read_csv('E:/examples/ex2.csv', header=None))\
# 自己定义列名
# print(pd.read_csv('E:/examples/ex2.csv', names=['a', 'b',
# 'c', 'd', 'message']))
# 假设你希望将message列作为DataFrame的索引，你可以明确表示要
# 将该列放到索引4的位置上，也可以通过set_col参数指定“message”
# names = ['a', 'b', 'c', 'd', 'message']
# print(pd.read_csv('E:/examples/ex2.csv', names=names,
#                   index_col='message'))

# 如果希望将多个列做一个层次化索引，只需传入由列编号或列名组成的列表即可
# ~!type E:/examples/csv_mindex.csv
# parsed=pd.read_csv('E:/examples/csv_mindex.csv', index_col=['key1', 'key2'])
# print(parsed)
# 有些表格可能不是用固定的分隔符去分隔字段的（比如空白符或其他模式）
# 对于这种情况，可以编写一个正则表达式作为read_table的分隔符
# print(list(open('E:/examples/ex3.csv')))
# 该文件各个字段由数量不定的空白符分隔，虽然你可以对其做一些手工调整，
# 但这个情况还是处理比较好
# 本例可以用正则表达式\s+表示
# result = pd.read_table('E:/examples/ex3.csv', sep='\s+')
# print(result)
# 由于列名比数据行的数量少，所以read_table推断第一列应该是
# DataFrame的索引
# 这些解析器函数还有许多参数可以帮助你处理各种各样的异形文件格式
# 比如skiprows跳过文件的第一行、第三行和第四行
# !type E:/examples/ex4.csv
# print(pd.read_csv('E:/examples/ex4.csv', skiprows=[0, 2, 3]))
# 缺失值处理时文件解析任务中的一个重要组成部分
# 缺失数据经常要么没有，要么用某个标记值表示
# 默认情况下，pandas会用一组经常出现的标记值进行识别，如NA、-1.#IND或NULL等
# !type E:/examples/ex5.csv
# result = pd.read_csv('E:/examples/ex5.csv')
# print(result)
# print(result.isnull())
# na_values可以接受一组用于表示缺失值的字符串
# result = pd.read_csv('E:/examples/ex5.csv', na_values=['NULL'])
# print(result)
# 可以用一个字典为各列指定不同的NA标记值
# sentinels = {'message': ['foo', 'NA'], 'something': ['two']}
# print(pd.read_csv('E:/examples/ex5.csv', na_values=sentinels))

# read_csv/read_table函数的参数
# read函数参数_1.png
# read函数参数_2.png
# read函数参数_3.png


# 逐块读取文本文件
# 在处理很大的文件时，或找出打文件中的参数集以便与后续处理时，
# 你可能只想读取文件的一小部分或逐块对文件进行迭代
# result = pd.read_csv('e:/examples/ex6.csv')
# print(result)
# 如果只想读取几行（避免读取整个文件），通过nrows进行指定即可
# print(pd.read_csv('e:/examples/ex6.csv', nrows=5))
# 要逐块读取文件，需要设置chunksize（行数）
# chunker = pd.read_csv('e:/examples/ex6.csv', chunksize=1000)
# print(chunker)
#<pandas.io.parsers.TextFileReader object at 0x0000000002864630>
# read_csv所返回的这个TextParser对象使你可以根据chunksize对文件
# 进行逐块迭代。
# 我们可以迭代处理ex6.csv,将值计数聚合到“key”列中
# chunker = pd.read_csv('e:/examples/ex6.csv', chunksize=1000)
# tot = Series([])
# for piece in chunker:
#     tot = tot.add(piece['key'].value_counts(), fill_value=0)
# tot = tot.sort_index(ascending=False)

# print(tot[:10])
# TextParser还有一个get_chunk方法，使你可以读取任意大小的块


# 将数据写出到文本格式
# 数据也可以被输出为分隔符格式的文本
# data = pd.read_csv('e:/examples/ex5.csv')
# print(data)
# 利用DataFrame的to_csv方法，可以将数据写入一个以逗号分隔的文件中
# data.to_csv('e:/examples/out_1.csv')
# 当然，还可以使用其他分隔符
# sys.stdout,仅仅是打印出文本结果而已
# data.to_csv(sys.stdout, sep='|')
# 缺失值在输出结果中会被表示为空字符串
# 你可能希望将其表示为别的标记值
# data.to_csv(sys.stdout, na_rep='NULL')
# 如果没有设置其他选项，则会写出行和列的标签，也可以被禁用
# data.to_csv(sys.stdout, index=False, header=False)
# 此外，你还可以只写出一部分的列，并以你指定的顺序排列
# data.to_csv(sys.stdout, index=False, columns=['a', 'b', 'c'])
# series也有一个to_csv方法
# dates = pd.date_range('1/1/2000', periods=7)
# ts = Series(np.arange(7), index=dates)
# ts.to_csv(sys.stdout)
# 虽然只需一点整理工作（无header行，第一列做索引）就能用
# read_csv将CSV文件读取为Series，但还有一个更为方便的
# from_csv方法
# from_csv is deprecated. Please use read_csv(...) instead
#  pd.read_csv(path, index_col=0, parse_dates=True)
# print(pd.read_csv('e:/examples/tseries.csv', index_col=0, parse_dates=True))


# 手工处理分隔符格式
# !type ex7.csv
# 对于任何单字符分隔符文件，可以直接使用Python内置的CSV模块
# 将任意已打开的文件或文件型的对象传给csv_reader
# f = open('e:/examples/ex7.csv')
# reader = csv.reader(f)
# 对这个reader进行迭代将会为每行产生一个元组（并移除了所有引号）
# for line in reader:
# print(line)
# 为了使数据格式合乎要求，需要对其做一些整理
# lines = list(csv.reader(open('e:/examples/ex7.csv')))
# header, values = lines[0], lines[1:]
# data_dict = {h: v for h, v in zip(header, zip(*values))}
# print(data_dict)
# CSV文件的形式有很多
# 只需定义csv.Dialect的一个子类即可定义出新格式（如专门的分隔符、
# 字符串引用约定、行结束符等）


# class my_dialect(csv.Dialect):
# """docstring for my_dialect"""
# 	lineterminator = '\n'
# 	delimiter = ';'
# 	quotechar = '"'


# reader = csv.reader(f, dialect=my_dialect)
# 各个CSV语支的参数也可以关键字的形式提供给csv.reader，而无需
# 定义子类
# reader = csv.reader(f, delimiter='|')

# 可用的选项（csv.Dialect的属性）及其功能
# CSV语支选项.png
# 注意：对于使用复杂分隔符或多字符分隔符的文件，只能使用字符串
# 的split方法或正则表达式re.split进行拆分和其他整理

# 要手工输出分隔符文件，可以使用csv.writer
# 它接受一个已打开且可写的文件对象以及跟csv.reader相同的
# 那些语支和格式化选项
# with open('mydata.csv', 'w') as f:
# writer = csv.writer(f, dialect=my_dialect)
# writer.writerow(('one', 'two', 'three'))
# writer.writerow(('1', '2', '3'))
# writer.writerow(('4', '5', '6'))
# writer.writerow(('7', '8', '9'))


# JSON数据
# JSON已经成为通过HTTP请求在web浏览器和其他应用程序之间发送
# 数据的标准格式之一
# 它是一种比表格型文本格式（如csv）灵活得多的数据格式
# obj = '{"name": "Wes", "places_lived": ["United States", "Spain", "Germany"], \
#        "pet": "", "siblings": [{"name": "Scott", "age": 25, "pet": "Zuko"}, \
#                                  {"name": "Katie", "age": 33, "pet": "Cisco"}]}'
# 除其空值null和一些其他的细微差别（如列表末尾不允许存在多余
# 的逗号）之外，JSON非常接近于有效的Python代码。
# 基本类型有对象（字典）、数组（列表）、字符串、数值、布尔值以及null
# 对象中所有的键都必须是字符串
# 许多Python库都可以读写JSON数据
# 我将使用json，因为它是构建与Python标准库的
# 通过json.loads即可将JSON字符串转换成Python形式
# json.loads take a string as input and returns a dictionary as output.
# json.dumps take a dictionary as input and returns a string as output.
# result = json.loads(obj)
# print(result)
# 相反，json.dumps则将Python对象转换为JSON格式
# asjson = json.dumps(result)
# 如何将（一个或一组）JSON对象转换为DataFrame或其他便于分析的
# 数据结构就由你决定
# 最简单方便的方式是：向DataFrame构造器传入一组JSON对象，并
# 选取数据字段的子集
# siblings = DataFrame(result['siblings'], columns=['name', 'age'])
# print(siblings)


# XML和HTML： Web信息收集
#  Python有许多可以读写HTML和XML格式数据的库
#  lxml(http://lxml.de)就是其中之一，它能够高效且可靠地解析大文件
#  lxml有多个编程接口
#  首先要用lxml.html处理HTML,然后再用lxml.objectify做一些XML处理
#  首先，找到你希望获取数据的URL，利用urllib2将其打开，然后用lxml
#  解析得到的数据流
# parsed = parse(urlopen('http://finance.yahoo.com/q/op?s=AAPL+Options'))
# doc = parsed.getroot()
# 通过这个对象，你可以获取特定类型的所有HTML标签，比如含有所需数据的
# table标签。
# 假设你想得到该文档中所有的URL链接，HTML中的连接是a标签。
# 使用文档根节点的findall方法以及一个XPATH
# links = doc.findall('.//a')
# print(links[15:20])
# 要得到URL和链接文本，您必须使用个对象的get方法(URL)和
# text_content方法(显示文本)
# lnk = links[28]
# print(lnk)
# print(lnk.get('href'))
# print(lnk.text_content())
# 编写下面这条列表推导式即可获取文档中的全部URL
# urls = [lnk.get('href') for lnk in doc.findall('.//a')]
# print(urls[-10:])
# 现在，从文档中找出正确表格的办法就是反复试验了
# 有些网站会给目标表格加上一个id属性
# tables = doc.findall('.//table')
# print(tables)
# calls = tables[0]
# puts = tables[1]
# print(calls)
# print(puts)
# 每个表格都有一个标题行，然后才是数据行
# rows = calls.findall('.//tr')
# print(rows)
# 对于标题行和数据行，我们希望获取每个单元格内的文本
# 对于标题行，就是th单元格，对于数据行，则是td单元格


# def _unpack(row, kind='td'):
#     elts = row.findall('.//%s' % kind)
#     return [val.text_content() for val in elts]


# print(_unpack(rows[0], kind='th'))
# print(_unpack(rows[1], kind='td'))
# 将所有步骤结合起来，将数据转换为一个DataFrame
# 由于数值型数据仍然是字符串格式，我们希望将部分列转换为浮点数格式
# pandas恰好有一个TextParser类可用于自动类型转换


# def parse_options_data(table):
#     rows = table.findall('.//tr')
#     header = _unpack(rows[0], kind='th')
#     data = [_unpack(r) for r in rows[1:]]
#     return TextParser(data, names=header).get_chunk()


# 对两个lxml表格对象调用该解析函数并得到最终的DataFrame
# call_data = parse_options_data(calls)
# put_data = parse_options_data(puts)
# print(call_data[:10])
# print(put_data[:10])


# 使用lxml.objectify解析XML
# XML是另一种常见的支持分层、嵌套数据以及元数据的结构化数据格式
# 先用lxml.objectify解析改文件，然后通过getroot得到给XML文件的根节点的引用
path = 'e:/datasets/mta_perf/Performance_MNR.xml'
parsed = objectify.parse(open(path))
root = parsed.getroot()
# root.INDICATOR返回一个用于产生各个<INDICATOR>XML元素的生成器
# 对于每条记录，我们可以用标记名和数据值填充一个字典
data = []
skip_fields = ['PARENT_SEQ', 'INDICATOR_SEQ', 'DESIRED_CHANGE',
               'DECIMAL_PLACES']
for elt in root.INDICATOR:
    elt_data = {}
    for child in elt.getchildren():
        if child in skip_fields:
            continue
        elt_data[child.tag] = child.pyval
    data.append(elt_data)
# 最后，将这组字典转换成一个DataFrame
perf = DataFrame(data)
print(perf)
# XML数据可以比本例复杂得多，每个标记都可以由元数据
# 