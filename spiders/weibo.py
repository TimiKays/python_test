import requests
from bs4 import BeautifulSoup
from urllib import parse
import time
# 常规单线程同步爬虫
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}

def get_html(url):
    # 获取网页源代码
    html=requests.get(url,headers=headers)
    if html.status_code==200:
        # 获取内容
        parse_html(html.text)
    else:
        print('ERROR',html.status_code)
    return

def parse_html(html):
    soup=BeautifulSoup(html,'lxml')
    trs=soup.select('table tbody tr')
    for tr in trs:
        # 获取a标签里的内容
        title=tr.select_one('td a').text
        # 获取a标签的属性href
        url=tr.select_one('td a')['href']
        # 补全地址
        url=parse.urljoin('https://s.weibo.com',url)
        print(title+url)


if __name__=='__main__':
    start=time.time()
    url='https://s.weibo.com/top/summary'
    get_html(url)
    url2='https://s.weibo.com/top/summary?cate=socialevent'
    get_html(url2)
    print(time.time()-start)