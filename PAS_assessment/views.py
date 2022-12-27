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
from PAS_assessment.decorator import validate_department, is_chief_assessor, is_super_assessor
from PAS_app.models import (
    Programme,
    Department,
    Session,
)

from PAS_hallAllocation.models import (
    AssessorHallAllocation,
)
from PAS_auth.models import (
    SupervisorProfile,
    User,
    Coordinators,
    StudentType,
)

from PAS_assessment.form import(
    SeminarAssessmentForm,
    ProgrammeTypeSelectionForm,
    SuperSeminarAssessmentForm,
)

from PAS_assessment.models import (
    Assessment,
)

# Create your views here.
@method_decorator(is_chief_assessor, name="get")
class WhatAssessmentView(LoginRequiredMixin, View):
    def get(self, request, dept_id):
        return render(request, 'assess/what_assess.html', context={'dept':dept_id})

@method_decorator(is_chief_assessor, name="get")
@method_decorator(is_chief_assessor, name="post")
class CRSeminarAssessmentView(LoginRequiredMixin, View):
    def get(self, request, dept_id):
        try:
            if not request.user.is_staff:
                supervisor = SupervisorProfile.objects.get(user_id=request.user)
                assessor = AssessorHallAllocation.objects.get(chief_assessor=supervisor)

                form = SeminarAssessmentForm(assessor=assessor)

                assessments = Assessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, assessor_id=assessor.chief_assessor).order_by('-created')

                return render(request, 'assess/cr_seminar.html', context={'form':form, 'dept':dept_id, 'assessor':assessor, 'assessments':assessments})
            messages.error(request, 'You are not authorized!')
            return redirect('assess:what_assess', dept_id)
        except ObjectDoesNotExist():
            messages.error(request, 'You are not authorized!')
            return redirect('assess:what_assess', dept_id)

    def post(self, request, dept_id):
        if not request.user.is_staff:
            supervisor = SupervisorProfile.objects.get(user_id=request.user)
            assessor = AssessorHallAllocation.objects.get(chief_assessor=supervisor)

            assessments = Assessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, assessor_id=assessor.chief_assessor).order_by('-created')

            form = SeminarAssessmentForm(request.POST, assessor=assessor)

            if form.is_valid():
                grading = form.save(commit=False)
                grading.assessor_id = supervisor
                grading.dept_id = assessor.dept_id
                grading.sess_id = assessor.sess_id
                grading.prog_id = assessor.prog_id
                grading.type_id = assessor.type_id
                grading.save()

                messages.success(request, f'{grading.student_id} seminar has been graded')
                return redirect('assess:assess_seminar', dept_id.pk)

            return render(request, 'assess/cr_seminar.html', context={'form':form, 'dept':dept_id, 'assessor':assessor, 'assessments':assessments})

        messages.error(request, 'Something went wrong!')
        return redirect('assess:what_assess', dept_id)

@method_decorator(is_chief_assessor, name="get")
@method_decorator(is_chief_assessor, name="post")
class UDSeminarAssessmentView(LoginRequiredMixin, View):
    view_type = 'edit'
    def get(self, request, dept_id, assess_id):
        try:
            if not request.user.is_staff:
                supervisor = SupervisorProfile.objects.get(user_id=request.user)
                assessor = AssessorHallAllocation.objects.get(chief_assessor=supervisor)
                assessment = Assessment.objects.get(assess_id=assess_id)

                form = SeminarAssessmentForm(assessor=assessor, instance=assessment)

                assessments = Assessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, assessor_id=assessor.chief_assessor).order_by('-created')

                return render(request, 'assess/cr_seminar.html', context={'form':form, 'dept':dept_id, 'assessor':assessor, 'assessments':assessments, 'type':self.view_type})
            messages.error(request, 'You are not authorized!')
            return redirect('assess:what_assess', dept_id)
        except ObjectDoesNotExist():
            messages.error(request, 'You are not authorized!')
            return redirect('assess:what_assess', dept_id)

    def post(self, request, dept_id, assess_id):
        if not request.user.is_staff:
            supervisor = SupervisorProfile.objects.get(user_id=request.user)
            assessor = AssessorHallAllocation.objects.get(chief_assessor=supervisor)

            assessments = Assessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, assessor_id=assessor.chief_assessor).order_by('-created')
            assessment = Assessment.objects.get(assess_id=assess_id)

            if 'edit' in request.POST:
                form = SeminarAssessmentForm(request.POST, assessor=assessor, instance=assessment)

                if form.is_valid():
                    grading = form.save(commit=False)
                    grading.assessor_id = supervisor
                    grading.save()
                    messages.success(request, f'{grading.student_id} seminar grade has been edited')

            elif 'delete' in request.POST:
                assessment.delete()
                messages.success(request, 'Assessment has been deleted!')

            else:
                messages.error(request, 'Something went wrong!')

            return redirect('assess:assess_seminar', dept_id.pk)

        messages.error(request, 'Something went wrong!')
        return redirect('assess:what_assess', dept_id)

