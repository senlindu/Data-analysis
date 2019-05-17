import os
import time
import random
import threading
import gevent
import urllib3
import Queue
from multiprocessing import Process, Pool, Pipe, freeze_support
from multiprocessing import Queue as mq
from multiprocessing.managers import BaseManager
from gevent import monkey
monkey.patch_all()
from urllib import request
from gevent.pool import Pool as gp


# 进程和线程


# 多进程
# Python实现多进程的方式主要有两种：
# 1、使用os模块的fork方法
# 2、使用multiprocessing模块
# 区别在于前者仅使用于Unix/Linux操作系统，后者是跨平台的
#
# Python的os模块封装了常见的系统调用，其中就有fork方法
# fork方法是调用一次，返回两次，原因在于操作系统将当前进程复制出一份进程(子进程)，
# 这两个进程几乎完全相同
# fork方法分别在父进程和子进程中返回，子进程永远返回0，父进程返回的是子进程的ID
# os模块中的getpid方法用于获取当前进程的ID，getppid方法用于获取父进程的ID

# if __name__ == '__main__':
# 	print('current process (%s) start ...' % (os.getpid))
# 	pid = os.fork()
# 	if pid < 0:
# 		print('error in fork')
# 	elif pid == 0:
# 		print('I am child process(%s) and my parent process is (%s)',
# 			(os.getpid(), os.getppid()))
# 	else:
# 		print('I(%s) created a child process (%s).' (od.getpid(), pid)

# multiprocessing模块提供了一个Process类来描述一个进程对象
# 创建子进程时需要传入一个执行函数和函数的参数，即可完成一个Process实例的创建，
# 用start()方法启动进程，用join()方法实现进程间的同步
# 子进程要执行的代码
# def run_proc(name):
# 	print('Child process %s (%s) Running...' % (name, os.getpid()))

# if __name__ == '__main__':
# 	print('Parent process %s.' % os.getpid())
# 	for i in range(5):
# 		p = Process(target=run_proc, args=(str(i)))
# 		print('Process will start')
# 		p.start()
# 	p.join()
# 	print('Process end')
# 启动大量的子进程时，使用进程池批量创建子进程的方式更加常见


# multiprocessing模块提供了一个Pool类来代表进程池对象
# Pool可以提供指定数量的进程供用户调用，默认大小是CPU的核数
# 当有新的请求提交到Pool中时，如果池还没有满，就创建一个新的进程用来执行该请求；
# 但如果池中进程数达到最大规定值，请求就会等待，直到有进程结束
# def run_task(name):
#     print('Task %s (pid = %s) is running...' % (name, os.getpid()))
#     time.sleep(random.random() * 3)
#     print('Task %s end.' % name)


# if __name__ == '__main__':
#     print('Current process %s.' % os.getpid())
#     p = Pool(processes=3)
#     for i in range(5):
#         p.apply_async(run_task, args=(i, ))
#     print('Waiting for all subprocesses done...')
#     p.close()
#     p.join()
#     print('All subprocesses done.')

# 注意：Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须调用close()，
# 调用close()之后就不能继续添加新的Process了


# 进程间通信
# Python提供了多种进程间通信的方式，如Queue、Pipe、Value+Array等
# Queue和Pipe的区别在于Pipe常用来在两个进程间通信，Queue用在多个进程间实现通信

# Queue是多进程安全的队列，可使用Queue实现多进程之间的数据传递。
# 有两个方法可以进行Queue操作：
# 1、Put方法用以插入数据到队列中，有两个可选参数blocked和timeout
# 如果blocked为True(默认值)，并且timeout为正值，该方法会阻塞timeout指定的时间，直到该队列有剩余的空间
# 如果超时，会抛出Queue.Full异常
# 如果blocked为False，但该Queue已满，会立即抛出Queue.Full异常
# 2、Get方法可以从队列读取并且删除一个元素。Get方法有两个可选参数：blocked和timeout
# 如果blocked为True(默认值)，并且timeout为正值，那么在等待时间内没有取到任何元素，会抛出Queue.Empty异常
# 如果blocked为False，分为两种情况：如果Queue有一个值可用，立即返回该值；否则，如果队列为空，
# 会立即抛出Queue.Empty异常
# 例如，在父进程中创建三个子进程，两个子进程往Queue中写入数据，一个子进程从Queue中读取数据

