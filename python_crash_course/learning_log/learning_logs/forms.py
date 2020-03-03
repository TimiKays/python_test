from django import forms
from .models import Topic

class TopicForm(forms.ModelForm):
    class Meta:
        """告诉Django根据哪个模型创建表单，在表单中包含哪些字段"""
        model=Topic
        # 表单的字段只有一个，text
        fields=['text']
        # 不要为字段生成标签
        labels={'text':''}
