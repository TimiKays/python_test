*- coding: utf-8 -*-
# @Author: Anderson
# @Date:   2019-11-14 16:30:55
# @Last Modified by:   Anderson
# @Last Modified time: 2019-12-30 15:32:39
from makerbean import web_crawler_bot as wbot
from makerbean import excel_bot as ebot
from makerbean import data_analysis_bot as dbot
from makerbean import pdf_bot as pbot
for page in range(50):
	data = wbot.get_liepin('Android',page)
	for job in data:
		ebot.add_row(job)
ebot.save('Android')
words=ebot.get_col(5)
word_freq=dbot.get_word_frequency(words)
dbot.generate_word_cloud(word_freq)
