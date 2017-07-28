from django import forms
from models import User, Post


class SignUp(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'password']


class LogIn(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user', 'image', 'caption']

