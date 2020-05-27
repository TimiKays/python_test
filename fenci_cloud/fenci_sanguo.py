import jieba


def getText():
    '''#获取文件内容，存入列表'''
    txt = open('threekingdoms.txt', 'r', encoding='utf-8').read()
    global ls_words
    ls_words = jieba.lcut(txt)


def getCounts():
    '''数据清洗'''
    # 统计词频
    for word in ls_words:
        if len(word) == 1:
            continue
        # 合并词汇
        elif word == "诸葛亮" or word == "孔明曰":
            rword = "孔明"
        elif word == "关公" or word == "云长":
            rword = "关羽"
        elif word == "玄德" or word == "玄德曰":
            rword = "刘备"
        elif word == "孟德" or word == "丞相":
            rword = "曹操"
        elif word == "后主":
            rword = "刘禅"
        else:
            rword = word
        counts[rword] = counts.get(rword, 0) + 1
    # 去重
    global excludes
    exclude_words = set()
    for k in counts.keys():
        if k in excludes:
            exclude_words.add(k)
    for s in exclude_words:
        del counts[s]

    global items
    # 排序
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)


def printCounts(x):
    '''打印排好序的列表，列表单项为元组'''
    for i in range(x):
        word, count = items[i]
        print('{:<10}{:>6}'.format(word, count))


if __name__ == '__main__':
    counts = {}
    ls_words = []
    items = []
    # 排除词汇
    excludes = '将军却说二人不可荆州不能如此商议如何主公军士左右军马引兵次日大喜天下东吴于是今日不敢魏兵陛下一人都督人马\
    不知汉中只见众将蜀兵上马大叫'
    getText()
    getCounts()
    printCounts(15)
