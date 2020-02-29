from __future__ import (absolute_import,division,print_function,unicode_literals)
from urllib.request import urlopen
import json

json_url='http://raw.githubusercontent.com/muxuezi/btc/master/btc_close_2017.json'
# 获取数据
response=urlopen(json_url)
# 读取数据
req=response.read()
# 将数据写入文件
with open('output\\btc_close_2017_urllib.json','wb') as f:
    f.write(req)
#将内容转换为python能处理的格式
file_urllib=json.loads(req)
print(file_urllib)