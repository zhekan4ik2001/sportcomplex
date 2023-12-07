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
    re_path(r'^profile/', views.profile, name='users-profile'),
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
    re_path(r'schedule/', login_required(views.ScheduleView.as_view()),
        name='schedule')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 