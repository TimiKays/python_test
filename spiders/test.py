# -*- coding: UTF-8 -*-


import pandas as pd

#----------lambda------------
# a = map(lambda x: x * x, [1, 2, 3, 4, 5, 6])
# print(list(a))  # 将map对象转换为list，并打印出结果

# a=map(lambda x,y:x+y,[1,2],[2,3])
# print(list(a))
#---------替换轴索引------------
# 创建一个三行四列的矩阵
# data = pd.DataFrame(np.arange(12).reshape((3, 4)), index=['Ohio', 'Colorado', 'New York'],columns=['one', 'two', 'three', 'four'])
# print(data)
#
# # 与Series类似，轴索引也有一个map方法：
# # 定义一个transform方法
# # transform = lambda x: x[:4].upper()
# # # 你可以赋值给index，修改DataFrame：
# # data.index = data.index.map(transform)
# # print(data)
#
# #rename方法
# print(data.rename(index=str.title,columns=str.upper))
# print(data)

#-------------------分箱-------------------
# ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
# # 让我们将这些年龄分为18～25、26～35、36～60以及61及以上等若干组。为了实现这个，你可以使用pandas中的cut：
# bins = [18, 25, 35, 60, 100]
# cats = pd.cut(ages, bins)
# print(cats.codes)

# ---------------qcut分箱---------------------
# data=np.random.randn(1000)
# print(data)
# data2=pd.qcut(data,[0,0.1,0.5,0.8,1])
# print(data2)
# print(pd.value_counts(data2))

# ---------------request库性能测试-------------------
import requests
import time

# 爬100次百度首页时间
# url='https://www.baidu.com/'
# start_time=time.time()
# def getHTMLText(url):
#     try:
#         r=requests.get(url)
#         r.raise_for_status()
#         r.encoding=r.apparent_encoding
#         return '爬到了！'
#     except:
#         return r.status_code
#
# for i in range(100):
#     print('第{}次爬取'.format(i))
#     print(getHTMLText(url))
# print('使用时长：',time.time()-start_time)
# # 使用时长： 20.4632465839386



# d={}
# for i in range(26):
#     d[chr(i+ord('a'))]=chr((i+13)%26 +ord('a'))
# for c in 'Python':
#     print(d.get(c,c),end="")

