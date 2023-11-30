from django.shortcuts import render
from django.http import HttpResponse
from .models import Club_Client, Club_Trainer


def index(request):
    return render(request, 'sportcomplex/mainpage.html', {})

def buff(request):
    return render(request, 'sportcomplex/buff.html', {})
