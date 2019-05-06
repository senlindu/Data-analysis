import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
from numpy.random import randn
from datetime import datetime
from io import StringIO


# 绘图和可视化
# 绘图是数据分析工作最重要的任务之一，是探索过程的一部分
# 还可以利用诸如d3.js（http://d3js.org/）之类的工具为web应用构建交互式图像
# Python有许多可视化工具，但主要讲解matplotlib（http://matplotlib.sourceforge.net）
#
# matplotlib是一个用于创建出版质量图表的桌面绘图包（主要是2D方面），其目的是诶Python构建
# 一个MATLAB式的绘图接口。
# 如果结合使用一种GUI工具包，matplotlib还具有诸如缩放和平移等交互功能
# 它不仅支持各种操作系统上许多不同的GUI后端，而且还能将图片导出为各种常见的矢量和光栅图：
# PDF、SVG、JPG、PNG、BMP、GIF等

# matplotlib还有许多插件工具集，如用于3D图形的mplot3D以及用于地图和投影的basemap
# 要使用本章中的代码示例，请确保你的IPython是以Pylab模式启动的，或通过%gui魔术命令
# 打开了GUI事件循环集成


# matplotlib API入门
# 使用matplotlib的办法有很多种，最常用的方式是pylab模式的IPython，这样会将IPython
# 配置为使用你所制定的matplotlib GUI后端
# pylab模式还会向IPython引入一大堆模块和函数以提供一种更接近MATLAB的界面
# plt.plot(np.arange(10))
# plt.show()
# 虽然pandas的绘图函数能够处理许多普通的绘图任务，但如果需要自定义一些高级功能的话
# 就必须学习matplotlib API


# Figure和Subplot
# matplotlib的图像都位于Figure对象中。
# 你可以用plt.figure创建一个新的Figure
# fig = plt.figure()
# plt.figure有一些选项，特别是figsize，用于确保当图片保存到磁盘时具有一定的大小和
# 纵横比。matplotlib中的Figure还支持一种MATLAB式的编号架构（plt.figure(2)）
# 通过plt.gcf()即可得到当前Figure的引用
# 不能通过空Figure绘图。必须用add_subplot创建一个或多个subplot才行
# ax1 = fig.add_subplot(2, 2, 1)
# 图像是2*2的，且当前选中的是4个subplot中的第一个（编号从1开始）
# ax2 = fig.add_subplot(2, 2, 2)
# ax3 = fig.add_subplot(2, 2, 3)

# 如果这时发出一条绘图命令,会在最后一个用过的subplot上进行绘制
# plt.plot([1.5, 3.5, -2, 1.6])
# plt.plot(randn(50).cumsum(), 'k--')
# plt.show()
# "k--"是一个线性选项，用于告诉matplotlib绘制黑色虚线图。上面那些由fig.add_subplot
# 所返回的对象时AxesSubplot对象，直接调用它们的实例方法就可以在其他空着的格子里画图
# _ = ax1.hist(randn(100), bins=20, color='k', alpha=0.3)
# ax2.scatter(np.arange(30), np.arange(30) + 3 * randn(30))
# plt.show()
# 你可以在matplotlib的文档中找到各种图标类型
# 由于根据特定布局创建Figure和subplot是一件非常常见的任务，于是便出现了一个更为方便
# 的方法（plt.subplots）,它可以创建一个新的Figure，并返回一个含有已 创建的subplot
# 对象的Numpy数组
# fig, axes = plt.subplots(2, 3)
# print(axes)
# 这是非常实用的，因为可以轻松地对axes数组进行索引，就好像一个二维数组一样
# 你还可以通过sharex和sharey指定subplot应该具有相同的X轴或Y轴
# 在比较相同范围的数据时，这也是非常实用的，否则，matplotlib会自动缩放各图表
# 的界限


# pyplot.subplots的选项
# pyplot_subplot选项.png


