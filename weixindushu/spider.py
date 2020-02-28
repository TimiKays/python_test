import requests

key_dict={'key1':'val1','key2':'val2'}
r=requests.get('http://www.santostang.com/get',params=key_dict)
# print('编码：',r.encoding)
# print('响应状态码：',r.status_code)
print('URL已正确编码',r.url)
print('字符串方式的响应体：',r.text)
