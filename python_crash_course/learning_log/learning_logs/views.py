from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Topic
from .forms import TopicForm


# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')  # 原始请求对象，一个可用于创建网页的模板


def topics(request):
    """用于显示所有topic的目录页"""
    # 查询数据库并排序，将查询集存储在变量
    topics = Topic.objects.order_by('date_added')
    # 要发送给模板的上下文，一个字典，值是模板要访问的数据
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """显示单个主题的所有条目"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')  # 倒序
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


def new_topic(request):
    """用户新增一个topic的页面"""
    if request.method != 'POST':
        # 是GET请求，表示未提交数据，需要创建一个空表单
        form = TopicForm()
    else:
        # 是post请求，说明要提交填好的表单
        form = TopicForm(request.POST)
        # 如果表单都填好了，并且数据与要求的字段类型和长度符合
        if form.is_valid():
            # 就保存到数据库
            form.save()
            # 重定向到网页topics,reverse根据url模型反推url
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    # 通过上下文把表单发给模板，显示出来
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