# 写数据进程执行的代码
# def proc_write(q, urls):
#     print('Process (%s) is writting...' % os.getpid())
#     for url in urls:
#         q.put(url)
#         print('Put %s to queue...' % url)
#         time.sleep(random.random())

# 读数据进程执行的代码


# def proc_read(q):
#     print('Process (%s) is reading...' % os.getpid())
#     while True:
#         url = q.get(True)
#         print('Get %s from queue...' % url)


# if __name__ == '__main__':
# 父进程创建Queue，并传给各个子进程
# q = mq()
# proc_writer1 = Process(target=proc_write, args=(q, ['url_1', 'url_2', 'url_3']))
# proc_writer2 = Process(target=proc_write, args=(q, ['url_4', 'url_5', 'url_6']))

# proc_reader = Process(target=proc_read, args=(q,))
# 启动子进程proc_writer，写入
# proc_writer1.start()
# proc_writer2.start()
# 启动子进程proc_reader，读取
# proc_reader.start()
# 等待proc_writer结束
# proc_writer1.join()
# proc_writer2.join()
# proc_reader进程里是死循环，无法等待其结束，只能强行终止
# time.sleep(random.random())
# proc_reader.terminate()

# Pipe常用来在两个进程间进行通信，两个进程分别位于管道的两端
# Pipe方法返回(conn1, conn2)代表一个管道的两个端。Pipe方法有duplex参数，如果为True(默认值)，
# 这个管道是全双工模式，conn1和conn2均可收发；若为False，conn1只负责接收消息，conn2只负责发送消息
# send和recv方法分别是发送和接收消息的方法
# 例如，创建两个进程，一个子进程通过Pipe发送数据，一个子进程通过Pipe接收数据


# def proc_send(pipe, urls):
#     for url in urls:
#         print('Process (%s) send: %s' % (os.getpid(), url))
#         pipe.send(url)
#         time.sleep(random.random())


# def proc_recv(pipe):
#     while True:
#         print('Process (%s) rev: %s' % (os.getpid(), pipe.recv()))
#         time.sleep(random.random())


# if __name__ == '__main__':
#     conn1, conn2 = Pipe()

#     p1 = Process(target=proc_send, args=(conn1, ['url_' + str(i) for i in range(10)]))
#     p2 = Process(target=proc_recv, args=(conn2,))
#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()


# 多线程
# 多线程类似于同时执行多个不同程序，有以下优点：
# 1、可以把运行时间长的任务放到后台去执行
# 2、用户界面可以更加吸引人
# 3、程序的运行速度可能加快
# 4、在一些需要等待的任务实现上如用户输入、文件读写和网络收发数据等比较有用
# Python提供了两个模块：thread和threading，thread是低级模块，threading是高级模块，对thread进行了封装

# 用threading模块创建多线程
# 两种方式创建：
# 1、把一个函数传入并创建Thread实例，然后调用start方法开始执行
# 2、直接从threading.Thread继承并创建线程类，然后重写__init__方法和run方法
# 第一种
# def thread_run(urls):
#     print('Current %s is running...' % threading.current_thread().name)
#     for url in urls:
#         print('%s ---->>> %s' % (threading.current_thread().name, url))
#         time.sleep(random.random())
#     print('%s ended.' % threading.current_thread().name)


# print('%s is running...' % threading.current_thread().name)
# t1 = threading.Thread(target=thread_run, name='Thread_1', args=(['url_1', 'url_2', 'url_3'], ))
# t2 = threading.Thread(target=thread_run, name='Thread_2', args=(['url_4', 'url_5', 'url_6'], ))
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print('%s ended.' % threading.current_thread().name)

