from django.forms import ModelForm

from .models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        labels = {
            'text': 'Текст задачи',
            'group': 'Группа'
        }
        help_text = {
            'text': 'Текст вашей записи',
            'group': 'Группа, к которой будет относится задача'
        }


class SearchPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('text',)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
