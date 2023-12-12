"""
URL configuration for SportComplex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.i18n import i18n_patterns
from rest_framework import routers
from application.views import TrainingViewSet
from django.views.i18n import JavaScriptCatalog

router = routers.DefaultRouter()
router.register(r'^trainings', TrainingViewSet)

urlpatterns = [
    re_path(r'^', include('application.urls')),
    re_path(r'^api/v1/', include(router.urls)),
    #re_path(r'accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += i18n_patterns(
    re_path(r'^admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    #re_path(r'accounts/', include('django.contrib.auth.urls')),
    # If no prefix is given, use the default language
    prefix_default_language=False
)