import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import requests
import json


# 使用HTML和Web API
# 许多网站都有一些通过JSON或其他格式提供数据的公共API
# 通过Python访问这些API的办法有不少
# 一个简单易用的办法是requests包
# 为了在Twitter上搜索"python pandas"，可以发送一个HTTP GET请求
url = 'http://search.twitter.com/serach.json?q=python%20pandas'
resp = requests.get(url)
print(resp)
# Response对象的text属性含有GET请求的内容
# 许多Web API返回的都是JSON字符串，我们必须将其加载到一个Python对象
data = json.loads(resp.text)
print(data.keys())
# 响应结果中的results字段含有一组tweet，每天tweet被表示为一个Python
# 字典
# 可以用一个列表定义出感兴趣的tweet字段，然后将results列表传给
# DataFrame
tweet_fields = ['created_at', 'from_user', 'id', 'text']
tweets = DataFrame(data['results'], columns=tweet_fields)
print(tweets)
# 要向能够直接得到便于分析的DataFrame对象，只需再多费些精力创建出
# 对常见Web API的更高级接口即可
