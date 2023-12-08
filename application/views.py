from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser, Training
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import classonlymethod
from django.views.decorators.cache import cache_control
from django.contrib.auth.views import PasswordResetView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomPassResetForm, TrainingSessionForm
from django.shortcuts import get_object_or_404, redirect



def index(request):
    return render(request, 'application/mainpage.html', {})

def buff(request):
    return render(request, 'application/buff.html', {})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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


class ScheduleView(TemplateView):
    form_class = TrainingSessionForm
    template_name="application/schedule.html"
    

    def is_in_group(self, user):
        return user.groups.filter(name='trainer').exists() 

    def get(self, request):
        training_sessions = Training.objects.all()
        if (request.user.groups.filter(name='trainer').exists() ):
            form = TrainingSessionForm(request.POST)
            return render(request, 'application/schedule.html', {'training_sessions': training_sessions,
                                                            'form': form})
        else:
            return render(request, 'application/schedule.html', {'training_sessions': training_sessions})

    def post(self, request):
        if (not self.is_in_group(request.user)):
            return ('application:index')
        data_form = TrainingSessionForm(request.POST)
        if data_form.is_valid():
            data_form.save()
            return redirect('application:schedule')

    #def put(self, request, *args, **kwargs):
    #    if (not self.is_in_group(request.user)):
    #        return ('application:index')
    #    training_session = get_object_or_404(Training, training_id=kwargs.training_id)
    #    form = TrainingSessionForm(instance=training_session)
    #    
    #    if request.method == 'POST':
    #        form = TrainingSessionForm(request.POST, instance=training_session)
    #        if form.is_valid():
    #            form.save()
    #            return redirect('application:schedule')
    #    return render(request, 'application/schedule.html', {'form': form})

