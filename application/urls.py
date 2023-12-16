from django.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .forms import UserLoginForm
from .views import CustomResetPasswordView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

app_name = 'application'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^profile/?$', views.profile, name='users-profile'),
    re_path(r'^login/',
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
            ),
        name='login'),
    re_path(r'^password_reset/', 
        CustomResetPasswordView.as_view(), 
        name='password_reset'),
    re_path(r'^logout/',
        auth_views.LogoutView.as_view(template_name="registration/logged_out.html"),
        name='logout'),
    re_path(r'^password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html")
        ),
    re_path(r'^schedule/?$', login_required(views.ScheduleView.as_view()),
        name='schedule'),
    re_path(r'^schedule/(?P<training_id>[0-9]+)$', views.schedule_get,
        name='schedule_get'),
    re_path(r'^schedule/delete$', login_required(views.schedule_delete),
        name='schedule_delete'),
    re_path(r'^schedule/update$', login_required(views.schedule_update),
        name='schedule_update'),
    
    re_path(r'^managing/?$', login_required(views.managing),
        name='managing'),
    
    re_path(r'^accounts/(?P<user_id>[0-9]+)$', login_required(views.account_get),
        name='account_get'),
    re_path(r'^accounts/delete$', login_required(views.account_delete),
        name='account_delete'),
    re_path(r'^accounts/update$', login_required(views.account_update),
        name='account_update'),
    
    re_path(r'^abonements/(?P<abonement_id>[0-9]+)$', login_required(views.abonement_get),
        name='abonement_get'),
    re_path(r'^abonements/delete$', login_required(views.abonement_delete),
        name='abonement_delete'),
    re_path(r'^abonements/update$', login_required(views.abonement_update),
        name='abonement_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 