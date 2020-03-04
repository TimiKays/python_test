from django import forms
from django.forms import widgets

from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    """主题的表单"""
    class Meta:
        """告诉Django根据哪个模型创建表单，在表单中包含哪些字段"""
        model=Topic
        # 表单的字段只有一个，text
        fields=['text']
        # 不要为字段生成标签
        labels={'text':''}

class EntryForm(forms.ModelForm):
    """条目的表单"""
    # 与topic的关联怎么表现出来？
    class Meta:
        model=Entry
        fields=['text']
        labels={'text':''}
        widgets={'text':forms.Textarea(attrs={'cols':80})}
