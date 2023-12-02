from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

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
                            'user_email')}),
        ('Fundamental Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', )
        }),
        ('Group Permissions', {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions', )
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
        ('Personal info', {'fields': ('user_gender', 'user_first_name', 'user_last_name', 
                            'user_patronymic', 'user_phone',
                            'user_email')}),
        ('Fundamental Permissions', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', )
        }),
        ('Group Permissions', {
            'classes': ('wide',),
            'fields': ('groups', 'user_permissions', )
        })
    )
    search_fields =  ('username', 'user_email')
    ordering = ('username',)

    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(CustomUser, MyUserAdmin)