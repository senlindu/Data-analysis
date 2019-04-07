# 通过命令行启动IPython
# ipython
# 可以在这里执行任何IPython语句，只需将其输入然后按下回车键就行了
# 如果只是在IPython中输入了一个变量，它将会显示出该对象的一个字符串表示
# 许多Python对象被格式化为可读性更好的形式，与print的普通输出形式有显著区别
# 在shell中输入表达式时，只要按下tab键，当钱命名空间中任何与已输入的字符串相匹配的变量就会被找出来
#
#
# 在变量的前面或后面加上一个问号（？）就可以将有关该对象的一些通用信息显示出来。这叫对象内省
# 使用？？还将显示出该函数的源代码
# ？还有一个用法，即搜索IPython命名空间，类似于UNIX或Windows命令行中的用法
# 一些字符再配以通配符（*）即可显示出所有与该通配符表达式相匹配的名称
#
#
# %run命令
# 在IPython会话环境中，所有文件都可以通过%run命令当做python程序来运行
# 脚本是在一个空的命名空间中运行的（没有import，也没有定义任何其他的变量）
# 此后，该文件中所定义的全部变量（还有各种import、函数和全局变量）就可以在当前shell中访问了
#
# 如果Python脚本需要用到命令行参数（通过sys.argv访问），可以将参数放到文件路径的后面，就像在命令行上执行那样
#
# 代码在执行中，只要按下“Ctrl+c”，就会引发一个keyboardinterrupt
#
# 多数情况下，可以通过“Ctrl+shift+v”将剪贴板中的代码片段粘贴出来
# 但有可能换行符被处理为<return>
#
# 使用%paste和%cpaste两个魔术函数
# %paste可以承载剪贴板中的一切文本，并在shell中以整体形式执行
#
# %cpaste多出一个用于粘贴代码的特殊提示符，在最终执行之前，你想粘贴多少代码就粘贴多少
# 如果想在执行那些粘贴进去的代码之前先检查一番，就可以考虑使用%cpaste
#
# 快捷键
# IPython快捷键.png
#
# 如果%run某段脚本或执行某条语句时发生了异常，ipython默然会输出整个调用栈跟踪，
# 其中还会附上调用栈各点附近的几行代码作为上下文参考
# 上下文代码参考的数量可以通过%xmode魔术命令进行控制
#
# Ipython有一些特殊命令（被称为魔术命令），以百分号%为前提
# 可以用%timeit这个魔术命令检测任意Python语句的执行时间
#
# 魔术命令默认是可以不带百分号%的，只要没有定义与其同名的变量即可，
# 这个技术叫做automagic,可以通过%automagic打开或关闭
# IPython魔术命令_1.png
# IPython魔术命令_2.png
#
# 基于Qt的富GUI控制台
# IPython开发了一个基于Qt框架的GUI控制台。如果你已经安装了pyQt或PySide，
# 使用下面的命令启动的话即可为其添加绘图功能
# ipython qtconsole --pylab=inline
# 通常通过在启动IPython时加上--pylab标记来集成matplotlib
#
# 使用命令历史
# IPython维护者一个位于硬盘上的小型数据库，其中含有你执行过的每条命令的文本
# 使用ctrl+p或上键向上搜索历史命令，Ctrl+n或下键向下搜索
# Ctrl+R用于实现部分增量搜索，按下后，输入你想搜索行中的几个字符
#
#
# 输入和输出变量
# 最近的两个输出结果分别保存在_和__变量中
# 输入的文本被保存在名为_iX的变量中，其中X表示的输入行的行号
# 每个输入变量都有一个对应的输出变量_X
# 由于输入变量是字符串，因此可以用Python的exec关键字重新执行
# %hint用于打印全部或部分输入历史，可以选择是否带行号
# %reset用于情况interactive命名空间，并可选择是否清空输入和输出缓存
# %xdel用于从IPython系统中移除特定对象的一切引用
#
#
# 记录输入和输出
# IPython能够记录整个控制台会话，包括输入和输出
# 执行%logstart即可开始记录日志
#
#
# 与操作系统交互
# 跟系统相关的IPython魔术命令
# Python-系统.png
# Python-系统_1.png
# 在IPython中，以感叹号（！）开头的命令行表示其后的所有内容需要在系统shell中执行
# 可以将shell命令的控制台输出存放到变量中，只需将！开头的表达式赋值给变量即可
# 使用！时，IPython还允许使用当钱环境中定义的Python值，只需在变量名前加上$即可
# 魔术命令%alias可以为shell命令自定义简称
# %alias test_alias(cd cho8; ls; cd..)
# IPython会在会话结束时忘记你定义的一切别名，除非在配置中添加
# 
# 
# 目录书签系统
# 能保存常用目录的别名以便实现快速跳转
# %bookmark db /home/wesm/Dropbox
# 在定义好书签后，可以在执行魔术命令%cd时使用这些书签了
# 如果书签名与当前工作目录中的某个目录名冲突，可以通过-b标记（其作用是覆写）使用书签目录
# %bookmark的-l选项的作用是列出所有书签
# 书签与别名的区别在于，会被自动持久化
# 
# 
# 软件开发工具
# IPython紧密集成并加强了Python内置的pdb调试器
# 交互式调试器
# %debug命令（在发生异常之后马上输入）将会调用那个“事后”调试器，并直接跳转到引发异常的那个栈帧
# 输入u（up）或d（down）可在栈跟踪的各级别之间切换
# 
# 执行%pdb命令可以让IPython在出现异常之后自动调用调试器
# 
# 当你想要设置断点或对函数/脚本进行单步调试时
# 1、使用带有-d选项的%run命令，会在执行之前先打开调试器，必须立即输入s(step)才能进入脚本
# 设置断点，然后输入c(continue)使脚本一直运行下去直到该断点为止
# 调试器命令的优先级高于变量名，这时在变量前面加上！即可查看其内容
# (I)Python调试器命令_1.png
# (I)Python调试器命令_2.png
# 
# 还有另外几种调用调试器的手段
# 1、使用set_trace这个特别的函数
# 
# 
# 测试代码的执行时间：%time和%timeit
# %time一次执行一条语句，然后报告总体执行时间
# %timeit对于任意语句，会自动多次执行以产生一个非常精确的平均执行时间
# 
# 
# 基本性能分析：%prun和%run -p
# 主要的Python性能分析工具是cprofile模块，不是专为IPython设计的
# cprofile在执行一个程序或代码块时，会记录各函数所耗费的时间
# python -m cProfile file
# 执行完，输出结果是按函数名排序的
# 加上参数-s标记制定一个排序规则
# python -m cProfile -c cumulative file
# 如果一个函数调用了别的函数，不会停下来重新计时，计算的是总时间
# 还可以编程的方式分析任意代码块的性能，%prun命令和带-p选项的%run
# %prun -l 7 -s cumulative function
# %run -p -s cumulative file也能达到，但无需退出IPython
# 
# 
# 逐行分析函数性能
# 使用一个叫做line_profile的小型库
# 其中一个新的魔术函数%lprun
# 可以配置IPython启用这个扩展
# c.TerminalIPythonApp.extensions = ['line_profiler']
# %lprun -f func1 -f func2 statement_to_profile
# 需要为%lprun指明想要测试哪个或哪些函数
# 
# 高级IPython功能
# 对于许多对象，内置的pprint模块就能给出漂亮的格式
# 但是，对于自己定义的类，必须自己生成所需的字符串输出
# 由于IPython会获取_repr_方法返回的字符串，并将其显示到控制台
# 我们也需要为自定义的类添加一个_repr_方法以得到一个更有意义的输出
# 
# 个性化和配置
# IPython shell在外观和行为方面的大部分内容都是可以进行设置IDE
# 1、修改颜色方案
# 2、修改输入输出和提示符
# 3、去掉out提示符跟下一个In提示符之间的空行
# 4、执行任意Python语句
# 5、启动IPython扩展
# 6、定义你自己的魔术命令或系统别名
# 所有的配置选项都定义在一个叫做ipython_config.py的文件中，
# 可以在~/.config/ipython/目录（UNIX）和%HOME%/.ipython/目录（windo）中
# 
# 还有一个很适合用的功能是拥有多个个性化设置
# ipython profile create secret_project
# 然后编辑新建这个profile_secret_project目录中的配置文件，再用下面方式启动IPython
# ipython --profile=secret_project
