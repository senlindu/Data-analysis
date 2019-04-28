import numpy as np 
import pandas as pd 
import sqlite3
import pymongo
import requests, json


# 使用数据库
# 在许多应用中，数据很少取自文本文件，因为用这种方式存储大量数据很低效
# 基于SQL的关系型数据库使用非常广泛
# 此外还有一些非SQL型数据库也变得非常流行
# 数据库的选择通常取决于性能、数据完整性以及应用程序的伸缩性需求
# 将数据从SQL加载到DataFrame的过程很简单
# 此外pandas还有一些能够简化该过程的函数
# 利用 使用一款嵌入式的SQLite数据库
query 'CREATE TABLE test (a VARCHAR(20), b CARCHAR(20), \
      c REAL, d INTEGER);'
con = sqlite3.connect(':memory:')
con.execute(query)
con.commit()
# 然后插入几行数据
# 从表中选取数据时，大部分Python SQL驱动器都会返回一个元组列表
# 你可以将这个元组列表传给DataFrame的构造器，但还学要列名
# cursor.description
# pandas有一个可以简化多次查询过程的read_frame函数(位于
# pandas.io.sql模块)。只需传入select语句和连接对象即可


# 存取MongoDB中的数据
# NoSQL数据库由许多不同的形式
# 有些是简单的字典式键值对存储，另一些是基于文档
# 存储在MongoDB中的文档被组织在数据库的集合中
# MongoDB服务器的每个运行实例可以有多个数据库，而每个数据库又
# 可以有多个集合
# 假设想保存之前通过Twitter API获取的数据
# 首先访问tweets集合
# tweets = con.db.tweets
# 然后将那组tweet加载进来并通过tweets.save（用于将Python字典写入
# MongoDB）逐个存入集合中
# url = "http://"
# data = json.loads(requests.get(url).text)
# for tweet in data['results']:
#         tweet.save(tweet)
# 如果想要从该集合中取出自己发的tweet，可以用下面的代码
# cursor = tweets.find({'from_user':'wesmckinn'})
# 返回的游标是一个迭代器，可以为每个文档产生一个字典
# 可以将其转换为一个DataFrame，此外还可以只获取各tweet的部分字段
# tweet_fields = ['created_at', 'from_user', 'id', 'text']
# result = DataFrame(list(cursor), columns=tweet_fields)