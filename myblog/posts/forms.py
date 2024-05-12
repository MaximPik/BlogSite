from django.forms import ModelForm, HiddenInput
from .models import Post, Comment, Follow
from django import forms

# cоздание класса формы
class PostForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Post
        fields = ['group', 'text', 'image']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class FollowForm(ModelForm):
    class Meta:
        model = Follow
        fields = ['user', 'author']
        