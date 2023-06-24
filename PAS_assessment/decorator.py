# My Django imports
from django.contrib.auth.models import AnonymousUser
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError

# My App imports
from PAS_app.models import (
    Department,
    Session,
)
from PAS_hallAllocation.models import (
    AssessorHallAllocation,
)

from PAS_auth.models import (
    SupervisorProfile,
    User,
)

# For validating the department via its id
def validate_department(func):
    def wrapper_func(request, *args, **kwargs):
        try:
            kwargs['dept_id'] = Department.objects.get(dept_id=kwargs['dept_id'])
            return func(request, *args, **kwargs)

        except ObjectDoesNotExist:  pass
        except ValidationError: pass

        messages.error(request, 'Error Retrieving department!')
        return redirect('auth:list_department')

    return wrapper_func

# For validating if the assessor is a chief assessor
def is_chief_assessor(func):
    def wrapper_func(request, *args, **kwargs):
        try:
            kwargs['dept_id'] = Department.objects.get(dept_id=kwargs['dept_id'])
            super_profile = SupervisorProfile.objects.get(user_id=request.user.user_id)
            allocation = AssessorHallAllocation.objects.get(dept_id=kwargs['dept_id'], chief_assessor=super_profile)
            return func(request, *args, **kwargs)

        except ObjectDoesNotExist:
            if request.user.is_staff:
                return func(request, *args, **kwargs)
        except ValidationError: pass

        messages.error(request, 'You are not authorized to make assessment!')
        return redirect('auth:dashboard')

    return wrapper_func

# For validating if the assessor is a super_assessor (Chief coordinator or superuser)
def is_super_assessor(func):
    def wrapper_func(request, *args, **kwargs):
        try:
            kwargs['dept_id'] = Department.objects.get(dept_id=kwargs['dept_id'])
            user = User.objects.get(username=request.user).is_staff
            if user:
                return func(request, *args, **kwargs)

        except ObjectDoesNotExist: pass
        except ValidationError: pass

        messages.error(request, 'You are not authorized to make assessment!')
        return redirect('auth:dashboard')

    return wrapper_func

# For validating that the user is a supervisor
def is_super(func):
    def wrapper_func(request, *args, **kwargs):
        try:
            kwargs['dept_id'] = Department.objects.get(dept_id=kwargs['dept_id'])
            user = User.objects.get(username=request.user).is_super

            if user:
                return func(request, *args, **kwargs)

        except ObjectDoesNotExist: pass
        except ValidationError: pass

        messages.error(request, 'You are not authorized to make assessment!')
        return redirect('auth:dashboard')

    return wrapper_func
