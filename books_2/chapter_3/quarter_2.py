import urllib
from urllib import request
from urllib import parse
from http import cookiejar
import requests
import chardet

# HTTP请求的Python实现
# Python中实现HTTP请求的三种方式
# 1、urllib2/urllib实现
# python3中没有urllib2，统一为urllib
# 简单的形式
# response = request.urlopen('http://zhihu.com')
# html = response.read()
# print(html)
# 上面为GET请求
# POST请求
# url = 'http://www.xxxxxx.com/login'
# postdata = {'username': 'nihao', 'password': 'nihao_pass'}
# info需要被编码为urllib能理解的格式
# data = parse.urlencode(postdata)
# req = request.Request(url, data)
# response = request.urlopen(req)
# html = response.read()
# 有时需要请求中的头信息，服务器会检验请求头，来判断是否是来自浏览器的访问，
# 这也是反爬虫的常用手段

# 请求头headers处理
# url = 'http://www.xxxxxx.com/login'
# user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36' \
#              '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
# referer = 'http://www.xxxxx.com'
# postdata = {'username': 'nihao', 'password': 'nihao_pass'}
# info需要被编码为urllib能理解的格式
# 将user_gent，referer写入头信息
# headers = {'User-Agent':user_agent, 'Referer':referer}
# data = parse.urlencode(postdata)
# req = request.Request(url, data, headers)
# response = request.urlopen(req)
# html = response.read()

# 也可以使用add_header来添加请求头信息
# url = 'http://www.douban.com/login'
# user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36' \
#              '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
# referer = 'http://www.douban.com'
# postdata = {'username': 'xxx', 'password': 'xxx'}
# info需要被编码为urllib能理解的格式
# headers = {'User-Agent': user_agent, 'Referer': referer}
# data = parse.urlencode(postdata).encode()
# req = request.Request(url)
# 将user_gent，referer写入头信息
# req.add_header('User-Agent', user_agent)
# req.add_header('Referer', referer)
# req.data = data
# response = request.urlopen(req)
# html = response.read().decode()
# print(html)

# 对于有些header要特别留意，服务器会做检查：
# 1、User-Agent
# 2、Content-Type：使用REST接口时，服务器会检查该值，用来确定HTTP Body中
# 的内容怎么解析。在使用服务器提供的RESTful或SOAP服务时，Content-Type设置
# 错误会导致服务器拒绝服务。
# 常见取值：
# application/xml(在XML RPC，如RESTful/SOAP调用时使用)
# application/json (JSON RPC)
# application/x-www-form-urlencoded(浏览器提交web表单时使用)
# Referer:服务器有时会检查防盗链

# Cookie处理
# 使用CookieJar函数进行Cookie的管理
# cookie = cookiejar.CookieJar()
# opener = request.build_opener(request.HTTPCookieProcessor(cookie))
# response = opener.open('http://www.zhihu.com')
# for item in cookie:
#     print(item.name + ':' + item.value)
# 自己添加Cookie的内容，可以通过设置请求头的Cookie域来做
# opener = request.build_opener()
# opener.addheaders.append(('Cookie', 'email=' + 'xxxxxx@163.com'))
# req = request.Request('http://www.zhihu.com/')
# response = opener.open(req)
# print(response.headers)
# retdata = response.read()

# Timeout设置超时
# url = 'http://www.zhihu.com/'
# req = request.Request(url)
# response = request.urlopen(req, timeout=2)
# html = response.read()
# print(html)

# # 获取HTTP响应码
# try:
#     response = request.urlopen('http://google.com')
#     print(response)
# except request.HTTPError as e:
#     if hasattr(e, 'code'):
#         print('Error code:', e.code)

# 重定向
# 要检测是否发生了重定向动作，只要检车以下Response的URL和Request的URL是否一致
# response = request.urlopen('http://www.zhihu.com')
# isRedirected = response.geturl() == 'http://www.zhihu.com'
# print(isRedirected)
# 如果不想自动重定向，可以自定义HTTPRedirectHandler类
# class RedirectHandler(request.HTTPRedirectHandler):
# 	def http_error_301(self, req, fp, code, msg, headers):
# 		pass
# 	def http_error_302(self, req, fp, code, msg, headers):
# 		result = request.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
# 		result.status = code
# 		result.newurl = result.geturl()
# 		return result
# opener = request.build_opener(RedirectHandler)
# opener.open('http://www.zhihu.com')

# Proxy的设置
# urllib默认使用环境变量http_proxy来设置HTTP Proxy，但我们一般不采用这种方式，而是
# 使用ProxyHandler在程序中动态设置代理
# proxy = request.ProxyHandler({'http':'127.0.0.1:8087'})
# opener = request.build_opener([proxy,])
# request.install_opener(opener)
# response = request.urlopen('http://www.zhihu.com')
# print(response.read())
# install_opener()会设置全局opener，之后所有HTTP访问都会使用这个代理
# 使用不同的Proxy，直接调用opener的open方法代替全局的URLopen方法
# proxy = request.ProxyHandler({'http':'127.0.0.1:8087'})
# opener = request.build_opener(proxy, )
# response = opener.open('http://www.zhihu.com')
# print(response.read())


