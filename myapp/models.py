# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=30)
    contact = models.IntegerField(max_length=13)
    age = models.IntegerField(max_length=3)
    created_on = models.DateTimeField(auto_now_add=True)
