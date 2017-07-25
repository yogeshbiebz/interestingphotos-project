from django import forms
from models import User


class SignUp(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'password']


class LogIn(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