# 第二种
# class myThread(threading.Thread):
#     def __init__(self, name, urls):
#         threading.Thread.__init__(self, name=name)
#         self.urls = urls

#     def run(self):
#         print('Current %s is running...' % threading.current_thread().name)
#         for url in self.urls:
#             print('%s --->>> %s' % (threading.current_thread().name, url))
#             time.sleep(random.random())
#         print('%s ended.' % threading.current_thread().name)


# print('%s is running...' % threading.current_thread().name)
# t1 = myThread(name='Thread_1', urls=['url_1', 'url_2', 'url_3'])
# t2 = myThread(name='Thread_2', urls=['url_4', 'url_5', 'url_6'])
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print('%s ended.' % threading.current_thread().name)


# 线程同步
# 如果多个线程共同对某个数据修改，则可能出现不可预料的结果，为了保证数据的正确性，
# 需要对多个线程进行同步
# 使用Thread对象的Lock和RLock可以实现简单的线程同步，这两个对象都有acquire方法
# 和release方法，对于那些每次只允许一个线程操作的数据，可以将其操作放到acquire和
# release方法之间

# 对于Lock对象，如果一个线程连续两次进行acquire操作，那么由于第一次acquire之后
# 没有release，第二次acquire将挂起线程。这会导致Lock对象永远不会release，使得
# 线程死锁.RLock对象允许一个线程多次对其进行acquire操作，因为在其内部通过一个
# counter变量维护着线程acquire的次数。而且每一次的acquire操作必须有一个release操作
# 与之对应，在所有的release操作完成之后，别的线程才能申请该RLock对象。
# mylock = threading.RLock()
# num = 0


# class myThread(threading.Thread):
#     def __init__(self, name):
#         threading.Thread.__init__(self, name=name)

#     def run(self):
#         global num
#         while True:
#             mylock.acquire()
#             print('%s locked, Number: %d' % (threading.current_thread().name, num))
#             if num >= 4:
#                 mylock.release()
#                 print('%s released, Number: %d' % (threading.current_thread().name, num))
#                 break
#             num += 1
#             print('%s released, Number: %d' % (threading.current_thread().name, num))
#             mylock.release()


# if __name__ == '__main__':
#     thread1 = myThread('Thread_1')
#     thread2 = myThread('Thread_2')
#     thread1.start()
#     thread2.start()

# 全局解释器锁(GIL)
# GIL会在解释执行代码时，产生互斥锁来限制线程对共享资源的访问，直到解释器遇到I/O操作或操作次数达到一定数目时才会释放GIL
# 由于GIL的存在，在进行多线程操作时，不能调用多个CPU内核，只能利用一个内核，所以在进行CPU密集型操作时，不推荐使用多线程，
# 更加倾向于多进程。
# 对于IO密集型操作，多线程可以明显提高效率，例如Python爬虫的开发


# 协程
# 又称微线程，是一种用户级的轻量级线程。
# 协程拥有自己的寄存器上下文和栈。协程调度切换时，将寄存器上下文和栈保存到其他地方，在切回来的时候，恢复先前保存的
# 寄存器上下文和栈。因此协程能保留上一次调用时的状态，每次过程重入时，就相当于进入上一次调用的状态。
# 在并发编程中，协程与线程类似，每个协程表示一个执行单元，有自己的本地数据，与其他协程共享全局数据和其他资源

# 协程需要用户自己编写调度逻辑，对于CPU来说，协程其实是单线程，所以CPU不用去考虑怎么调度，切换上下文，省去了CPU
# 的切换开销，一定程度上又好于多线程

