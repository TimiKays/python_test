# -*- coding: utf-8 -*-
import re
import xlwt
import time
import requests
import pandas as pd
from retrying import retry
from concurrent.futures import ThreadPoolExecutor
import matplotlib
import missingno as msno
# 分词的
import jieba
# 可视化的
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import imread  # 导入有误，用来读图的，先不要了


# 爬取网页，返回请求的网页内容
@retry(stop_max_attempt_number=3)  # 设置最大重试次数
def network_programming(num):
    url = 'https://s.taobao.com/search?q=保温饭盒&s_from=newHeader&ssid=s5-e&search_type=item&sourceId=tb.item&bcoffset=3&ntoffset=3&p4ppushleft=1%2C48&s=' + str(
        num)
    # https://s.taobao.com/search?q=%E6%8A%BD%E7%BA%B8&s_from=newHeader&ssid=s5-e&search_type=item&sourceId=tb.item
    html = requests.get(url, headers=headers)
    html.encoding = 'utf-8'
    return html


# 多线程遍历页码并调用爬取网页的方法
def multithreading(pagenum):
    # 每次爬取未爬取成功的页
    number = pagenum
    html_list = []
    with ThreadPoolExecutor(max_workers=10) as executor:  # 多线程开始，最大线程为10
        for html in executor.map(network_programming, number, chunksize=10):  # 把页码中的数字遍历并传给爬取网页的方法
            html_list.append(html)  # 把返回的网页都加入到event列表
    return html_list


def get_data():
    # plist 为1-100页的URL的编号num,第二页的url以44结尾
    page_list = []
    for html in range(1, 10):
        j = 44 * (html - 1)
        page_list.append(j)
    print(page_list)

    pagenum = page_list  # 为什么要换个
    datatmsp = pd.DataFrame(columns=[])  # 创建一个空的二维数组？

    while True:
        listpg = []
        html_list = multithreading(pagenum)  # 调用多线程爬取网页，返回网页的列表
        for html in html_list:  # 遍历网页列表
            json = re.findall('"auctions":(.*?),"recommendAuctions"', html.text)  # 用正则表达式找到网页中的
            print(json)
            if len(json):
                table = pd.read_json(json[0])
                datatmsp = pd.concat([datatmsp, table], axis=0, ignore_index=True)  # 数据拼接

                pg = re.findall('"pageNum":(.*?),"p4pbottom_up"', html.text)[0]
                listpg.append(pg)

        # 将爬取成功的页码转为url中的num值
        lists = []
        for a in listpg:
            b = 44 * (int(a) - 1)
            lists.append(b)

        listn = pagenum

        pagenum = []
        for p in listn:
            if p not in lists:
                pagenum.append(p)

        # 当未爬取页数未0时，终止循环
        if len(pagenum) == 0:
            break  # 跳出while true循环

    # 保存到excel表格中
    datatmsp.to_excel('./data/data1_original.xls', sheet_name='原始数据', index=False)


