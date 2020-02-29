from __future__ import (absolute_import,division,print_function,unicode_literals)
from urllib.request import urlopen
import requests
import json

json_url='http://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
# ------用urlopen方式------
# 获取数据
response=urlopen(json_url)
# 读取数据
res=response.read()
# 将数据写入文件
with open('output\\btc_close_2017_urllib.json','wb') as f:
    f.write(res)
#将内容转换为python能处理的格式
file_urllib=json.loads(res)
print(file_urllib)

# ------用requests方式------
req=requests.get(json_url)
# 输出文件与之前的方式内容相同
with open('output\\btc_close_2017_requests.json','w') as f:
    f.write(req.text)
#将内容转换为python能处理的格式
file_requests=req.json()

print(file_requests==file_urllib)