# Python通过yield提供对协程的基本支出，但是不完全，使用第三方库gevent库是更好的选择。
# gevent是一个基于协程的Python网络函数库，使用greenlet在libev时间循环顶部提供了一个有更高级别并发性的API
# 主要有以下特性：
# 1、基于libev的快速事件循环，Linnux上是epoll机制
# 2.基于greenlet的轻量级执行单元
# 3、API复用了Python标准库里的内容
# 4、支持SSL的协作式sockets
# 5、可通过线程池或c-ares实现DNS查询
# 6、通过monkey patching功能使得第三方模块编程协作式

# gevent对协程的支持，本质上是greenlet在实现切换工作，基本流程如下：
# 假如进行访问网络IO操作时，出现阻塞，greenlet就显式地切换到另一段没有被阻塞的代码段执行，直到原先的阻塞状况消失以后，
# 再自动切换回原来的代码段继续处理。因此，greenlet是一种合理安排的串行方式

# 由于IO操作非常耗时，经常使程序处于等待状态，有了gevent为我们自动切换协程，就保证总有greenlet在运行，而不是等待IO，
# 这就是协程一般比多线程效率高的原因。由于切换时在IO操作时自动完成，所以gevent需要修改Python自带的一些标准库，将一些
# 常见的阻塞，如socket、select等地方实现协程跳转，这一过程在启动时通过monkey patch完成
# def run_task(url):
#     print('Visit ---> %s' % url)
#     try:
#         response = request.urlopen(url)
#         data = response.read()
#         print('%d bytes received from %s' % (len(data), url))
#     except Exception as e:
#         print(e)


# if __name__ == '__main__':
#     urls = ['https://github.com/', 'https://www.python.org/', 'http://www.cnblogs.com/']
#     greenlets = [gevent.spawn(run_task, url) for url in urls]
#     gevent.joinall(greenlets)
# spawn方法可以看做是用来形成协程，joinall方法就是添加这些协程人物，并且启动运行
# gevent还提供了对池的支持，当拥有动态数量的greenlet需要进行并发管理(限制并发数)时，就可以使用池，这在处理大量的
# 网络和IO操作时是非常需要的
# def run_task(url):
#     print('Visit --> %s' % url)
#     try:
#         response = request.urlopen(url)
#         data = response.read()
#         print('%d bytes received from %s' % (len(data), url))
#     except Exception as e:
#         print(e)
#     return 'url:%s ---> finish' % url


# if __name__ == '__main__':
#     pool = gp(2)
#     urls = ['https://github.com/', 'https://www.python.org/', 'http://www.cnblogs.com/']
#     results = pool.map(run_task, urls)
#     print(results)


# 分布式进程
# 分布式进程指的是将Process进程分布到多台机器上，充分利用多台机器的性能完成复杂的任务
# 分布式进程在Python中依然要用到multiprocessing模块
# 这个模块不仅支持多进程，其中managers子模块还支持把多进程分布到多台机器上，可以写一个服务进程作为调度者，将任务
# 分布到其他多个进程中，依靠网络通信进行管理
# 分布式进程.png

# 创建分布式进程需要分为六个步骤：
# 1、建立队列Queue，用来进行进程间的通信。服务进程创建任务队列task_queue，用来作为传递任务给任务进程的通道；服务进程
# 创建结果队列result_queue，作为任务进程完成任务后回复服务进程的通道。在分布式多进程环境下，必须通过由Queuemanager
# 获得的Queue接口来添加任务
# 2、把第一步中建立的队列在网络上注册，暴露给其他进程(主机)，注册后获得网络队列，相当于本地队列的映像
# 3、建立一个对象(Queuemanager(BaseManager))实例manager，绑定端口和验证口令
# 4、启动第三步中建立的实例，即启动管理manager，监管信息通道
# 5、通过管理实例的方法获得通过网络访问的Queue对象，即再把网络队列实体化成可以使用的本地队列
# 6、创建任务到"本地"队列中，自动上传任务到网络队列汇总，分配给任务进程进行处理
# Linux版
# taskManager.py
# 第一步：建立task_queue和result_queue，用来存放任务和结果
# task_queue = Queue.Queue()
# result_queue = Queue.Queue()

