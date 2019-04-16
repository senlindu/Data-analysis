import numpy as np
import random
import matplotlib.pyplot as plt

# 范例：随机漫步
# 我们通过模拟随机漫步来说明如何运用数组运算
# 从0开始，步长1和-1出现的概率相等
# 通过内置的random模块以纯Python的方式实现1000步的随机漫步
# position = 0
# walk = [position]
# steps = 1000
# for i in xrange(steps):
# 	step = 1 if random.randint(0, 1) else -1
# 	position += step
# 	walk.append(position)
# 	
# 其实就是随机漫步中各步的累计和，可以用一个数组运算来实现
# 用np.random模块一次性随机产生1000个“掷硬币”结果，将其分别设置为1或-1，然后计算累计和
# nsteps = 1000
# draws = np.random.randint(0, 2, size=nsteps)
# steps = np.where(draws > 0, 1, -1)
# walk = steps.cumsum()
# walk.min()
# walk.max()
# 
# 更复杂的统计任务--首次穿越时间，即随机漫步过程中第一次到达某个特定值的时间
# 假设我们想知道本次随机漫步需要多久才能距离初始0点至少10步远
# np.abs(walk) > 10可以得到一个布尔型数组，表示距离是否达到或超过10
# 我们想知道第一个10或-10的索引，可以用argmax来解决，返回该布尔型数组第一个最大值的索引
# (np.abs(walk) >= 10).argmax()
# 注意：使用argmax并不是很高效，因为它无论如何都会对数组进行完全扫描
# 
# 一次模拟多个随机漫步
# 如果你希望模拟多个随机漫步过程（比如5000个），只需稍微修改下即可
# 只要给numpy.random的函数传入一个二元数组就可以产生一个二维数组
# 然后我们就可以一次性计算5000个随机漫步过程（一行一个）的累计和
# nwalks = 5000
# nsteps = 1000
# draws = np.random.randint(0, 2, size=(nwalks, nsteps))
# steps = np.where(draws >= 0, 1, -1)
# walks = steps.cumsum(1)
# walks.max()
# walks.min()
# 
# 计算30或-30的最小穿越时间
# 因为不是5000个过程都达到了30，可以用any来对此进行检查
# hints30 = (np.abs(walks) >= 30).any(1)
# hints30.sum()
# 然后利用这个布尔型数组选出那些穿越了30的随机漫步，并调用
# argmax在轴1上获取穿越时间
# crossing_times = (np.abs(walks[hints30])) >= 30).argmax(1)
# crossing_times.mean()
# 
# 尝试其他分布方式得到漫步数据，只需使用不同的随机数生成函数即可
# 使用normal用于生成指定均值和标准差的正态分布数据
# steps = np.random.normal(loc=0, scale=0.25, size-(nwalks, nsteps))
# 