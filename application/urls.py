from django.urls import re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'application'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^buff.html$', views.buff, name='buff'),
    re_path(r'^profile/', views.profile, name='users-profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 