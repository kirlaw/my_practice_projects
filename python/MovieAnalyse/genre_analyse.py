#!/usr/bin/python3
# author eloise

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

file_path = './IMDB-Movie-Data.csv'
df = pd.read_csv(file_path)

temp_list = df['Genre'].str.split(',').tolist()
genre_list = list(set(i for j in temp_list for i in j))

zeros_df = pd.DataFrame(np.zeros((df.shape[0], len(genre_list))),
                        columns=genre_list)
# 统计每个电影对应的标签
for i in range(df.shape[0]):
    zeros_df.loc[i, temp_list[i]] = 1

# 每个分类电影的数量
genre_count = zeros_df.sum()
_x = genre_count.index
_y = genre_count.values

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(15, 8))
rects = plt.bar(range(len(_x)), _y)
plt.xticks(range(len(_x)), _x)
plt.xlabel('电影类型')
plt.ylabel('电影数量')
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height + 2, str(height), ha='center')
plt.show()
