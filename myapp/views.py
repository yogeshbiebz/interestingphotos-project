# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from forms import SingUpForm


# Create your views here.


def home_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
    elif request.method == "GET":
        form = SignUpForm()
    return render(request, 'home.html')
