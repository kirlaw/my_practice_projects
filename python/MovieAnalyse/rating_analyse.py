#!/usr/bin/python3
# author eloise

import pandas as pd
from matplotlib import pyplot as plt

file_path = './IMDB-Movie-Data.csv'
df = pd.read_csv(file_path)

rating_data = df['Rating'].values
max_rating = rating_data.max()
min_rating = rating_data.min()
group = (max_rating - min_rating) // 0.5

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(15, 8))
plt.hist(rating_data, int(group))

_x = [min_rating]
i = min_rating
while i < max_rating + 0.5:
    i += 0.5
    _x.append(i)

plt.xticks(_x)
plt.xlabel('评分')
plt.ylabel('电影数量')
plt.show()
