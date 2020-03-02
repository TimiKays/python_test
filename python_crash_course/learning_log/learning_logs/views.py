from django.shortcuts import render

# Create your views here.
from learning_logs.models import Topic


def index(request):
    """学习笔记的主页"""
    return render(request,'learning_logs/index.html') #原始请求对象，一个可用于创建网页的模板

def topics(request):
    """用于显示所有topic的目录页"""
    # 查询数据库并排序，将查询集存储在变量
    topics=Topic.objects.order_by('date_added')
    # 要发送给模板的上下文，一个字典，值是模板要访问的数据
    context={'topics':topics}
    return render(request,'learning_logs/topics.html',context)

def topic(request,topic_id):
    # 显示单个主题的所有条目
    topic =Topic.objects.get(id=topic_id)
    entries=topic.entry_set.order_by('-date_added') #倒序
    context={'topic':topic,'entries':entries}
    return render(request,'learning_logs/topic.html',context)