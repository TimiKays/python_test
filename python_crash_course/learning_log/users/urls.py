"""为应用程序users定义URL模式"""

from django.conf.urls import url
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    # 直接用系统的登录视图，不用自己创建视图了
    # 匹配 localhost:8000/users/login
    url(r'^login/$', LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register, name='register'),


]
