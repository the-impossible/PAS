# My django imports
from django.contrib.auth.models import AnonymousUser
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages

# My app imports

# Determining if the user is an admin
def is_staff(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return func(request, *args, **kwargs)
            else:
                messages.warning(request, 'You are not authorized to view that page')
                return redirect('auth:dashboard')
    return wrapper_func

# Determining if the user is a supervisor
def is_super(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_super:
                return func(request, *args, **kwargs)
            else:
                messages.warning(request, 'You are not authorized to view this page')
                return redirect('auth:dashboard')
    return wrapper_func

# When a user tries logging out when they are not even authenticated
def only_authenticated_users(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            messages.warning(request, 'You can not logout when you are not logged in!')
            return redirect('app:home')
    return wrapper_func

# Determine if user has updated their account or account
def has_updated(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.has_updated():
            return func(request, *args, **kwargs)
        else:
            messages.info(request, 'You have to update your profile before proceeding!')
            return redirect('auth:manage_profile', request.user.user_id)
    return wrapper_func
