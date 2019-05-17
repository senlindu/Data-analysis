import socket
import threading
import time

# 网络编程
# Socket(套接字)是网络编程的一个抽象概念，通常用Socket表示"打开了一个网络链接"
# 打开一个Socket需要知道目标计算机的IP地址和端口号，再指定协议类型即可
# Python提供了两个基本的Socket模块：
# 1、Socket，提供了标准的BSD Sockets API
# 2、SocketServer，提供了服务器中心类，可以简化网络服务器的开发

# Socket 类型
# 套接字格式为socket(family, type[, protocal]),使用给定的地址族，套接字类型，协议编号
# (默认为0)来创建套接字
# Socket类型及说明.png

# Socket函数
# 包括了TCP和UDP
# Socket函数及说明.png

# TCP编程
# 网络编程一般包括两部分：服务端和客户端
# TCP是一种面向连接的通信方式，主动发起连接的叫客户端，被动响应连接的叫服务端
# 服务端创建和运行TCP服务端需要五个步奏：
# 1、创建Socket，绑定Socket到本地IP与端口
# 2、开始监听连接
# 3、进入循环，不断接收客户端的连接请求
# 4、接收传来的数据，并发送给对方数据
# 5、传输完毕后，关闭Socket
def dealClient(sock, addr):
	# 第四步：接收传来的数据，并发送给对方数据
	print('Accept new connection from %s : %s' % addr)
	sock.send(b'Hello, I am server!')
	while True:
		data = sock.recv(1024)
		time.sleep(1)
		if not data or data.decode('utf-8') == 'exit':
			break
		print('-->> %s!' % data.decode('utf-8'))
		sock.send(('Loop_Msg: %s!' % data.decode('utf-8')).encode('utf-8'))
	# 第五步：关闭Socket
	sock.close()
	print('Connection from %s:%s closed.' % addr)
if __name__ == '__main__':
	# 第一步：创建一个基于IPv4和TCP协议的Socket
	# Socket绑定的IP(127.0.0.1为本机IP)与端口
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('127.0.0.1', 9999))
	# 第二步：监听连接
	s.listen(5)
	print('Waiting for connection...')
	while True:
		# 第三步：接收一个新连接
		sock, addr = s.accept()
		# 创建新线程来处理TCP连接
		t = threading.Thread(target=dealClient, args=(sock, addr))
		t.start()
# 编写客户端，与服务端进行交互，TCP客户端的创建和运行需要三个步骤
# 1、创建Socket，连接远端地址
# 2、连接后发送数据和接收数据
# 3、传输完毕后，关闭Socket
# 初始化socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 连接目标的IP和端口
s.connect(('127.0.0.1', 9999))
# 接收消息
print('-->>'+ s.recv(1024).decode('utf-8'))
# 发送消息
s.send(b'Hello, I am a client')
print('-->>' + s.recv(1024).decode('utf-8'))
s.send(b'exit')
# 关闭Socket
# s.close()


# UDP编程
# TCP通信需要一个建立可靠连接的过程，而且通信双方以流的形式发送数据
# UDP是面向无连接的协议，不需要建立连接，只需要知道对方的IP地址和端口号，可以直接发送
# 数据包，但是不关心是否能到达目的端
# 对于不可靠到达的数据，就可以使用UDP协议
# UDP服务端创建和运行只需要三个步骤
# 1、创建Socket，绑定指定的IP和端口
# 2、直接发送数据和接收数据
# 3、关闭Socket
# 创建Socket，绑定指定的IP和端口
# SOCK_DGRM指定了这个Socket的类型是UDP，绑定端口和TCP一样
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 9999))
print('Bind UDP on 9999...')
while True:
	# 直接发送数据和接收数据
	data, addr = s.recvfrom(1024)
	print('Received from %s:%s' % addr)
	s.sendto(b'Hello, %s!' % data, addr)
# 客户端的创建和运行更加简单，创建Socket，直接可以与服务器进行数据交换
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'Hello', b'World']:
	# 发送数据
	s.sendto(data, ('127.0.0.1', 9999))
	# 接收数据
	print(s.recv(1024).decode('utf-8'))
s.close()
# 服务器绑定UDP与TCP端口互不冲突，即UDP的9999端口与TCP的9999端口可以各自绑定
# 