@method_decorator(is_super_assessor, name="get")
@method_decorator(is_super_assessor, name="post")
class ProgrammeTypeSelectionView(LoginRequiredMixin, View):
    programmes = Programme.objects.all()
    form = ProgrammeTypeSelectionForm()
    def get(self, request, dept_id):
        return render(request, 'assess/seminar_selection.html', context={'dept':dept_id, 'programmes':self.programmes, 'form':self.form})

    def post(self, request, dept_id):
        form = ProgrammeTypeSelectionForm(request.POST)

        if form.is_valid():
            prog_id = Programme.objects.get(programme_title=request.POST['prog_id'])
            return redirect(to='assess:super_assess_seminar', dept_id=dept_id.pk, type_id=form.cleaned_data['student_type'].pk, prog_id=prog_id.pk, sess_id=form.cleaned_data['session'].pk)

        messages.error(request, 'Form not valid')
        return render(request, 'assess/seminar_selection.html', context={'dept':dept_id, 'programmes':self.programmes, 'form':form})

@method_decorator(is_super_assessor, name="get")
@method_decorator(is_super_assessor, name="post")
class CRSuperAssessorSeminarAssessmentView(LoginRequiredMixin, View):
    def get(self, request, dept_id, type_id, prog_id, sess_id):
        department_id = dept_id
        assessments = Assessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id).order_by('-created')

        form = SuperSeminarAssessmentForm(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id)
        return render(request, 'assess/cr_seminar.html', context={'dept':department_id, 'form':form, 'assessments':assessments})

    def post(self, request, dept_id, type_id, prog_id, sess_id):
        department_id = dept_id
        assessments = Assessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id).order_by('-created')
        form = SuperSeminarAssessmentForm(request.POST, dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id)

        if form.is_valid():
            grading = form.save(commit=False)
            if request.user.is_superuser:
                super_id = assessments.latest('created').assessor_id
            else:
                super_id = SupervisorProfile.objects.get(user_id=request.user)
            grading.assessor_id = super_id
            grading.dept_id = dept_id
            grading.sess_id = Session.objects.get(id=sess_id)
            grading.prog_id = Programme.objects.get(id=prog_id)
            grading.type_id = StudentType.objects.get(id=type_id)
            grading.save()

            messages.success(request, f'{grading.student_id} seminar has been graded')
            return redirect('assess:super_assess_seminar', department_id.pk, type_id, prog_id, sess_id)

        return render(request, 'assess/cr_seminar.html', context={'dept':department_id, 'form':form, 'assessments':assessments})

@method_decorator(is_super_assessor, name="get")
@method_decorator(is_super_assessor, name="post")
class UDSuperAssessorSeminarAssessmentView(LoginRequiredMixin, View):
    view_type = 'edit'
    def get(self, request, dept_id, type_id, prog_id, sess_id, assess_id):
        department_id = dept_id
        assessments = Assessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id).order_by('-created')
        assessment = Assessment.objects.get(assess_id=assess_id)

        form = SuperSeminarAssessmentForm(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, instance=assessment)

        return render(request, 'assess/cr_seminar.html', context={'dept':department_id, 'form':form, 'assessments':assessments, 'type':self.view_type})

    def post(self, request, dept_id, type_id, prog_id, sess_id, assess_id):
        department_id = dept_id
        assessment = Assessment.objects.get(assess_id=assess_id)

        if 'edit' in request.POST:
            form = SuperSeminarAssessmentForm(request.POST, dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, instance=assessment)

            if form.is_valid():
                grading = form.save(commit=False)
                if request.user.is_superuser:
                    super_id = assessment.assessor_id
                else:
                    super_id = SupervisorProfile.objects.get(user_id=request.user)
                grading.assessor_id = super_id
                grading.save()

                messages.success(request, f'{grading.student_id} seminar grade has been edited')

        elif 'delete' in request.POST:
            assessment.delete()
            messages.success(request, f'Seminar assessment deleted!')

        else:
            messages.warning(request, f'Something went wrong!')

        return redirect('assess:super_assess_seminar', department_id.pk, type_id, prog_id, sess_id)


