from functools import wraps
from django.http import HttpResponseForbidden
from .models import *

def get_user_group(user):
    user_group = user.groups.all()
    return user_group

def has_permission(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_group = get_user_group(request.user)
                if (user_group and user_group.filter(name=group_name).exists()):
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You don't have permission to do that.")
        return _wrapped_view
    return decorator