import os
import re
import requests
import bs4

# 爬取网页
def get_html(url):
    try:
        r=requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        # print(r.text[:500])
        return r.text
    except(Exception) as e:
        print(e)

# 封装信息
def package_data(f,li_uni):
    soup= bs4.BeautifulSoup(f,'html.parser')
    tbody=soup.find('tbody','hidden_zhpm')
    for tr in tbody('tr'):
        td=tr('td')
        dict={}
        dict['range']=td[0].string
        dict['name']=td[1].string
        dict['score']=td[3].string
        li_uni.append(dict)





# 打印信息
def print_data(li_uni,len):
    tplt='{0:{3}^6}\t{1:{3}^15}\t{2:{3}^}'
    print(tplt.format('排名','大学名称','得分',chr(12288)))
    for i in li_uni[:20]:
        # print (i)
        print(tplt.format(i['range'],i['name'],i['score'],chr(12288)))


if __name__ == '__main__':
    url='http://www.zuihaodaxue.cn/zuihaodaxuepaiming2016.html'
    li_uni=[]
    root='./data/'
    path=root+url.split('/')[-1]
    if not os.path.exists(root):
        os.mkdir(root)
    with open(path,'r+',encoding='utf-8') as f:
        # html=get_html(url)
        # f.write(html)
        package_data(f,li_uni)
    print_data(li_uni,20)