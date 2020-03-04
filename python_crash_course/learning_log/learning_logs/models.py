from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Topic(models.Model):
    """主题的类"""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        """返回模型的字符串表示"""
        return self.text


class Entry(models.Model):
    """条目的类"""
    # 外键，引用数据库的另一条记录
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    # 不限制长度的文本
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # 嵌套的meta类，verbose_name_plural表示复数的词汇
    class Meta:
        verbose_name_plural = 'entries'

    def __str__(self):
        # 只显示前50个字符
        if len(self.text) > 50:
            return self.text[:50] + "..."
        else:
            return self.text
