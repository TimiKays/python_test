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
    sec=(soup.find('section','stockTable'))('a')

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

def get_stock_info():
    pass


if __name__ == '__main__':
    list_url='https://hq.gucheng.com/gpdmylb.html'
    start_url='https://hq.gucheng.com/SZ000001/'
    list=[]
    get_stock_list(list_url,list)
    df=pd.DataFrame(list,columns=['url','code','name'])
    df.to_csv('stock_list.csv')
    get_stock_info()