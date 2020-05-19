'''
@a作者
    TimiKays
@功能描述
    分析txt文件的内容，生成词云，并保存为png图片
'''

import jieba
import wordcloud
from imageio import imread

if __name__ == '__main__':
    all_words=''
    f=open('./zhenfu_cloud_data/新时代中国特色主义.txt',encoding='utf-8')
    for line in f:
        line=line.replace('\n','')
        wordsls=jieba.lcut(line)
        words=' '.join(wordsls)
        all_words=all_words+words+' '
    mk=imread('./zhenfu_cloud_data/cat.jpeg')
    w=wordcloud.WordCloud(
        font_path='msyh.ttc',
        background_color='white',
        width=1000,
        height=800,
        max_words=30,
        mask=mk

    )
    w.generate(all_words)

    w.to_file('zhenfu_cloud.png')
