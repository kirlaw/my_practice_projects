#!/usr/bin/python3
# author eloise

import numpy as np
from matplotlib import pyplot as plt

us_file_path = "./data/USvideos.csv"
uk_file_path = "./data/GBvideos.csv"

t_uk = np.genfromtxt(uk_file_path, delimiter=",",
                     dtype='int',
                     skip_header=1,  # 跳过前n行
                     usecols=(6, 8),
                     # usecols=('likes', 'comment_total'),
                     encoding='ansi',
                     invalid_raise=False,  # 跳过出错行
                     missing_values='',
                     comments=None  # 默认为#，#之后的字符都被忽略
                     )
t_uk = t_uk[t_uk[:, 1] > -1]
t_uk = t_uk[t_uk[:, 0] > -1]
t_uk = t_uk[t_uk[:, 0] < 500000]
t_uk_like = t_uk[:, 0]
t_uk_comment = t_uk[:, 1]
# print(t_uk_like[:7])

plt.figure(figsize=(20, 8), dpi=80)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.scatter(t_uk_like, t_uk_comment)
plt.xlabel('点赞数')
plt.ylabel('评论数')
plt.title('英国YouTube视频点赞数和评论数')
# 不使用科学计数法
plt.ticklabel_format(style='plain')
plt.show()
