

import requests
import aiohttp
import asyncio #这个包不需要另外下
from bs4 import BeautifulSoup
from urllib import parse
import time
from pyquery import PyQuery as pq  #获取整个网页的源代码
from collections import OrderedDict
import lxml
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from pyquery import PyQuery as pq  #获取整个网页的源代码
import pandas as pd

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}
browser = webdriver.Firefox()
wait = WebDriverWait(browser,10)

def get_tianmao_header(url):
    browser.get(url)
    # wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item'))) #加载所有宝贝
    html = browser.page_source
    doc = pq(html)
    # print(doc)
    info = OrderedDict()  # 存放该商品所具有的全部信息
    items = doc('#page')

    # info['店铺名'] = items.find('.slogo').find('.slogo-shopname').text()
    # info['ID'] = items.find('#LineZing').attr['itemid']
    info['宝贝'] = items.find('.tb-detail-hd').find('h1').text()
    info['促销价'] = items.find('#J_PromoPrice').find('.tm-promo-price').find('.tm-price').text()
    info['原价'] = items.find('#J_StrPriceModBox').find('.tm-price').text()
    # '月销量' :items.find('.tm-ind-panel').find('.tm-ind-item tm-ind-sellCount').find('.tm-indcon').find('.tm-count').text(),
    info['月销量'] = items.find('.tm-ind-panel').find('.tm-indcon').find('.tm-count').text().split(' ', 2)[0]
    info['累计评价'] = items.find('#J_ItemRates').find('.tm-indcon').find('.tm-count').text()
    print(info)
    return info

def get_taobao_header(url):
    html = requests.get(url,headers=headers)

    # doc = pq(html.text)
    # print(doc)
    # soup = BeautifulSoup(html, 'lxml')


    # items = doc('#page')

    # print(items)
    # info['店铺名'] = items.find('.tb-shop-seller').find('.tb-seller-name').text()
    # info['ID'] = items.find('#J_Pine').attr['data-itemid']
    # info['宝贝'] = items.find('#J_Title').find('h3').text()
    # info['原价'] = items.find('#J_StrPrice').find('.tb-rmb-num').text()
    # info['价格'] = soup.select_one(class_='tm-price')
    # # '月销量' :items.find('.tm-ind-panel').find('.tm-ind-item tm-ind-sellCount').find('.tm-indcon').find('.tm-count').text(),
    # info['月销量'] = items.find('#J_SellCounter').text()
    # info['累计评价'] = items.find('#J_RateCounter').text()
    # print(info)
    # return info

async def get_html(url):
    print('正在爬取：',url)
    # 请求获取网页源代码
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status==200:
                # 获取内容，在阻塞的地方标记await
                time.sleep(1)
                parse_html(await resp.text())
            else:
                print('ERROR',resp.status)
            return

def parse_html(html):

    with open ('../test.py', 'w') as f:
        f.write(html)

    # soup = BeautifulSoup(html, 'lxml')
    # info = OrderedDict()  # 存放该商品所具有的全部信息
    # info['价格'] = soup.select_one('.tm-price').text
    # print(info)
    # with open('test.py','r') as f:
    #
    #     soup=BeautifulSoup(f,'lxml')
    #     info = OrderedDict()  # 存放该商品所具有的全部信息
    #     # info['价格'] = soup.select_one('.tm-promo-price').text
    #     print(soup.select("[class~=tm-price]"))



if __name__=='__main__':
    start=time.time()
    url='https://detail.tmall.com/item.htm?&spm=a230r.1.14.14.da8d5473NnQdPO&id=588700982071&ad_id=&am_id=&cm_id=140105335569ed55e27b&pm_id=&abbucket=8'
    get_tianmao_header(url)


    # urls = ['https://detail.tmall.com/item.htm?&spm=a230r.1.14.14.da8d5473NnQdPO&id=588700982071&ad_id=&am_id=&cm_id=140105335569ed55e27b&pm_id=&abbucket=8']
    # tasks = []
    # for url in urls:
    #     tasks.append(get_html(url))
    #
    # loop = asyncio.get_event_loop()
    # # 等待tasks任务列表全部执行完，
    # loop.run_until_complete(asyncio.wait(tasks))
    # loop.close()

    print(time.time() - start)