import csv
from datetime import datetime

from matplotlib import pyplot as plt

filename='sitka_weather_07-2014.csv'
with open(filename) as f:
    reader=csv.reader(f)
    reader_row=next(reader)
    # 第一行包括文件头，指出相应列名，并存储在列表中,打印索引和列名
    # for index,column_header in enumerate(reader_row):
        # print(index,column_header)

    # 从第二行开始读取每一行的第一、二列，即日期和最高温度，并存储到列表
    highs,dates=[],[]
    for row in reader:
        dates.append(datetime.strptime(row[0],'%Y-%m-%d'))
        highs.append(int(row[1]))
    print(highs)

    # 把日期和时间绘成图表
    fig=plt.figure(dpi=128,figsize=(10,6))
    plt.plot(dates,highs,c='red')
    plt.title('Daily high temperautures,July 2014',fontsize=24)
    plt.xlabel('',fontsize=16)
    # 绘制横坐标的斜标签，没有的话标签会重叠
    fig.autofmt_xdate()
    plt.ylabel('Temperature(F)',fontsize=16)
    plt.tick_params(axis='both',which='major',labelsize=16)
    plt.show()