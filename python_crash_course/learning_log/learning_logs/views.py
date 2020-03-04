from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')  # 原始请求对象，一个可用于创建网页的模板

# 限制登陆后才能访问的页面
@login_required
def topics(request):
    """用于显示所有topic的目录页"""
    # 查询数据库并排序，将查询集存储在变量
    # 筛选属于该用户的主题
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    # 要发送给模板的上下文，一个字典，值是模板要访问的数据
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个主题的所有条目"""
    topic = Topic.objects.get(id=topic_id)
    # 检查该页面的主题是否为登录用户所有，不属于，就返回404错误页面
    if topic.owner!=request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')  # 倒序
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
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
            new_topic=form.save(commit=False)
            new_topic.owner=request.user
            new_topic.save()
            # 重定向到网页topics,reverse根据url模型反推url
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    # 通过上下文把表单发给模板，显示出来
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """新增一个条目的页面"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            # 创建一个条目的实例，但不提交到数据库
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            # 返回到新增条目所属的主题页
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    # 发给网页模板
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑单个条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 保护条目编辑页
    if topic.owner!=request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    # 发给网页模板
    return render(request, 'learning_logs/edit_entry.html', context)
