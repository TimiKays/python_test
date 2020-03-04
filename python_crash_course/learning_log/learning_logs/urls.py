"""定义learning_logs的URL模式"""

from django.conf.urls import url
from . import  views
urlpatterns=[
    #主页
    # 正则表达式，让python查找从开头到末尾没任何东西的url
    # 当与正则表达式匹配时，调用这个视图
    # 指定这个url模式名字为index
    url(r'^$',views.index,name='index'),
    url(r'^topics/$',views.topics,name='topics'),
    # 匹配两个斜杠中的整数，并把该证书存储在topic_id中，d+表示任意位数的整数
    url(r'^topics/(?P<topic_id>\d+)/$',views.topic,name='topic'),
    url(r'^new_topic/$',views.new_topic,name='new_topic'),
    url(r'^new_entry/(?P<topic_id>\d+)/$',views.new_entry,name='new_entry'),
    url(r'^edit_entry/(?P<entry_id>\d+)/$',views.edit_entry,name='edit_entry')
]