def clean_data():
    data_source = pd.read_excel('./data/data1_original.xls')
    # 查看清洗前的数据长宽，26列，180行
    print(data_source.shape)

    # 处理缺失值
    # msno.matrix(data, labels=True)      #msno查看数据缺失情况图
    # msno.bar(data.sample(len(data)),figsize=(10,4))     #msno查看列的缺失值的条形图,figsize调整图的纵横比，
    half_count = len(data_source) / 2  # 计算行数的一半，如180行，则这里等于90
    # dropna：pandas的方法，删除缺失值过半的列，返回删除了空值的dataframe对象
    # thresh=half_count，表示保留至少有90个非空值的行/列，
    # axis=1表示删除列，等价于axis=columns。如果要删除行，则axis=0或者index。默认为0
    data_source = data_source.dropna(thresh=half_count, axis=1)
    print(data_source.shape)  # 处理完空值后，还剩19列，180行

    data_source = data_source.drop_duplicates()  # 删除重复行
    data = data_source[  # 根据需求，选取了七列
        ['raw_title', 'detail_url', 'view_price', 'item_loc', 'view_sales', 'comment_count', 'nick']
    ]
    print(data.shape)  # 选取后的数据长宽，7列，179行

    # 删除有缺失值的行
    # data1 = data.reindex(columns=list(data.columns) + ['E'])
    # data.dropna(inplace=True)         #inplace=True，表示就地删除，不返回啥了

    # 缺失值只要在付款人数和评论数，把缺失值设为0
    data.fillna(0, inplace=True)
    # print(data.head())
    print(data.shape)

    # 字段重组。把省份和城市分开，对销售额进行格式化
    data['province'] = data.item_loc.apply(lambda x: x.split()[0])
    data['city'] = data.item_loc.apply(
        lambda x: x.split()[0] if len(x) < 4 else x.split()[1])  # 如果小于4，说明是直辖市，就取省名，如果大于4，就取市名
    data['view_sales'] = data.view_sales.astype('str')
    # data['sales'] = data.view_sales.apply(lambda x: x.str.split('人')[0])      #一会float一会str一会Int的，直接先转成str格式
    data['sales'] = data['view_sales'].map(lambda x: x.split('人')[0])

    # 要把sales列的万+字样去掉，换成Int类型
    # 有+号的去掉+号
    move_plus = lambda x: x.split('+')[0] if ('+' in x) else x
    # 有万字的去掉万，并把剩余部分*10000
    move_wan = lambda x: float(x.split('万')[0]) * 10000 if ('万' in x) else x
    data['sale'] = data['sales'].map(move_plus)
    data['sale2'] = data['sale'].map(move_wan)

    print(data.dtypes)
    # 开始把列转换类型,有些分析需要用到category
    data['sales'] = data.sale2.astype('int')
    list_col = ['province', 'city']  # 设置数据集中的新增两列的属性
    for i in list_col:
        data[i] = data[i].astype('category')  # 种类的类型？
    data = data.drop(['item_loc', 'view_sales', 'sale', 'sale2'], axis=1)  # 删除旧的两列数据
    print(data.dtypes)
    print(data.head())

    # 保存到excel，没办法不覆盖之前的sheet，就重新建了个文件。后面再一起合并吧
    data.to_excel('./data/data2_cleaned.xls', sheet_name='清洗后', index=False)


