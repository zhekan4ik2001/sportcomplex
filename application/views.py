from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser


def index(request):
    return render(request, 'sportcomplex/mainpage.html', {})

def buff(request):
    return render(request, 'sportcomplex/buff.html', {})