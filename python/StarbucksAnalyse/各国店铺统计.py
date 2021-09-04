#!/usr/bin/python3
# author eloise

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

file_path = "./directory.csv"

df = pd.read_csv(file_path, encoding='ansi')

grouped = df.groupby(by="Country").count()['Brand']

plt.rcParams['font.sans-serif'] = ['SimHei']

_x = grouped.index
_y = grouped.values

plt.figure(figsize=(20, 8))
rects = plt.bar(range(len(_x)), _y)
plt.xticks(range(len(_x)), _x)
plt.xlabel('国家')
plt.ylabel('店铺数量')
for rect in rects:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width() / 2, height + 2, str(height), ha='center')
plt.title('各国星巴克店铺数对比')
plt.show()