def analyze_data():
    data = pd.read_excel('./data/data2_cleaned.xls')

    # 得到标题一列，并把标题分词，去重，合并，统计次数
    # title = data.raw_title.values.tolist()
    # title_s = []
    # for line in title:
    #     title_cut = jieba.lcut(line)
    #     title_s.append(title_cut)
    # print(title_s)
    #
    # # 剔除不需要的单词，使用停用表，这里直接自己创建一个列表好了
    # # stopwords = pd.read_excel('./data/stopwords.xlsx')
    # # stopwords = stopwords.stopword.values.tolist()
    # stopwords = ['抽纸','纸巾']
    # pattern = '^[\u4e00-\u9fa5]{2,}$'  # 两个以上汉字
    # title_clean = []
    # for line in title_s:
    #     line_clean = []
    #     for word in line:
    #         if word not in stopwords and re.match(pattern, word):  # 正则表达式
    #             line_clean.append(word)
    #     title_clean.append(line_clean)
    # print(title_clean)
    #
    # # 统计每个词语的个数，先把单个列表中的词汇去重
    # title_clean_dist = []
    # for line in title_clean:
    #     line_dist = []
    #     for word in line:
    #         if word not in line_dist:
    #             line_dist.append(word)
    #     title_clean_dist.append(line_dist)
    #
    # # 将所有词转换为一个list
    # allwords_clean_dist = []
    # for line in title_clean_dist:
    #     for word in line:
    #         allwords_clean_dist.append(word)
    #
    # # 将所有词语转换数据帧，计算每个词汇出现的次数
    # df_allwords_clean_dist = pd.DataFrame({'allwords': allwords_clean_dist})
    # word_count = df_allwords_clean_dist.allwords.value_counts().reset_index()
    # word_count.columns = ['word', 'count']
    # print(word_count.head())

    # 词云可视化
    # plt.figure(figsize=(10, 10))
    # pic = imread("./data/chouzhi.png")   #`imread` is deprecated in SciPy 1.0.0, and will be removed in 1.2.0.Use ``imageio.imread`` instead.
    # w_c = WordCloud(font_path="./data/SourceHanSans-Normal.otf",  #设置字体，要中文字体，ttf或otf格式
    #                 background_color='white',  #背景色
    #                 mask=pic,  #造型遮盖
    #                 # max_font_size=48,  #最大字体
    #                 # min_font_size=10,  #最小字体
    #                 random_state=23,  #随机数
    #                 # collocations=False, #避免重复单词
    #                 # width=1000,height=800,margin=10,  #图像宽高，字间距，需要配合下面的plt.figure(dpi=xx)放缩才有效
    #                 scale=4,   #越大越清晰
    #                 # 绘图区域怎么设置？
    #                 )
    # wc = w_c.fit_words({
    #     x[0]: x[1] for x in word_count.head(100).values   #???
    # })
    # # 显示词云图片
    # plt.imshow(wc, interpolation='bilinear')  #遮罩
    # plt.axis("off")  #去掉坐标轴
    # plt.show()

    # 不同关键词的销量统计分析
    # sale_sum = []
    # for word in word_count.word:  # 根据统计词汇列表生成对应的销量列表
    #     i = 0
    #     s_list = []
    #     for word_single_list in title_clean_dist:  # 包含所有词组列表的列表
    #         if word in word_single_list:
    #             try:
    #                 s_list.append(data.sales[i])
    #             except:
    #                 s_list.append(0)
    #         i += 1
    #     sale_sum.append(sum(s_list))
    # df_sale_sum = pd.DataFrame({'w_s_sum': sale_sum})  # 得到不同关键词的销量统计列
    # # 把两个表拼起来
    # df_word_count_sum = pd.concat([word_count, df_sale_sum], axis=1, ignore_index=True)
    # # 没有纵轴标签了，加一下：
    # df_word_count_sum.columns = ['word', 'count', 'sale_sum']
    # print(df_word_count_sum.head(20))

    font = matplotlib.font_manager.FontProperties(fname='./data/SourceHanSans-Normal.otf')
    # 把销量可视化-条形图
    # df_word_count_sum.sort_values('sale_sum', inplace=True, ascending=True)  # 按照销量升序
    # df_top30_sale = df_word_count_sum.tail(30)  # 得到销量最高的30个数据
    # index = np.arange(df_top30_sale.word.size)  # 30
    # show_barh(index, df_top30_sale.sale_sum, list(df_top30_sale.word), '关键词销量条形图',font)

    # 查看300元以下商品的价格分布情况
    price=300
    data_p = data[(data['view_price'] < price) & (data['sales']>1)]
    print(data_p.shape)
    print(data_p.head(10))
    # title = '%s元以下的商品数据分布' % (price)
    # draw_hist(data_p['view_price'],title,'价格','商品数量',font)


    # 查看商品的销量分布情况
    # data_s=data[(data['sales']>100) ]
    # print(u'销量100以上的商品占比 : %0.3f' % (len(data_s) / len(data)))
    # draw_hist(data_s['sales'], '销量100以上的商品分布', '销量', '商品数量',font)

    # 查看不同价格区间的商品平均销量分布
    data['price'] = data.view_price.astype('int')
    # bins=[]
    # for i in range(11):
    #     bins.append(i*30)
    # print(bins)
    # data['group'] = pd.cut(data.price, bins)  # 根据价格分组，分成10组
    # df_group = data.group.value_counts().reset_index()
    # df_grouped_data = data[['sales', 'group']].groupby('group').mean().reset_index()  #mean计算平均数,sum计算总数
    # print(df_grouped_data)
    # index = np.arange(df_grouped_data.group.size)
    # draw_bar(index, df_grouped_data.sales, df_grouped_data.group, '不同价格区间商品的平均销量分布',font)

    # 计算300元以下商品的价格对销量的影响
    ## 绘制散点图
    # fig, ax = plt.subplots()
    # ax.scatter(data_p['view_price'], data_p['sales'], color='red',s=5)
    # ax.set_xlabel(u'价格', fontproperties=font)
    # ax.set_ylabel(u'销量', fontproperties=font)
    # title='商品价格对销量的影响_散点图'
    # ax.set_title(title, fontproperties=font)
    # plt.savefig('./data/%s.png' % title)
    # # 绘制线性回归拟合线
    # data['GMV'] = data['price'] * data['sales']
    # import seaborn as sns
    # sns.regplot(x='price', y='GMV', data=data, color='purple')
    # plt.savefig('./data/%s.png' % ('商品价格对销量的影响_线性回归'))

    #不同省份商品数量分布
    plt.figure(figsize=(8,4))
    data.province.value_counts().plot(kind='bar')
    plt.xticks(rotation=0,fontproperties=font)
    plt.xlabel(u'省份',fontproperties=font)
    plt.ylabel(u'商品数量',fontproperties=font)
    plt.title(u'不同省份商品数量分布',fontproperties=font)
    plt.savefig('./data/不同省份商品数量分布.png')