# 调整subplot周围的间距
# 默认情况下，matplotlib会在subplot外围留下一定的边距，并在subplot之间留下一定的间距
# 间距跟图像的高度和宽度有关，因此，如果你调整了图像大小，间距也会自动调整
# 利用Figure的subplots_adjust方法可以轻而易举地修改间距，此外，它也是个顶级函数
# subplots_adjust(left=None, bottom=None, right=None, top=None,
# 	wspace=None, hspace=None)
# wspace和hspace用于控制宽度和高度的百分比，可以用作subplot之间的间距。
# fig, axes = plt.subplots(2, 2, sharex=True, sharey=True)
# for i in range(2):
#     for j in range(2):
#         axes[i, j].hist(randn(500), bins=50, color='k', alpha=0.5)
# plt.subplots_adjust(wspace=0, hspace=0)
# plt.show()
# 不难看出，其中的轴标签重叠了。matplotlib不会检查标签是否重叠，所以对于这种
# 情况，只能自己设定刻度位置和刻度标签


# 颜色、标记和线型
# matplotlib的plot函数接受一组X和Y坐标，还可以接受一个表示颜色和线型的字符串缩写
# 例如，要根据x和y绘制绿色虚线，可以执行：
# ax.plot(x, y, 'g--')
# 通过更为明确的方式
# ax.plot(x, y, linestyle='--', color='g')
# 常用的颜色都有一个缩写词，要使用其他任意颜色则可以通过制定其RGB值的形式使用
# 线型图还可以加上一些标记，以强调实际的数据点
# 由于matplotlib创建的是连续的线型图（点与点之间插值），因此有时可能不太容易
# 看出真实数据点的位置
# 标记也可以放到格式字符串中，但标记类型和线型必须放在颜色后面
# plt.plot(randn(30).cumsum(), 'ko--')
# plt.show()
# 还可以写成更为明确的形式
# plot(randn(30).cumsum(), color='k', linestyle='dashed', marker='o')
# 在线型图中，非实际数据点默认是按线性方式插值的，可以通过drawstyle选项修改
# data = randn(30).cumsum()
# plt.plot(data, 'ko--', label='Default')
# plt.plot(data, 'k-', drawstyle='steps-post', label='steps-post')
# 选择最佳的标签位置
# plt.legend(loc='best')
# plt.show()


# 刻度、标签和图例
# 对于大多数的图表装饰项，其主要实现方式有二：使用过程型的pyplot接口以及更为面向
# 对象的原生matplotlib API
# pyplot接口的设计目的就是交互式使用，含有诸如xlim、 xticks和xticklabels之类的
# 方法。它们分别控制图表的范围、刻度位置、刻度标签等。其使用方式有：
# 1.调用时不带参数，则返回当前的参数值。plt.xlim()返回当前的x轴绘图范围
# 2.调用时带参数，则设置参数值。plt.xlim([0,10])会将X轴的范围设置为0到10
# 所有这些方法都是对当前或最近创建的AxesSubplot起作用的。它们各自对应subplot对象
# 上的两个方法，以xlim为例，就是ax.get_xlim和ax.set_xlim。


# 设置标题、轴标签、刻度以及刻度标签
# 为了说明轴的自定义，创建一个简单的图像并绘制一段随机漫步
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# ax.plot(randn(1000).cumsum())
# 要修改X轴的刻度，最简单的办法是使用set_xticks和set_xticklabels
# 前者告诉matplotlib要将刻度放在数据范围中的哪些位置，默认情况下，
# 这些位置也就是刻度标签。但我们可以通过set_xticklabels将任何其他
# 值用作标签
# ticks = ax.set_xticks([0, 250, 500, 750, 1000])
# labels = ax.set_xticklabels(['one', 'two', 'three', 'four', 'five'],
#                             rotation=30, fontsize='small')
# 最后再用set_xlabels为X轴设置一个名称，并用set_title设置一个标题
# ax.set_title('My first matplotlib plot')
# ax.set_xlabel('Stages')
# plt.show()


# 添加图例
# 图例是另一种用于标识图表元素的重要工具
# 添加图例的方式有二，最简单的是在添加subplot的时候传入label参数
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# ax.plot(randn(1000).cumsum(), 'k', label='one')
# ax.plot(randn(1000).cumsum(), 'k--', label='two')
# ax.plot(randn(1000).cumsum(), 'k.', label='three')
# 在此之后，你可以调用ax.legend()或plt.legend()来自动创建图例
# ax.legend(loc='best')
# plt.show()
# loc告诉matplotlib要将图例放在哪。
# 要从图例中去除一个或多个元素，不传入label或传入label='_nolegend_'即可


