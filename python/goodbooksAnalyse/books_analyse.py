#!/usr/bin/python3
# author eloise
# 统计图书出版年份与数量及评分的关系

import pandas as pd
from matplotlib import pyplot as plt

file_path = './books_data/books.csv'

df = pd.read_csv(file_path, encoding='ansi')

# 去除有NAN的行
data = df[pd.notnull(df['original_publication_year'])]
data = data[data['original_publication_year'] > 1975]

# 按年份算书的均分
grouped = data['average_rating'].groupby(data['original_publication_year']).mean()
# 按年份算书的数量
grouped1 = data.groupby(data['original_publication_year']).count()['book_id']

year = grouped.index
rating = grouped.values
year1 = grouped1.index
books_num = grouped1.values

plt.rcParams['font.sans-serif'] = ['SimHei']
fig = plt.figure(figsize=(15, 8))
# （xxx）这里前两个表示几*几的网格，最后一个表示第几子图
ax1 = fig.add_subplot(111)
ax1.plot(range(len(year)), rating, color='black', alpha=0.8, marker='.', label='平均评分')
for i, (_x, _y) in enumerate(zip(range(len(year)), rating)):
    plt.text(_x, _y, round(rating[i], 3), color='black', fontsize=10)
# 图例
ax1.legend(loc='upper left')
# y轴取值范围
ax1.set_ylim([3.95, 4.11])
# 次坐标轴
ax2 = ax1.twinx()

plt.bar(range(len(year1)), books_num, alpha=0.3, label='数量')
plt.xticks(list(range(len(year))), year.astype(int))
plt.legend(loc=1)
plt.show()
