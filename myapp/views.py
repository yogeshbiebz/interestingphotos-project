# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import SignUp
from django.contrib.auth.hashers import make_password

# Create your views here.


def home_view(request):
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(name=name, password=make_password(password), email=email, username=username)
            user.save()
            render(request, 'success.html')

    elif request.method == "GET":
        form = SignUp()
    return render(request, 'home.html')