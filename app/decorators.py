from django.http import HttpResponse 
from django.shortcuts import redirect, render 
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
        
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse(' ❌❌  you are  not autherised to use this page  ( and you know it..) ❌❌')
        return wrapper_func
    return decorator

def allowed_login(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
        
            user = None
            if request.user.user.exists():
                group = request.user.user.all()[0].name

            if user in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('you are  not autherised to use this page')
        return wrapper_func
    return decorator