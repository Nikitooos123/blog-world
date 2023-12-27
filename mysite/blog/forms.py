from django import forms
from .models import UserPost, CommentPost


''' Форма заполнения комментария '''

class CommentForm(forms.ModelForm):

    class Meta:
        model = CommentPost
        fields = ['body']

''' Форма заполнения поста '''

class PostForm(forms.ModelForm):

    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'submit-post', 'placeholder': 'Что у вас нового?'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'submit-title', 'placeholder': 'Название поста'}))

    class Meta:
        model = UserPost
        fields = ['title', 'body', 'image']