from django.urls import re_path
from . import views

app_name = 'application'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^buff.html$', views.buff, name='buff'),
]