def draw_bar(li_x, li_y, li_x_label, title,font):
    # 绘制条形图
    font = matplotlib.font_manager.FontProperties(fname='./data/SourceHanSans-Normal.otf')
    plt.figure(figsize=(8, 4))
    plt.bar(li_x, li_y, color='blue',alpha=0.2)
    plt.xticks(li_x, li_x_label, fontproperties=font, rotation=20,fontsize=8)
    #不太需要坐标轴的标题
    # plt.xlabel('Group')
    # plt.ylabel('mean_sales')
    plt.title(title, fontproperties=font)
    ax = plt.subplot()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.savefig('./data/%s.png' % title)


def draw_hist(data, title, x_title, y_title,font):
    # 绘制直方图
    # 参数：数值列表，标题字符串

    plt.figure(figsize=(7, 5))
    plt.hist(data, bins=20, color='purple', rwidth=0.6)
    ### 参数说明###
    # matplotlib.pyplot.hist(x,bins=None,range=None, density=None, bottom=None, histtype='bar', align='mid', log=False, color=None, label=None, stacked=False, normed=None)
    # 关键参数
    # x: 数据集，最终的直方图将对数据集进行统计
    # bins: 统计的区间个数
    # range: tuple, 显示的区间，range在没有给出bins时生效
    # density: bool，默认为false，显示的是频数统计结果，为True则显示频率统计结果，这里需要注意，频率统计结果=区间数目/(总数*区间宽度)，和normed效果一致，官方推荐使用density
    # histtype: 可选{'bar', 'barstacked', 'step', 'stepfilled'}之一，默认为bar，推荐使用默认配置，step使用的是梯状，stepfilled则会对梯状内部进行填充，效果与bar类似
    # align: 可选{'left', 'mid', 'right'}之一，默认为'mid'，控制柱状图的水平分布，left或者right，会有部分空白区域，推荐使用默认
    # log: bool，默认False,即y坐标轴是否选择指数刻度
    # stacked: bool，默认为False，是否为堆积状图
    plt.xlabel(x_title, fontproperties=font)
    plt.ylabel(y_title, fontproperties=font)
    plt.title(title, fontproperties=font)
    # plt.show()
    plt.savefig('./data/%s.png' % title)


