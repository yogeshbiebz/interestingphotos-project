# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import uuid

# Create your models here.
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Post(models.Model):
    user = models.OneToOneField(User)
    image = models.FileField(upload_to='user_images/')
    caption = models.CharField(max_length=240)
    image_url = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    has_liked = False

    @property
    def like_count(self):
        return len(LikeModel.objects.filter(post=self))

    @property
    def comments(self):
        return CommentModel.objects.filter(post=self).order_by('-created_on')


class LikeModel(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class CommentModel(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    comment_text = models.CharField(max_length=555)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    has_upvoted = False


class Upvote(models.Model):
    user = models.ForeignKey(User)
    comment = models.ForeignKey(CommentModel)
