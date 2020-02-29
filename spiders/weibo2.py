import aiohttp
import asyncio #这个包不需要另外下
from bs4 import BeautifulSoup
from urllib import parse
import time

# 单线程异步爬虫

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}

# 在函数的地方标记async异步
async def get_html(url):
    print('正在爬取：',url)
    # 请求获取网页源代码
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status==200:
                # 获取内容，在阻塞的地方标记await
                parse_html(await resp.text())
            else:
                print('ERROR',resp.status)
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
    urls=['https://s.weibo.com/top/summary',
    'https://s.weibo.com/top/summary?cate=socialevent']
    tasks=[]
    for url in urls:
        tasks.append(get_html(url))

    loop =asyncio.get_event_loop()
    # 等待tasks任务列表全部执行完，
    loop.run_until_complete(asyncio.wait(tasks))
    print(time.time()-start)
    loop.close()