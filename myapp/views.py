# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import SignUp, LogIn
from models import User, SessionToken
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.



def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token'))
        if session:
           return session.user
    else:
        # return render(request, 'login.html')
        return None


def signup_view(request):
    loginerror2 = ""
    form = 0
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(name=name, password=make_password(password), email=email, username=username)
            user.save()
            return render(request, 'success.html')
        else:
            username = form.cleaned_data['username ']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            loginerror2 = username + password + email + name
            return render(request, 'signup.html', {'loginerror2': loginerror2})
    elif request.method == "GET":
        form = SignUp()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    # check_validation(request)
    loginerror = ""
    if request.method == "POST":
        form = LogIn(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = User.objects.filter(username=username).first()
            if user:
                if check_password(password, user.password):
                    token = SessionToken(user=user)
                    token.create_token()
                    token.save()
                    response = redirect('../feed')
                    response.set_cookie(key='session_token', value=token.session_token)
                    return response
                else:
                    loginerror = "Incorrect Username or Password."
                    return render(request, 'login.html', {'loginerror': loginerror})
            else:
                loginerror = "Incorrect Username or Password."
                return render(request, 'login.html', {'loginerror': loginerror})
        else:
            loginerror = "Incorrect Username or Password."
            return render(request, 'login.html', {'loginerror' : loginerror})
    elif request.method == "GET":
        form = LogIn()
        return render(request, 'login.html')

def feed_view(request):
    # x = check_validation(request)
    # if x:
        return render(request, 'feed.html')
    # else:
    #     return render(request, 'login.html')
#