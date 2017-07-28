# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from forms import SignUp, LogIn, PostForm
from models import User, SessionToken
from django.contrib.auth.hashers import make_password, check_password
from imgurpython import ImgurClient
from interesting_photos.settings import BASE_DIR


# Create your views here.


def check_validation(request):
    if request.COOKIES.get('session_token'):
        session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token'))
        if session:
            return session
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
            return redirect('/login/')
        else:
            # username = form.cleaned_data['username ']
            # name = form.cleaned_data['name']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            loginerror2 = "Incorrect Input."
            return render(request, 'signup.html', {'loginerror2': loginerror2})
    elif request.method == "GET":
        form = SignUp()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
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
                    response = redirect('../feed/')
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
    # return render(request, 'feed.html')
    user = check_validation(request)

    if user:
        return render(request, 'feed.html')
    else:
        return redirect('/login/')


def upload_view(request):
    usr = check_validation(request)

    if usr:
        if request.method == "GET":
            form = PostForm()
            return render(request, 'upload.html', {'form' : form})
        elif request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                pic = form.cleaned_data['image']
                title = form.cleaned_data['caption']
                post = PostForm()
                post.user = usr
                post.image = pic
                post.caption = title
                post.save()

                path = str(BASE_DIR + post.image.url)

                client = ImgurClient('683c1c4dca9fe29', '77fe734f66c784b86ba973d9cb415280df89ce4e')
                post.image_url = client.upload_from_path(path, anon=True)['link']
                post.save()
                return redirect('feed/')
            else:
                return render(request, 'upload.html', {'error_msg' : "error"})

    else:
        return redirect('/login/')
