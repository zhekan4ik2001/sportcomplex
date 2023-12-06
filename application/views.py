from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomPassResetForm

def index(request):
    return render(request, 'application/mainpage.html', {})

def buff(request):
    return render(request, 'application/buff.html', {})

def buff(request):
    return render(request, 'application/buff.html', {})

@login_required
def profile(request):
    return render(request, 'application/profile.html')

class CustomResetPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = CustomPassResetForm
    template_name="registration/password_reset_form.html"
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = 'password_reset_done'
