#fenci_hamlet.py
import re

def getText():
    '''#获取文件内容并去掉标点符号，并分割到列表中'''
    txt=open('hamlet.txt', 'r').read()
    txt=txt.lower()
    # 把所有的标点符号替换为空格
    pure_txt=re.sub(r'\W',' ',txt)
    # print(pure_txt)
    global ls_words
    ls_words=pure_txt.split()

def getCounts():
    '''得到统计次数的列表，并根据次数倒序'''
    for word in ls_words:
        counts[word]=counts.get(word,0)+1
    global items
    # 键值对的列表
    items=list(counts.items())
    items.sort(key=lambda x:x[1],reverse=True)

def printCounts(x):
    '''打印排好序的列表，列表单项为元组'''
    for i in range(x):
        word,count=items[i]
        print('{:<10}{:>6}'.format(word,count))

if __name__ == '__main__':
    counts = {}
    ls_words=[]
    items=[]
    getText()
    getCounts()
    printCounts(10)