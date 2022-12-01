# My django imports
from django.shortcuts import render
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

# My app imports
from PAS_assessment.decorator import validate_department
from PAS_app.models import (
    Programme,
    Department,
)

# Create your views here.
@method_decorator(validate_department, name="get")
class WhatAssessmentView(LoginRequiredMixin, View):
    def get(self, request, dept_id):
        programmes = Programme.objects.all()

        return render(request, 'assess/what_assess.html', context={'dept':dept_id, 'programmes':programmes})