# httplib
# ....


# 更人性化的Requests
# 首先实现一个完整的请求与相应模型
# GET请求
# r = requests.get('http://www.baidu.com')
# print(r.content)
# POST请求
# postdata = {'key':'value'}
# r = requests.post('http://www.xxxx.com/login', data=postdata)
# print(r.content)
# HTTP中的其他请求方式也可以用Requests来实现
# r = requests.put('http://www.xxxx.com/put', data={'key':'value'})
# r = requests.delete('http://.../delete')
# r = requests.head('.../get')
# r = requests.options('.../get')
# 网址+？+参数
# Requests提供了除完整的URL带入之外的方式
# http://zzk.cnblogs.com/s/blogpost?Keywords=blog:qiyeboy&pageindex=1
# payload = {'keywords':'blog:qiyeboy', 'pageindex':1}
# r = requests.get('http://zzk.cnblogs.com/s/blogpost', params=payload)
# print(r.url)

# 响应与编码
# r = requests.get('http://www.baidu.com')
# print('content-->' + r.content)
# print('text-->' + r.text)
# print('excoding->' + r.encoding)
# r.encoding = 'utf-8'
# print('new text-->' + r.text)
# content返回的是字节形式，text返回的是文本形式，encoding是猜测网页的编码
# Requests设置编码格式的更简便的方式：chardet,这是一个非常优秀的字符串/文件
# 编码检测模块
# 使用chardet.detect()返回字典，其中confidence是检测精确度，encoding是编码形式
# r = requests.get('http://www.baidu.com')
# print(chardet.detect(r.content))
# r.encoding = chardet.detect(r.content)['encoding']
# print(r.text)
# 除了上述直接获取全部响应的方式，还有一种流模式
# r = requests.get('http://www.baidu.com', stream=True)
# print(r.raw.read(10))

# 请求头headers处理
# user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36' \
#              '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
# headers = {'User-Agent':user_agent}
# r = requests.get('http://www.baidu.com', headers=headers)
# print(r.content)

# 响应码code和响应头headers处理
# 获取响应吗码的是使用Requests中的status_code字段，获取响应头使用Requests中的
# headers字段
# r = requests.get('http://www.baidu.com')
# if r.status_code == requests.codes.ok:
# print(r.status_code)
# print(r.headers)
# 推荐这种方式
# print(r.headers.get('content-type'))
# 不推荐这种方式
# 	print(r.headers['content-type'])
# else:
# 	r.raise_for_status()
# r.raise_for_status()是用来主动地产生一个异常，当响应码是4XX或5XX时，会抛出异常，
# 为200时，返回None

# Cookie处理
# user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36' \
#              '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
# headers = {'User-Agent': user_agent}
# r = requests.get('http://www.baidu.com', headers=headers)
# 遍历出所有的cookie字段的信息
# for cookie in r.cookies.keys():
#     print(cookie + ':' + r.cookies.get(cookie))
# 自定义Cookie值发送出去，使用以下方式
# user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36' \
#              '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
# headers = {'User-Agent': user_agent}
# cookies = dict(name='qiye', age='10')
# r = requests.get('http://www.baidu.com', headers=headers, cookies=cookies)
# print(r.text)
# 还有一种更高级的，且能自动处理Cookie的方式
# Requests提供了一个session的概念，在连续访问网页，处理登录跳转时特别方便，不需要关注细节
# loginUrl = 'http://www.xxxx.com/login'
# s = requests.Session()
# 首先访问登录界面，作为游客，服务器会先分配一个cookie
# r = s.get(loginUrl, allow_redirects=True)
# datas = {'name':'qiye', 'passwd':'qiye'}
# 向登录链接发送post请求，验证成功，游客权限转为会员权限
# r = s.post(loginUrl, data=datas, allow_redirects=True)
# print(r.text)

# 重定向与历史信息
# 处理重定向只需要设置一下allow_redirects字段即可
# 如果允许重定向，r.history字段查看历史信息

# 超时设置
# 通过参数timeout设置
# requests.get(url, timeout=2)

# 代理设置
# 可以为任意请求方法通过设置proxies参数来配置单个请求
# proxies = {'http':'http://0.10.1.10:3128',
# 			'https':'http://10.10.1.10:1080'}
# requests.get(url, proxies=proxies)
# 也可以通过环境变量HTTP_PROXY和HTTPS_PROXY配置，在爬虫开发不常用
# 你的代理需要使用HTTP Basic Auth，可以使用http://user:password@host/语法：
# proxies = {"http":"http://user:pass@10.10.1.10:3128",}