# 注解以及在Subplot上绘图
# 除标准的图表对象之外，你可能还希望绘制一些自定义的注解（文本、箭头或其他图形）
# 注解可以通过text、arrow和annotate等函数进行添加
# text可以将文本绘制在图表的制定坐标（x, y），还可以加上一些自定义格式
# ax.text(x, y, 'Hello World!', family='monospace', fontsize=10)
# 注解中可以既含有文本也含有箭头
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)

# data = pd.read_csv('e:/examples/spx.csv', index_col=0,
#                    parse_dates=True)
# print(data)
# spx = data['SPX']

# spx.plot(ax=ax, style='k-')

# crisis_data = [(datetime(2007, 10, 11), 'Peak of bull market'),
#                (datetime(2008, 3, 12), 'Bear Stearns Fails'),
#                (datetime(2008, 9, 15), 'Lehman Bankruptcy')]
# for date, label in crisis_data:
#     ax.annotate(label, xy=(date, spx.asof(date) + 50),
#                 xytext=(date, spx.asof(date) + 200),
#                 arrowprops=dict(facecolor='red'),
#                 horizontalalignment='left', verticalalignment='top')
# 放大到2007-2010
# ax.set_xlim(['1/1/2007', '1/1/2011'])
# ax.set_ylim([600, 1800])

# ax.set_title('important dates in 2008-2009 financial crisis')
# plt.show()

# matplotlib有一些表示常见图形的对象，这些对象被称为块
# 其中有些可以在matplotlib。pyplot中找到（如Rectangle和Circle），
# 但完整集合位于matplotlib.patches

# 要在图表中添加一个图形，你需要创建一个块对象shp，然后通过ax.add_subplot(shp)
# 将其添加到subplot中
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

rect = plt.Rectangle((0.2, 0.75), 0.4, 0.15, color='k', alpha=0.3)
circ = plt.Circle((0.7, 0.2), 0.15, color='b', alpha=0.3)
pgon = plt.Polygon([[0.15, 0.15], [0.35, 0.4], [0.2, 0.6]],
                   color='g', alpha=0.5)

ax.add_patch(rect)
ax.add_patch(circ)
ax.add_patch(pgon)
# 如果查看许多常见图表对象的具体实现代码，你就会发现它们其实就是由块组装而成的
plt.show()


# 将图表保存到文件
# 利用plt.savefig可以将当前图表保存到文件
# 该方法相当于Figure对象的实例方法savefig
# plt.savefig('figpath.svg')
# 文件类型是通过文件扩展名推断出来的
# 最常用的两个重要的选项dpi(控制每英寸点数分辨率)和bbox_inches(可以
# 剪除当前图表周围的空白部分)
# 要得到一张带有最小白边且分辨率为400DPI的PNG图片
# plt.savefig('figpath.png', dpi=400, bbox_inches='tight')
# savefig并非一定要写入磁盘，也可以写入任何文件型的对象，比如StringIO
# buffer = StringIO()
# plt.savefig(buffer)
# plot_data = buffer.getvalue()
# 这对在web上提供动态生成的图片是很实用的


# savefig选项
# savefig选项.png


# matplotlib配置
# matplotlib自带一些配色方案，以及为生成出版质量的图片而设定的默认配置信息
# 几乎所有默认行为都能通过一组全局参数进行自定义，可以管理图像大小、subplot边距、
# 配色方案、自体大小、网格类型等
# 操作matplotlib配置系统的方式主要有两种
# 1.Python编程方式，利用rc方法
# 要将全局的图像默认代销设置为10*10
# plt.rc('figure', figsize=(10, 10))
# rc的第一个参数是希望自定义的对象，如'figure'、'axes'、'xtick'、'ytick'、'grid'、
# 'legend'等，其后可以跟上一系列的关键字参数
# 最简单的办法是将这些选项写成一个字典
# font_options = {'family':'monospace', 'weight':'bold', 'size':'small'}
# plt.rc('font', **foot_options)
# 要了解全部的自定义选项，请查阅matplotlib的配置文件matplotlibrc