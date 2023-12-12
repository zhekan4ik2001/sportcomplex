from django.contrib import admin
from django import forms
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

admin.site.register(Abonement_Type)
admin.site.register(Abonement)
admin.site.register(Human_Gender)
admin.site.register(Training_Type)
admin.site.register(Training)

class MyUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'user_gender', 
                    'user_first_name', 'user_last_name', 
                    'user_patronymic', 'user_phone',
                    'user_email')
    list_filter = ('is_staff',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('user_gender', 'user_first_name', 'user_last_name', 
                            'user_patronymic', 'user_phone',
                            'user_email', 'avatar')}),
        (_('Fundamental Permissions'), {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', )
        }),
        (_('Group Permissions'), {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions', )
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
        (_('Personal info'), {'fields': ('user_gender', 'user_first_name', 'user_last_name', 
                            'user_patronymic', 'user_phone',
                            'user_email')}),
        (_('Fundamental Permissions'), {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', )
        }),
        (_('Group Permissions'), {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions', )
        })
    )
    search_fields =  ('username', 'user_email')
    ordering = ('username',)

    filter_horizontal = ('groups', 'user_permissions',)

class MyTrainingAdmin(admin.ModelAdmin):
    model = Training
    list_display = ('training_type', 'training_date', 
                    'training_leader')
    list_filter = ('training_date',)

    fieldsets = (
        (None, {'fields': ('training_type', 'training_date', 'training_leader',)}),
        (_('Clients'), {
            'classes': ('wide',),
            'fields': ('clients',)
        })
    )
    add_fieldsets = (
        (None, {'fields': ('training_type', 'training_date', 'training_leader', 
                            'clients')}),
    )
    search_fields =  ('training_type', 'training_date', 'training_leader')
    ordering = ('training_date',)

    filter_horizontal = ('clients',)

admin.site.register(CustomUser, MyUserAdmin)
admin.site.unregister(Training)
admin.site.register(model_or_iterable=Training, admin_class= MyTrainingAdmin)
admin.site.index_title = _('Adminitration')
admin.site.site_header = _('Site Administration')
admin.site.site_title = _('Management')