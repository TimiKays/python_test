import datetime

import requests
from bs4 import BeautifulSoup
import traceback
import re
import pandas as pd


def get_html(url,encode='utf-8'):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=encode
        return r.text
    except:
        traceback.print_exc()


# 得到股票列表：名称、代码、url组成的字典，并加入到list
def get_stock_list(url,list):
    html=get_html(url)

    soup=BeautifulSoup(html,'html.parser')
    sec=soup.find('section','stockTable')('a')

    for i in sec:
        try:
            stock={}
            href=i.attrs['href']
            stock['url']=href
            match=re.search(r'[S][ZH]\d{6}',href)
            if match:
                stock['code']=match.group(0)

            name=re.match(r'[\u4e00-\u9fa5a-zA-Z\s\*]*',i.string)
            stock['name']=name.group(0)
            list.append(stock)
        except:
            traceback.print_exc()
            continue
    print(list)

def get_stock_info(url,path):
    # 读取文件
    stocks=pd.read_csv(path)
    # 获取第一行
    # print(stocks.loc[0])

    # 得到所有的链接和股票名称
    urls=stocks.url
    names=stocks.name
    stocks_list=[]
    keys = ['今收', '增长幅度', '增长率']

    for i in range(len(urls)):
        # if i >=50:
        #     break
        print('正在爬取第{}个...'.format(i))
        try:
            # 获取网页，生成soup对象
            html=get_html(urls[i])
            soup=BeautifulSoup(html,'html.parser')

            # 页面中的第一个section标签就是我要的
            section=soup.section

            # 键只需要获得一次
            if (i == 0):
                for dt in section('dt'):
                    keys.append(dt.string)
                keys[17] = '市盈率(动)'
                print(keys)

            # 数据值分别在em和dd中
            values = []
            for em in section(['em','dd']):
                values.append(em.string)

             # 加入名称列。把键值两个列表合成一个字典
            socket={'name':names[i]}
            for ii in range(len(keys)):
                socket[keys[ii]]=values[ii]
            # 把字典加入到列表中，一个字点代表一个股票
            stocks_list.append(socket)
        except:
            traceback.print_exc()
            continue

    # 把列表保存到csv文件
    df=pd.DataFrame(stocks_list)
    # 把两个db 拼合成一个
    combine=pd.merge(stocks,df,on='name')
    now = datetime.datetime.now()
    combine.to_excel('股票信息_{}年{}月{}日.xls'.format(now.year,now.month,now.day),index=0)



if __name__ == '__main__':
    list_url='https://hq.gucheng.com/gpdmylb.html'
    start_url='https://hq.gucheng.com'  #/SZ000001/
    path='stock_list.csv'
    list=[]

    # # 获得股票列表
    # get_stock_list(list_url,list)
    # # 保存到csv文件
    # df=pd.DataFrame(list,columns=['url','code','name'])
    # df.to_csv(path)

    # 解析单个股票信息
    get_stock_info(start_url,path)