#!/usr/bin/python3
# author eloise

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

file_path = "./directory.csv"

df = pd.read_csv(file_path, encoding='ansi')

china_data = df[df["Country"] == "CN"]

grouped = china_data.groupby(by="City").count()['Brand']
# 统计店铺数最多的15个城市
city_data = grouped.sort_values(ascending=False)[:15]

plt.rcParams['font.sans-serif'] = ['SimHei']

_x = city_data.index
_y = city_data.values

plt.figure(figsize=(15, 8))
rects = plt.bar(range(len(_x)), _y)
plt.xticks(range(len(_x)), _x)
plt.xlabel('城市')
plt.ylabel('店铺数量')
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height + 2, str(height), ha='center')
plt.title('中国星巴克店铺最多的15个城市')
plt.show()
