import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import json
import matplotlib.pyplot as plt


# 示例：USDA食品数据库
# 每种食物都带有若干标识性属性以及两个有关营养成分和分量的列表
# 这种形式的数据不是很适合分析工作，因此我们需要做一些规整化以使其具有更好用的形式

# 可以用任何喜欢的JSON库将其加载到Python中
# 使用Python内置的json模块
db = json.load(open('e:/datasets/usda_food/database.json'))
print(len(db))
# db中的每个条目都是一个含有某种食物全部数据的字典
# nutrients字段是一个字典列表，其中的每个字典对应一种营养成分
print(db[0].keys())
print(db[0]['nutrients'][0])
nutrients = DataFrame(db[0]['nutrients'])
print(nutrients[:7])
# 在将字典列表转换为DataFrame时，可以只抽取其中的一部分字段
# 我们将取出食物的名称、分类、编号以及制作商等信息
info_keys = ['description', 'group', 'id', 'manufacturer']
info = DataFrame(db, columns=info_keys)
print(info[:5])
print(info)
# 通过value_counts，你可以查看食物类别的分布情况
print(pd.value_counts(info.group)[:10])
# 现在，为了对全部营养数据做一些分析，最简单的办法是将所有食物的营养成分整合到一个大表中
# 我们分几个步骤来实现该目的
# 首先，将各食物的营养成分列表转换为一个DataFrame，并添加一个表示编号的列，
# 然后将该DataFrame添加到一个列表中
# 最后通过concat将这些东西连接起来就可以了
nutrients = []
for rec in db:
    fnuts = DataFrame(rec['nutrients'])
    fnuts['id'] = rec['id']
    nutrients.append(fnuts)
nutrients = pd.concat(nutrients, ignore_index=True)
# 如果一切顺利的话，nutrients应该是下面这样的
print(nutrients)
# 我们发现这个DataFrame中无论如何都会有一些重复项，所以直接丢弃就可以了
print(nutrients.duplicated().sum())
nutrients = nutrients.drop_duplicates()
# 由于两个DataFrame对象中都有“group”和“description”，所以为了明确到底谁是谁
# 需要对它们进行重命名
col_mapping = {'description': 'food', 'group': 'fgroup'}
info = info.rename(columns=col_mapping, copy=False)
print(info)
col_mapping = {'description': 'nutrient', 'group': 'nutgroup'}
nutrients = nutrients.rename(columns=col_mapping, copy=False)
print(nutrients)
# 做完这些事情之后，就可以将info和nutrients合并起来
ndata = pd.merge(nutrients, info, on='id', how='outer')
print(ndata)
print(ndata.ix[3000])
# 根据食物分类和营养类型画出一张中位值图
result = ndata.groupby(['nutrient', 'fgroup'])['value'].quantile(0.5)
result['Zinc, Zn'].order().plot(kind='barh')
plt.show()
# 只要稍微动一动脑子，就可以发现各营养成分最为丰富的食物是什么了
by_nutrient = ndata.groupby(['nutgroup', 'nutrient'])


def get_maximum(x): return x.xs(x.value.idxmax())


def get_minimum(x): return x.xs(x.value.idxmin())


max_foods = by_nutrient.apply(get_maximum)[['value', 'food']]
# 让food小一点
max_foods.food = max_foods.food.str[:50]
# 由于得到的DataFrame很大，不方便全部打印出来
print(max_foods.ix['Amino Acids']['food'])
