#!/usr/bin/python3
# author eloise

import pandas as pd
from matplotlib import pyplot as plt

file_path = './IMDB-Movie-Data.csv'

df = pd.read_csv(file_path)

time_data = df['Runtime (Minutes)'].values
print(time_data)
max_time = time_data.max()
min_time = time_data.min()
group_time = (max_time - min_time) // 5

# 可视化
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(15, 8))
plt.hist(time_data, group_time)
plt.xticks(range(min_time, max_time + 5, 5))
plt.xlabel('电影时长')
plt.ylabel('电影数量')
plt.show()
