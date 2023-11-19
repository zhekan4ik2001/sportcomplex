from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'sportcomplex/mainpage.html', {})

def buff(request):
    return render(request, 'sportcomplex/buff.html', {})
