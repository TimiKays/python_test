import requests
import time
from bs4 import BeautifulSoup
import os
from uuid import uuid4

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}


def get_html(url):
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        # 获取内容
        print('连接成功')
        parse_html(html.text)
    else:
        print('ERROR', html.status_code)
    return


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    books = soup.select('li.subject-item')
    for book in books:
        # 获取书名
        title = book.select_one('div.info h2 a').text.strip().replace('\n', '').replace(' ', '')
        # 获取作者
        author = book.select_one('.pub').text.strip().replace('\n', '').replace(' ', '')
        # 获取简介
        brif = book.select_one('p')
        if not brif:
            # 有的简介为空，就手动赋值
            brif = '无简介'
        else:
            brif = brif.text.strip().replace('\n', '').replace(' ', '')

        # 获取图片
        img = book.select_one('.pic a img')['src']
        download(img, time.time())

        print(title, author, '\n\t', brif, img)
        print('-' * 20)


def download(imgurl, imgname):
    """图片下载的函数"""
    root_dir = 'doubanimg'

    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    html = requests.get(imgurl, headers=headers)
    with open(root_dir+'/{}.jpg'.format(imgname), 'wb') as file:

        file.write(html.content)


if __name__ == '__main__':
    start = time.time()
    number = 1
    # https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start=20&type=T
    for i in range(0, 200, 20):
        url = 'https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T'.format(i)
        print('正在获取第{}页数据'.format(number))
        get_html(url)
        number += 1

    print(time.time() - start)
