# My django imports
from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.contrib import messages


# My app imports
from PAS_auth.views import EnforceAuth
from PAS_app.models import (
    Programme,
    Department,
)

# Create your views here.
class ValidateDepartment:
    def __init__(self, dept, request):
        self.dept = dept
        self.request = request

    @property
    def validate(self):
        try:
            dept = Department.objects.get(dept_id=self.dept)
            return dept

        except ObjectDoesNotExist:  pass

        except ValidationError: pass

        messages.error(self.request, 'Error Retrieving department!')
        return False


class WhatAssessmentView(EnforceAuth, View):

    def get(self, request, dept_id):
        dept = ValidateDepartment(dept_id, request).validate
        programmes = Programme.objects.all()

        if dept:
            return render(request, 'assess/what_assess.html', context={'dept':dept, 'programmes':programmes})

        return redirect('auth:list_department')