# class Queuemanager(BaseManager):
# 	pass

# 第二步：把创建的两个队列注册在网络上，利用register方法，callable参数关联了Queue对象，
# 将Queue对象在网络中暴露
# Queuemanager.register('get_task_queue', callable=lambda:task_queue)
# Queuemanager.register('get_result_queue', callable=lambda:result_queue)

# 第三步：绑定端口8001，设置验证口令'nihao'。相当于对象的初始化
# manager = Queuemanager(address=('', 8001), authkey='nihao')

# 第四步：启动管理，监听信息通道
# manager.start()

# 第五步：通过管理实例的方法获得通过网络访问的Queue对象
# task = manager.get_task_queue()
# result_queue = manager.get_result_queue()

# 第六步：添加任务
# for url in ['ImageUrl_' + i for i in range(10)]:
# 	print('put task %s ...' % url)
# 	task.put(url)

# 获取返回结果
# print('try get result...')
# for i in range(10):
# 	print('result is %s' % result.get(timeout=10))
# 关闭管理
# manager.shutdown()

# taskWorker.py
# 1、使用QueueManager注册用于获取Queue的方法名称，任务进程只能通过名称来在网络上获取Queue
# 2、连接服务器，端口和验证口令注意保持与服务进程中完全一致
# 3、从网络上获取Queue，进行本地化
# 4、从task队列获取任务，并把结果写入result队列
# win/linux版
# coding:utf-8
# 创建类似的QueueManager
# class QueueManager(BaseManager):
# 	pass
# 第一步：使用QueueManager注册用于获取Queue的方法名称
# QueueManager.register('get_task_queue')
# QueueManager.register('get_result_queue')
# 第二步：连接到服务器
# server_addr = '127.0.0.1'
# print('Connect to server %s...' % server_addr)
# 端口和验证口令注意保持与服务进程完全一致
# m = QueueManager(address=(server_addr, 8001), authkey='nihao')
# 从网络连接
# m.connect()
# 第三步：获取Queue的对象
# task = m.get_task_queue()
# result = m.get_result_queue()
# 第四步：从task队列获取任务，并把结果写入result队列
# while(not tsk.empty()):
# 	image_url = task.get(True, timeout=5)
# 	print('run task download %s...' % image_url)
# 	time.sleep(1)
# 	result.put('%s --->success' % image_url)
# 处理结束
# print('worker exit.')

# taskManager.py
# windows版
# 任务个数
# task_number = 10
# 定义收发队列
# task_queue = Queue.Queue(task_number)
# result_queue = Queue.Queue(task_number)
# def get_task():
# 	return task_queue
# def get_result():
# 	return result_queue
# 创建类似的QueueManager
# class QueueManager(BaseManager):
# 	pass
# def win_run():
	# windows下绑定调用接口不能使用lambda，所以只能先定义函数再绑定
	# QueueManager.register('get_task_queue', callable = get_task)
	# QueueManager.register('get_result_queue', callable = get_result)
	# 绑定端口并设置验证口令，Windows下需要填写IP地址，Linux下不填默认为本地
	# manager = QueueManager(address = ('127.0.0.1, 8001'), authkey='nihao')
	# 启动
	# manager.start()
	# try:
		# 通过网络获取任务队列和结果队列
		# task = manager.get_task_queue()
		# result = manager.get_result_queue()
		# 添加任务
	# 	for url in ['ImageUrl_' + str(i) for i in range(10)]:
	# 		print(' put task %s...' % url)
	# 		task.put(url)
	# 	print('try get result...')
	# 	for i in range(10):
	# 		print('result is %s' % result.get(timeout=10))
	# except Exception as e:
	# 	print('Manager error')
	# finally:
		# 一定要关闭，否则会报管道未关闭的错误
		# manager.shutdown()
# if __name__ == '__main__':
	# windows下多进程可能会有问题，添加这句会有缓解
	# freeze_support()
	# win_run()

		