def show_barh(li_y, li_width, y_label, title,font):
    # 参数：纵坐标值列表，横坐标值列表，纵轴标签列表，标题字符串
    # 中文的字体路径
    font = matplotlib.font_manager.FontProperties(fname='./data/SourceHanSans-Normal.otf')

    # 尺寸
    plt.figure(figsize=(8, 8))
    plt.barh(
        li_y,
        li_width,
        # color='blue',  #颜色
        # facecolor='tan',
        # edgecolor='red',  # 边缘颜色
        height=0.8,  # 高度
        tick_label=y_label,  # y轴标签
        align='center',  # 对齐
        # alpha=0.4, #透明度
    )
    # plt.yticks(index, list(df_top30_sale.word), fontproperties=font)  # y轴标签
    plt.yticks(fontproperties=font)

    # 前边设置的x、y值其实就代表了不同柱子在图形中的位置（坐标），通过for循环找到每一个x、y值的相应坐标——a、b，再使用plt.text在对应位置添文字说明来生成相应的数字标签，而for循环也保证了每一个柱子都有标签。
    # '%.0f' % b,代表标注的文字，即每个柱子对应的y值，其中0表示不显示小数后面的数值，1就表示显示小数后面一位，以此类推；
    # ha='center', va= 'bottom'代表horizontalalignment（水平对齐）、verticalalignment（垂直对齐）的方式，
    # fontsize则是文字大小。条形图、折线图也是如此设置，饼图则在pie命令中有数据标签的对应参数。对于累积柱状图、双轴柱状图则需要用两个for循环，同时通过a与b的不同加减来设置数据标签位置。
    for x, y in zip(li_width, li_y):
        plt.text(x + 0.5, y, "%.0f" % x, ha='left', va='center', fontsize=8)  # 添加数据标签
    # 标题
    plt.title(title, fontproperties=font)
    # 横轴纵轴标题
    plt.xlabel('Sales', fontsize=10)
    plt.ylabel('Words', fontsize=10)
    # 横坐标纵坐标的范围，弄高一点图形整个下移了，不弄了
    # plt.axis([0, 900000, 0, 31])
    # 去除右边和上边的边框
    ax = plt.subplot()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # plt.show()
    plt.savefig('./data/%s.png' % title)


if __name__ == '__main__':
    # 计时开始
    start = time.time()

    # 请求头，为了反爬虫，要用cookie
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
        'cookie': 'td_cookie=18446744071423230592; thw=cn; v=0; cna=SCVpFkZXfCwCAT24cx3PJgie; t=6adef129ce0b98c6fcd52f3e83e3be03; cookie2=7de44eefb19e3e48e25b7349163592b7; _tb_token_=f1fae43e5e551; unb=3345403123; uc3=nk2=F6k3HMt8ZHbGobgMG0t6YMg7MKU%3D&vt3=F8dByuQFmIAq493a88Y%3D&lg2=W5iHLLyFOGW7aA%3D%3D&id2=UNN5FEBc3j%2FI9w%3D%3D; csg=07879b0c; lgc=t_1499166546318_0384; cookie17=UNN5FEBc3j%2FI9w%3D%3D; dnk=t_1499166546318_0384; skt=759aebdc118b2fc5; existShop=MTU3NTEwNzAyMg%3D%3D; uc4=id4=0%40UgQxkzEr7yNNkd0wQjAOQOK5hAra&nk4=0%40FbMocp0bShNOwIAboxPdw7pZW0Ru%2FnrngZiTM4a03Q%3D%3D; tracknick=t_1499166546318_0384; _cc_=UIHiLt3xSw%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=439; _nk_=t_1499166546318_0384; cookie1=B0TwtzQNNmewbhSpcaaRe7U24nc6DXOpwhexZLEN8Zo%3D; mt=ci=0_1; _m_h5_tk=ec0a32b82d6a8d5c46fe6f873373169b_1575114952532; _m_h5_tk_enc=cfea89ad4f02b520c3a094931d00e376; enc=CnjhIlaGaoA3J%2FSi2PeXU8%2FNC4cXQUAZjulyZI%2Bd9Z8JjGflldsE%2F%2B8F0Ty2oLD4v1wKgm3CuiGftr11IfyB5w%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; l=dBIBcdfeq5nSzFl5BOCa-urza77ThIRvfuPzaNbMi_5Ia1T6YV7OknJtce96cjWfTG8B4HAa5Iy9-etlwrZEMnMgcGAw_xDc.; uc1=cookie15=VFC%2FuZ9ayeYq2g%3D%3D&cookie14=UoTbmEp9zNxMrw%3D%3D; isg=BDk53DNPQMq9RRxe_Fnoei4wSKUTRi34hR8HPVturmDf4ll0o5Y9yKc0YOYUrsUw',
    }

    print("开始爬取...")
    # get_data()
    print('数据保存成功，开始清洗数据...')
    # clean_data()
    print('数据清洗完成，开始分析...')
    analyze_data()
    print(time.time() - start)
