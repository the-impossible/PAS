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