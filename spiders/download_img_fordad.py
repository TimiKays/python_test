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
    books = soup.select('.react-swipe-container span')
    print(len(books),books)
    img_num=1
    for book in books:
        # 获取书名
        # title = book.select_one('react-swipe-container').text.strip().replace('\n', '').replace(' ', '')
        # # 获取作者
        # author = book.select_one('.pub').text.strip().replace('\n', '').replace(' ', '')
        # # 获取简介
        # brif = book.select_one('p')
        # if not brif:
        #     # 有的简介为空，就手动赋值
        #     brif = '无简介'
        # else:
        #     brif = brif.text.strip().replace('\n', '').replace(' ', '')

        # 获取图片
        # book = book.select_one('url')
        # print('img:',book)

        left=str(book).find('"')
        right=str(book).rfind('"')
        # print(left,right)
        # left=img.index('"')
        # print(left)
        # right=img.rfind('"')
        img_url=str(book)[left+1:right-13]
        print(img_url)

        download(img_url, img_num)
        img_num+=1
        # print(title, author, '\n\t', brif, img)
        # print('-' * 20)


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
    filename = 'F:\python\practice\spiders\img.html'
    try:
        fp=open(filename,'r', encoding="utf-8")
        html=fp.read()
        fp.close()
    except IOError:
        print("文件打开失败")
    else:
        parse_html(html)
        print("完成下载")


    print(time.time() - start)
