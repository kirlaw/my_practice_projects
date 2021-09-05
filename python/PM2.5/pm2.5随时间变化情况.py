#!/usr/bin/python3
# author eloise

import pandas as pd
from matplotlib import pyplot as plt

bej_file_path = './data/BeijingPM20100101_20151231.csv'
ctu_file_path = './data/ChengduPM20100101_20151231.csv'
snh_file_path = './data/ShanghaiPM20100101_20151231.csv'
gnz_file_path = './data/GuangzhouPM20100101_20151231.csv'
shy_file_path = './data/ShenyangPM20100101_20151231.csv'

bej_df = pd.read_csv(bej_file_path)
ctu_df = pd.read_csv(ctu_file_path)
snh_df = pd.read_csv(snh_file_path)
gnz_df = pd.read_csv(gnz_file_path)
shy_df = pd.read_csv(shy_file_path)

# 将数据中的分离的时间字段重组为时间序列
period = pd.PeriodIndex(year=bej_df['year'], month=bej_df['month'], day=bej_df['day'], hour=bej_df['hour'], freq='H')

bej_df['datetime'] = period
ctu_df['datetime'] = period
snh_df['datetime'] = period
gnz_df['datetime'] = period
shy_df['datetime'] = period

# 将datetime指定为index
bej_df.set_index('datetime', inplace=True)
ctu_df.set_index('datetime', inplace=True)
snh_df.set_index('datetime', inplace=True)
gnz_df.set_index('datetime', inplace=True)
shy_df.set_index('datetime', inplace=True)

# 取1个月的均值
bej_df = bej_df.resample('M').mean()
ctu_df = ctu_df.resample('M').mean()
snh_df = snh_df.resample('M').mean()
gnz_df = gnz_df.resample('M').mean()
shy_df = shy_df.resample('M').mean()

# 取US检测的数据
bej_data = bej_df['PM_US Post']
ctu_data = ctu_df['PM_US Post']
snh_data = snh_df['PM_US Post']
gnz_data = gnz_df['PM_US Post']
shy_data = shy_df['PM_US Post']

_x_bej = [i.strftime('%Y%m%d') for i in bej_data.index]
_x_ctu = [i.strftime('%Y%m%d') for i in ctu_data.index]
_x_snh = [i.strftime('%Y%m%d') for i in snh_data.index]
_x_gnz = [i.strftime('%Y%m%d') for i in gnz_data.index]
_x_shy = [i.strftime('%Y%m%d') for i in shy_data.index]

_y_bej = bej_data.values
_y_ctu = ctu_data.values
_y_snh = snh_data.values
_y_gnz = gnz_data.values
_y_shy = shy_data.values

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(20, 8))
plt.plot(range(len(_x_bej)), _y_bej, label='北京')
plt.plot(range(len(_x_ctu)), _y_ctu, label='成都')
plt.plot(range(len(_x_snh)), _y_snh, label='上海')
plt.plot(range(len(_x_gnz)), _y_gnz, label='广州')
plt.plot(range(len(_x_shy)), _y_shy, label='沈阳')
plt.xticks(range(0, len(_x_bej), 3), list(_x_bej)[::3])
plt.legend()
plt.xlabel('日期')
plt.ylabel('PM2.5浓度(ug/m^3)')
plt.title('五地2010-2015年PM2.5变化趋势')
plt.show()
