import datetime
import urllib
import requests
import time
from bs4 import BeautifulSoup
import xlwt

"""
author:TimiKays
version:1.0
date:2020.4.10
"""
def get_html(url):
    # 获取网页
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        # 获取内容
        print('连接成功')
        parse_html(html.text)

    else:
        print('ERROR', html.status_code)
    return


def parse_html(html):
    # 解析网页
    soup = BeautifulSoup(html, 'lxml')
    webs = soup.find_all(class_='c-container')
    print(len(webs))

    for web in webs:
        #获取id
        id=web["id"]

        # 获取标题
        # results_a = web.find_all('a')
        title=web.a.text.strip().replace('\n', '').replace(' ', '')
        # print(title)

        # 获取链接
        link = web.a['href'].strip().replace('\n', '').replace(' ', '')
        # print(link)

        # 获取网站名
        # webname=web.find('a',class_="c-showurl")
        # webname=web.select('a[class="c-showurl"]').string
        webname=web.select_one(".c-showurl")
        if(webname):
            end=webname.text.rfind('}')
            webname=str(webname.text)[end+1:]
        else:
            webname="不明网站"

        # 封装数据
        result = []
        result.append(id)
        result.append(title)
        result.append(webname)
        result.append(link)
        # result['标题'] = title
        # result['网站名'] = webname
        # result['链接'] = urllib.parse.urlencode(link)
        results.append(result)




def save_to_excel(results):
    # 把数据保存到excel表格中
    # 通过pandas实现
    # df=pd.DataFrame(results)
    # df.to_excel("results.xlsx",sheet_name='Sheet1')

    #通过xlwt实现
    workbook=xlwt.Workbook(encoding='utf-8')
    worksheet=workbook.add_sheet('爬取结果',cell_overwrite_ok=True)
    worksheet.col(0).width=256*5
    worksheet.col(1).width = 256*50
    worksheet.col(2).width = 256*30

    tablehead=['id','标题','网站名']
    # 写表头
    for i in range(len(tablehead)):
        worksheet.write(0,i,tablehead[i])

    # 写内容
    for row in range(len(results)):
        for col in range(len(tablehead)):
            if(col==1):
                str='HYPERLINK("%s" ; "%s")'%( results[row][3], results[row][col])
                try:
                    worksheet.write(row + 1, col,xlwt.Formula(str))
                except Exception:
                    print("有一个问题,这里用无链接的")
                    worksheet.write(row + 1, col, results[row][col])
            else:
                worksheet.write(row+1,col,results[row][col])
    now=datetime.datetime.now()

    workbook.save('%s年%s月%s日爬取百度搜索%s结果%d条.xlsx'%(now.year,now.month,now.day,keyword,page*10))



if __name__ == '__main__':
    start = time.time()
    # https: // www.baidu.com / s?rtt = 1 & bsst = 1 & cl = 2 & tn = news & word = % E5 % A4 % A7 % E7 % 96 % 86
    baseUrl = 'http://www.baidu.com/s?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400'}

    # ----------------------关键词和页数在下面改-------------------------
    # 要多少页
    page = 3

    # 搜索的关键词,注意别把引号去掉了！
    keyword = '大疆'
    # -----------------------关键词和页数在上面改------------------------

    results = []
    for i in range(1, page+1):
        data = {'wd': keyword, 'pn': str(i-1) + '0', 'ie': 'utf-8','oq':keyword}
        # , 'tn': 'baidurt', 'bsst': '1', 'f': '8', 'rsv_bp': '1',
        data = urllib.parse.urlencode(data)
        url = baseUrl + data
        # url = 'https://www.baidu.com/s?wd={}n={}&ie=utf-8&usm=3&rsv_pq=fbda1a0e00007209&rsv_t=e42d5EfBAg375HlCG0hUUDfwSqlVCGUXnY4JhGFoRaR6JGNevLA5a2j1GIM'.format(keyword,i)
        print('正在获取第{}页数据'.format(i))
        get_html(url)
        print('---------------')

    save_to_excel(results)
    print(time.time() - start)
