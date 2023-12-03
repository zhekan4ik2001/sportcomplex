from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'sportcomplex/mainpage.html', {})

def buff(request):
    return render(request, 'sportcomplex/buff.html', {})

@login_required
def profile(request):
    return render(request, 'users/profile.html')
