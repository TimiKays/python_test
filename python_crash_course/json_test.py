from __future__ import (absolute_import,division,print_function,unicode_literals)

import math
from urllib.request import urlopen
import requests
import json
import pygal

# json_url='http://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
# # ------用urlopen方式------
# # 获取数据
# response=urlopen(json_url)
# # 读取数据
# res=response.read()
# # 将数据写入文件
# with open('output\\btc_close_2017_urllib.json','wb') as f:
#     f.write(res)
# #将内容转换为python能处理的格式
# file_urllib=json.loads(res)
# # print(file_urllib)

# # ------用requests方式------
# req=requests.get(json_url)
# # 输出文件与之前的方式内容相同
# with open('output\\btc_close_2017_requests.json','w') as f:
#     f.write(req.text)
# #将内容转换为python能处理的格式
# file_requests=req.json()
# # 真的相同
# print(file_requests==file_urllib)

# 获取其中的具体数据
filename='output\\btc_close_2017_urllib.json'
with open(filename) as f:
    json_file = json.load(f)
dates=[]
months=[]
weeks=[]
weekdays=[]
closes=[]
for one_dict in json_file:
    date=one_dict['date']
    month=int(one_dict['month'])
    week=int(one_dict['week'])
    weekday=one_dict['weekday']
    close=int(float(one_dict['close']))
    # print('{} is month {} ,week {} ,{},the end price is {} RMB'.format(date,month,week,weekday,close))
    dates.append(date)
    months.append(month)
    weeks.append(week)
    weekdays.append(weekday)
    closes.append(close)

# # 绘制折线图
# # x坐标顺时针旋转20度，不用显示全部坐标
# line_chart=pygal.Line(x_label_rotation=20,show_minor_x_labels=False)
# line_chart.title='收盘价（￥）'
# line_chart.x_labels=dates
# # x坐标每20天显示一次
# N=20
# line_chart.x_labels_major=dates[::N]
# line_chart.add('收盘价',closes)
# line_chart.render_to_file('output\\收盘价折线图.svg')

# 绘制盘价对数变换折线图
line_chart=pygal.Line(x_label_rotation=20,show_minor_x_labels=False)
line_chart.title='收盘价对数变换（￥）'
line_chart.x_labels=dates
# x坐标每20天显示一次
N=20
line_chart.x_labels_major=dates[::N]
# 收盘价对数变换
close_log=[math.log10(l) for l in closes]

line_chart.add('收盘价对数变换',close_log)
line_chart.render_to_file('output\\收盘价对数变换折线图.svg')