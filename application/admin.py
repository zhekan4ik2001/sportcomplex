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
    list_display = ('username', 'password', 'user_gender', 
                    'user_first_name', 'user_last_name', 
                    'user_patronymic', 'user_phone',
                    'user_email')
    list_filter = ('is_staff',)

    fieldsets = (
        (None, {'fields': ('username', 'password', 'user_gender', 'user_first_name', 'user_last_name', 
                            'user_patronymic', 'user_phone',
                            'user_email')}),

        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_gender', 'user_first_name', 'user_last_name', 
                            'user_patronymic', 'user_phone',
                            'user_email')}
        ),
    )
    search_fields =  ('username', 'user_email')
    ordering = ('username','user_email')

    filter_horizontal = ()

admin.site.register(CustomUser, MyUserAdmin)
