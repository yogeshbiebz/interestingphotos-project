# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from forms import *
from models import LikeModel, CommentModel, Post
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password, check_password
from imgurpython import ImgurClient
from interesting_photos.settings import BASE_DIR


# Create your views here.

def signup_view(request):
    welcome_text = "Aperture Community Welcomes aboard the community. We are glad to have to part of our Aperture. Login to your account and start posting."
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            email = form.cleaned_data.get('email')
            send_mail(
                'Welcome to Aperture',
                welcome_text,
                'yogesh.bieber@gmail.com',
                [email],
                fail_silently=False,
           )
        return redirect('../../feed/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


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


@login_required(login_url='../login/')
def feed_view(request, username=None):

    if username:
        posts = Post.objects.filter(user=username).order_by('-created_on')
    else:
        posts = Post.objects.all().order_by('-created_on')

    for post in posts:
        x = User.objects.get(id=request.user.id)
        existing_like = LikeModel.objects.filter(post_id=post.id, user=x).first()
        if existing_like:
            post.has_liked = True

    return render(request, 'feed.html', {'posts': posts})

@login_required(login_url='../login/')
def upload_view(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, 'upload.html', {'form': form})
    elif request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            pic = form.cleaned_data.get('image')
            title = form.cleaned_data.get('caption')
            post = PostForm().instance
            x = User.objects.get(id=request.user.id)
            post.user = x
            post.image = pic
            post.caption = title

            post.save()

            path = str(BASE_DIR + "/" + post.image.url)

            client = ImgurClient('683c1c4dca9fe29', '77fe734f66c784b86ba973d9cb415280df89ce4e')
            post.image_url = client.upload_from_path(path, anon=True)['link']
            post.save()
            return redirect('../feed/')
        else:
            return render(request, 'upload.html')
    else:
        return render(request, 'upload.html')

@login_required(login_url='../login/')
def like_view(request):
    form = LikeForm(request.POST)
    if form.is_valid():
        post_id = form.cleaned_data.get('post').id
        x = User.objects.get(id=request.user.id)
        existing_like = LikeModel.objects.filter(post_id=post_id, user=x).first()
        if not existing_like:
            LikeModel.objects.create(post_id=post_id, user=x)
        else:
            existing_like.delete()
        return redirect('../feed/')


@login_required(login_url='../login/')
def comment_view(request):
    form = CommentForm(request.POST)
    if form.is_valid():
        post_id = form.cleaned_data.get('post').id
        comment_text = form.cleaned_data.get('comment_text')
        x = User.objects.get(id=request.user.id)
        comment = CommentModel.objects.create(user=x, post_id=post_id, comment_text=comment_text)
        comment.save()
        return redirect('/feed/')
    else:
        return redirect('/feed/')

@login_required(login_url='../login/')

def upvote_view(request):
    form = UpvoteForm(request.POST)
    if form.is_valid():
        comment_id = form.cleaned_data.get('comment').id
        x = User.objects.get(id=request.user.id)
        existing_like = Upvote.objects.filter(comment_id=comment_id, user=x).first()
        if not existing_like:
            LikeModel.objects.create(comment_id=comment_id, user=x)
        else:
            existing_like.delete()

        return redirect('../feed/')
    else:
        return redirect('../upload/')
