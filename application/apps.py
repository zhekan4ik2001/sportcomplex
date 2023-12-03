from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class ApplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'application'
    verbose_name = _('SportСomplex')
