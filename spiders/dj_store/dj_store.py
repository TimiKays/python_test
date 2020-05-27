# -*- coding: utf-8 -*-

# @Author: TQ
# @Date:   2020-6-8
# 爬取动态网站，采用selenium

# 知乎：https://www.zhihu.com/question/46528604/answer/101954171


from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
import re


driver=webdriver.Chrome()                #用chrome浏览器打开
driver.get("https://www.dji.com/cn/where-to-buy/retail-stores?site=brandsite&from=footer")       #打开知乎我们要登录
time.sleep(3)                            #让操作稍微停一下
# driver.find_element_by_link_text('登录').click() #找到‘登录’按钮并点击
# time.sleep(2)
# #找到输入账号的框，并自动输入账号 这里要替换为你的登录账号
# driver.find_element_by_name('account').send_keys('你的账号')
# time.sleep(2)
# #密码，这里要替换为你的密码
# driver.find_element_by_name('password').send_keys('你的密码')
# time.sleep(2)
# #输入浏览器中显示的验证码，这里如果知乎让你找烦人的倒立汉字，手动登录一下，再停止程序，退出#浏览器，然后重新启动程序，直到让你输入验证码
# yanzhengma=input('验证码:')
# driver.find_element_by_name('captcha').send_keys(yanzhengma)
# #找到登录按钮，并点击
# driver.find_element_by_css_selector('div.button-wrapper.command > button').click()

# 滚动
def execute_times(times):
    for i in range(times + 1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
execute_times(3)

# selenium处理下拉选择框，选择省份
# https://www.cnblogs.com/jieliu8080/p/10710377.html
from selenium.webdriver.support.select import Select
selector=Select(driver.find_elements_by_class_name("selector-select")[2])
# selector.select_by_visible_text('省份/直辖市/行政区 *')
store_li=[]
for i in range(1,35):
    selector.select_by_index(i)
    time.sleep(2)
    # 解析
    html=driver.page_source
    soup1=BeautifulSoup(html,'lxml')
    # print(soup1.text)
    stores=soup1.find('tbody')
    sheng=soup1('select')[2].contents[i].string

    for td in stores('td'):
        # print(td)

        name='不明'
        # print(td.text)
        st_li=re.split(r"\s\s+",td.text)
        print('maobing',st_li)

        name=st_li.pop(1)
        location=st_li.pop(1)
        tel=st_li.pop(-2)
        t=''.join(st_li)

        clean_store={}
        clean_store['sheng'] = sheng
        clean_store['name']=name
        clean_store['location'] = location
        clean_store['tel'] = tel
        clean_store['time'] = t

        store_li.append(clean_store)
        # try:
        #     name=td.find('h4').string
        # except:
        #     print('名称有问题')
        # store.append(name)
        # ps=td.findall('p')
        # for p in ps:
        #     store.append(p.string)
        #     store.append(p.text)
        # store_li.append(store)
print(store_li)

df=pd.DataFrame(store_li)
df.to_excel('大疆门店20200611.xls',index=0)

