from django.shortcuts import render
from django.http import HttpResponse
from .models import CustomUser, Training, Abonement
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import classonlymethod
from django.views.decorators.cache import cache_control
from django.contrib.auth.views import PasswordResetView
from django.views.generic.base import TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import CustomPassResetForm, TrainingSessionForm, ClientForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from rest_framework import permissions, viewsets
from .decorators import has_permission
from django.http import JsonResponse
from django.contrib.auth.models import Group

from .serializers import *



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


class TrainingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Training.objects.all()#.order_by('training_date')
    serializer_class = TrainingSerializer
    permission_classes = [permissions.IsAuthenticated]


class ScheduleView(TemplateView):
    form_class = TrainingSessionForm
    template_name="application/schedule.html"
    

    def is_in_group(self, user, group_name):
        return user.groups.filter(name=group_name).exists() 

    def get(self, request):
        #print(training_serializer.data)
        current_user = request.user
        if (self.is_in_group(current_user, 'trainer')):
            training_sessions = Training.objects.filter(training_leader__in = [current_user.user_id])
            training_serializer = TrainingSerializer(training_sessions, many=True)
            add_form = TrainingSessionForm(request.POST)
            add_form.setPrefix("add_")
            upd_form = TrainingSessionForm()
            upd_form.setPrefix("upd_")
            return render(request, self.template_name, {'training_serializer': training_serializer.data,
                                                            'add_form': add_form,
                                                            'upd_form': upd_form})
        elif (self.is_in_group(current_user, 'client')):
            training_sessions = Training.objects.filter(clients__in = [current_user.user_id])
            #print(Training.objects.filter(clients__in = [4]), current_user.user_id)
            training_serializer = TrainingSerializer(training_sessions, many=True)
            return render(request, self.template_name, {'training_serializer': training_serializer.data})
        else:
            return redirect('application:index')
    
    

    def post(self, request):
        if (not self.is_in_group(request.user, 'trainer')):
            return redirect('application:index')
        temp_data = TrainingSessionForm(request.POST)
        if temp_data.is_valid():
            #print(temp_data.fields)
            if (temp_data.data.get('clients')):
                new_data = temp_data.save(commit=False)
                new_data.training_leader_id = request.user.user_id
                #print(new_data)
                new_data.save()
                temp_data.save_m2m()
                return redirect('application:schedule')
            else:
                context = self.get_context_data(form=temp_data)
                context.update({"error": "No clients defined."})
                return self.render_to_response(context)
        else:
            return redirect('application:schedule')
    


@login_required
@has_permission('trainer')
def schedule_delete(request):
    id = request.POST.get('training_id')
    if (not request.user.groups.filter(name='trainer').exists()):
        return ('application:index')
    schedule_record = get_object_or_404(Training, pk=id)
    context = {'schedule_record': schedule_record}    
    output = schedule_record.delete()
    print(output)
    messages.success(request,  'The schedule_record has been deleted successfully.')
    return redirect('application:schedule')

@login_required
@has_permission('trainer')
def schedule_get(request, training_id):
    current_user = request.user
    if (current_user.groups.filter(name='trainer').exists() or
            current_user.groups.filter(name='client').exists()):
        #training_id = request.GET.get('training_id')
        training = Training.objects.get(training_id=training_id)
        cl = training.clients.all()
        print(cl)
        clients = list()
        for i in cl:
            clients.append(str(i.user_id))
        data = {
            'training_id': training.training_id,
            'training_date': training.training_date,
            'training_type': training.training_type.training_type_id,
            'clients': clients
        }
        return JsonResponse(data)
    else:
        return redirect('application:index')


@login_required
@has_permission('trainer')
def schedule_update(request):
    if request.method == 'POST':
        print(request.__dict__)
        instance = get_object_or_404(Training, training_id=request.POST.get('training_id'))
        instance_id = instance.training_leader_id
        temp_data = TrainingSessionForm(request.POST, instance=instance)
        print(instance.training_leader)
        if (instance and temp_data.is_valid()):
            if (temp_data.data.get('clients')):
                new_data = temp_data.save(commit=False)
                new_data.training_leader_id = instance_id
                new_data.save()
                temp_data.save_m2m()
                return redirect('application:schedule')
        else:
            print(temp_data.errors)

        return redirect('application:schedule')
    else:
        return redirect('application:schedule')



class AccountsView(TemplateView):
    form_class = CustomUser
    template_name="application/accounts.html"
    

    def is_in_group(self, user, group_name):
        return user.groups.filter(name=group_name).exists() 

    def get(self, request):
        #print(training_serializer.data)
        current_user = request.user
        if (not self.is_in_group(request.user, 'admin')):
            return redirect('application:index')

        accounts_list = CustomUser.objects.filter(groups__name='client')
        abonements_list = Abonement.objects.all()
        accounts_serializer = CustomUserSerializer(accounts_list, many=True)
        #abonements_serializer = CustomUserSerializer(accounts_list, many=True)
        add_form = ClientForm(request.POST)
        add_form.setPrefix("add_")
        upd_form = ClientForm(edition=True)
        upd_form.setPrefix("upd_")
        #upd_form.setEditionMode(True)
        return render(request, self.template_name, {'accounts_serializer': accounts_serializer.data,
                                                    'abonements_list': abonements_list,
                                                            'add_form': add_form,
                                                            'upd_form': upd_form})
    
    

    def post(self, request):
        if (not self.is_in_group(request.user, 'admin')):
            return redirect('application:index')
        temp_data = ClientForm(data=request.POST)
        if temp_data.is_valid():
            print(temp_data.fields)
            new_data = temp_data.save(commit=False)
            new_data.set_password(
                temp_data.cleaned_data["password"]
            )
            new_data.is_staff = True
            new_data.is_active = True
            #print(new_data)
            new_data.save()
            print('!!')
            client_group = Group.objects.get(name='client') 
            new_data.groups.add(client_group)
            return redirect('application:accounts')
        else:
            print(temp_data.errors)
            return redirect('application:accounts')

@login_required
@has_permission('admin')
def account_delete(request):
    id = request.POST.get('user_id')
    print(id)
    account_item = get_object_or_404(CustomUser.objects.filter(groups__name='client'), pk=id)
    context = {'account_item': account_item}  
    print(account_item)  
    if (account_item):
        output = account_item.delete()
        print(output)
    messages.success(request,  'The client account has been deleted successfully.')
    return redirect('application:accounts')

@login_required
@has_permission('admin')
def account_get(request, user_id):
    current_user = request.user
    #training_id = request.GET.get('training_id')
    account_item = CustomUser.objects.filter(groups__name='client').get(user_id=user_id)
    data = {
        'user_id': account_item.user_id,
        'username': account_item.username,
        'user_gender': account_item.user_gender.gender_id,
        'user_first_name': account_item.user_first_name,
        'user_last_name': account_item.user_last_name,
        'user_patronymic': account_item.user_patronymic,
        'user_email': account_item.user_email,
        'user_phone': account_item.user_phone
    }
    return JsonResponse(data)


@login_required
@has_permission('admin')
def account_update(request):
    if request.method == 'POST':
        instance = get_object_or_404(CustomUser, user_id=request.POST.get('user_id'))
        instance_id = instance.user_id
        temp_data = ClientForm(data=request.POST, edition=True, instance=instance)
        if (instance and temp_data.is_valid()):
            new_data = temp_data.save(commit=False)
            new_data.training_leader_id = instance_id
            new_data.save()
            temp_data.save_m2m()
            return redirect('application:accounts')
        else:
            print(temp_data.errors)

        return redirect('application:accounts')
    else:
        return redirect('application:accounts')


