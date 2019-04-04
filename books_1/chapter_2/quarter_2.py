import pandas as pd


# MovieLens 1M数据集
# 本数据集是从20世纪90年代末至21世纪初由movieLens用户提供的电影评分数据
# 包括电影评分、电影元数据（风格类型和年代）以及关于用户的人口统计学数据（年龄、邮编、性别和职业等）
# 基于机器学习算法的推荐系统一般都会对此类数据感兴趣
# 含有来组6000名用户对4000部电影的100万条评分数据
# 分为三个表：评分、用户信息和电影信息
# 通过pandas.read_table将各个表分别读到一个pandas DataFrame对象中
unames = ['user_id', "gender", 'age', 'occuption', 'zip']
users = pd.read_table('E:/Data-analysis/books_1/datasets/movielens/users.dat',
                      sep='::', header=None, names=unames, engine='python')
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('E:/Data-analysis/books_1/datasets/movielens/ratings.dat',
                        sep='::', header=None, names=rnames, engine='python')
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('E:/Data-analysis/books_1/datasets/movielens/movies.dat',
                       sep='::', header=None, names=mnames, engine='python')
# 利用Python的切片语法，通过查看每个DataFrame的前几行即可验证数据加载工作是否顺利
# print(users[:5])
# print(ratings[:5])
# print(movies[:5])
# 其中的年龄和职业是以编码形式给出的，它们的具体含义参考README文件
# 假设想要根据性别和年龄计算某部电影的平均得分，把所有数据都合并到一个表中就简单了
# 先用pandas的merge函数将ratings跟users合并到一起，然后在将movies也合并进去
# pandas会根据列名的重叠情况推断出哪些列是合并（或连接）键
data = pd.merge(pd.merge(ratings, users), movies)
# print(data[:5])
# print(data.ix[0])
# 为了按性别计算每部电影的平均得分，我们也可以使用pivot_table方法
mean_ratings = data.pivot_table('rating', index='title',
                                columns='gender', aggfunc='mean')
# print(mean_ratings[:5])
# gender                                F         M
# title
# $1,000,000 Duck (1971)         3.375000  2.761905
# 'Night Mother (1986)           3.388889  3.352941
# 'Til There Was You (1997)      2.675676  2.733333
# 'burbs, The (1989)             2.793478  2.962085
# ...And Justice for All (1979)  3.828571  3.689024

# 过滤掉评分数据不够250条的电影
# 需要先对title进行分组，利用size()得到一个含有各电影分组大小的Series对象
ratings_by_title = data.groupby('title').size()
# print(ratings_by_title[:5])
active_titles = ratings_by_title.index[ratings_by_title >= 250]
# print(active_titles[:5])
# Index([''burbs, The (1989)', '10 Things I Hate About You (1999)',
#        '101 Dalmatians (1961)', '101 Dalmatians (1996)',
#        '12 Angry Men (1957)'],
#       dtype='object', name='title')
# 该索引含有评分数据大于250条的电影名称，然后我们就可以根据之前的mean_ratings选取所需的行了
mean_ratings = mean_ratings.ix[active_titles]
# print(mean_ratings)
# 为了了解女性观众最喜欢的电影，可以对F列降序排列
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)
# print(top_female_ratings[:5])
# 计算评分分歧
# 找出男女观众分歧最大的电影
# 一个办法是给mean_ratings加上一个用于存放平均得分之差的列，并排序
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_values(by='diff')
# print(sorted_by_diff[:5])
# 对排序结果反序并取出前15行，得到的则是男性观众更喜欢的电影
# print(sorted_by_diff[::-1][:15])
# 如果只是想找出分歧最大的电影，可以计算得分数据的方差或标准差
rating_std_by_title = data.groupby('title')['rating'].std()
rating_std_by_title = rating_std_by_title.ix[active_titles]
print(rating_std_by_title.sort_values(ascending=False)[:10])
# 电影分类是以竖线分隔的字符串形式给出的，如果想对电影分类进行分析的话，需要先转换成更有用的形式
