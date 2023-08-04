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
from PAS_assessment.decorator import validate_department, is_chief_assessor, is_super_assessor, is_super
from PAS_auth.decorator import *

from PAS_app.models import (
    Programme,
    Department,
    Session,
)

from PAS_hallAllocation.models import (
    AssessorHallAllocation,
    StudHallAllocation,
)
from PAS_auth.models import (
    SupervisorProfile,
    StudentProfile,
    User,
    Coordinators,
    StudentType,
    Allocate,
    Groups,
)

from PAS_assessment.form import(
    SeminarAssessmentForm,
    ProjectAssessmentForm,

    SupervisorAssessmentForm,
    SuperProjectAssessmentForm,
    ProgrammeTypeSelectionForm,
    SuperSeminarAssessmentForm,
    SuperSupervisorAssessmentForm,
)

from PAS_assessment.models import (
    Assessment,
    SeminarAssessment,
    ProjectAssessment,
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

                assessments = SeminarAssessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, venue=assessor.venue_id).order_by('-created')

                return render(request, 'assess/cr_seminar.html', context={'form':form, 'dept':dept_id, 'assessor':assessor, 'assessments':assessments})

            messages.error(request, 'You are not authorized!')
            return redirect('assess:what_assess', dept_id.dept_id)

        except SeminarAssessment.DoesNotExist:
            messages.error(request, 'You are not authorized!')
            return redirect('assess:what_assess', dept_id.dept_id)

    def post(self, request, dept_id):
        if not request.user.is_staff:
            supervisor = SupervisorProfile.objects.get(user_id=request.user)
            assessor = AssessorHallAllocation.objects.get(chief_assessor=supervisor)

            assessments = SeminarAssessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, venue=assessor.venue_id).order_by('-created')

            form = SeminarAssessmentForm(request.POST, assessor=assessor)

            if form.is_valid():
                grading = form.save(commit=False)
                student = grading.student_id

                try:
                    assessment = SeminarAssessment.objects.get(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, venue=assessor.venue_id, student_id=student)

                    assessment.assessor_id = supervisor
                    assessment.seminar_defense_grade = grading.seminar_defense_grade
                    assessment.save()

                except SeminarAssessment.DoesNotExist:

                    grading.assessor_id = supervisor
                    grading.venue = assessor.venue_id
                    grading.dept_id = assessor.dept_id
                    grading.sess_id = assessor.sess_id
                    grading.prog_id = assessor.prog_id
                    grading.type_id = assessor.type_id
                    grading.save()

                messages.success(request, f'{grading.student_id} seminar has been graded')
                return redirect('assess:assess_seminar', dept_id.pk)

            return render(request, 'assess/cr_seminar.html', context={'form':form, 'dept':dept_id, 'assessor':assessor, 'assessments':assessments})

        messages.error(request, 'Something went wrong!')
        return redirect('assess:what_assess', dept_id.dept_id)

@method_decorator(is_chief_assessor, name="get")
@method_decorator(is_chief_assessor, name="post")
class UDSeminarAssessmentView(LoginRequiredMixin, View):
    view_type = 'edit'
    def get(self, request, dept_id, assess_id):
        try:
            if not request.user.is_staff:
                supervisor = SupervisorProfile.objects.get(user_id=request.user)
                assessor = AssessorHallAllocation.objects.get(chief_assessor=supervisor)
                assessment = SeminarAssessment.objects.get(assess_id=assess_id)

                form = SeminarAssessmentForm(assessor=assessor, instance=assessment)

                assessments = SeminarAssessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, venue=assessor.venue_id).order_by('-created')

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

            assessments = SeminarAssessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, venue=assessor.venue_id).order_by('-created')

            assessment = SeminarAssessment.objects.get(assess_id=assess_id)

            if 'edit' in request.POST:
                form = SeminarAssessmentForm(request.POST, assessor=assessor, instance=assessment)

                if form.is_valid():
                    grading = form.save(commit=False)
                    grading.assessor_id = supervisor
                    grading.save()
                    messages.success(request, f'{grading.student_id} seminar grade has been edited')
                    return redirect('assess:assess_seminar', dept_id.pk)

                messages.error(request, f'{form.errors.as_text()}')
                return render(request, 'assess/cr_seminar.html', context={'form':form, 'dept':dept_id, 'assessor':assessor, 'assessments':assessments, 'type':self.view_type})

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

    def get(self, request, dept_id, grade_type):

        if grade_type == 's' or grade_type == 'p' or grade_type == 'sg':
            return render(request, 'assess/seminar_selection.html', context={'dept':dept_id, 'programmes':self.programmes, 'form':self.form, 'grade_type':'seminar'})

        messages.error(request, 'Invalid assessment selection')

        return redirect('assess:what_assess', dept_id.dept_id)


    def post(self, request, dept_id, grade_type):
        form = ProgrammeTypeSelectionForm(request.POST)

        if form.is_valid():
            prog_id = Programme.objects.get(programme_title=request.POST['prog_id'])

            if grade_type == 's':
                return redirect(to='assess:super_assess_seminar', dept_id=dept_id.pk, type_id=form.cleaned_data['student_type'].pk, prog_id=prog_id.pk, sess_id=form.cleaned_data['session'].pk)

            if grade_type == 'p':
                return redirect(to='assess:super_assess_project', dept_id=dept_id.pk, type_id=form.cleaned_data['student_type'].pk, prog_id=prog_id.pk, sess_id=form.cleaned_data['session'].pk)

            if grade_type == 'sg':
                return redirect(to='assess:super_assess_supervisor', dept_id=dept_id.pk, type_id=form.cleaned_data['student_type'].pk, prog_id=prog_id.pk, sess_id=form.cleaned_data['session'].pk)

        messages.error(request, 'Form not valid')

        return render(request, 'assess/seminar_selection.html', context={'dept':dept_id, 'programmes':self.programmes, 'form':form})

@method_decorator(is_super_assessor, name="get")
@method_decorator(is_super_assessor, name="post")
class CRSuperAssessorSeminarAssessmentView(LoginRequiredMixin, View):
    def get(self, request, dept_id, type_id, prog_id, sess_id):
        department_id = dept_id

        assessments = SeminarAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id).order_by('-created')

        form = SuperSeminarAssessmentForm(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id)
        return render(request, 'assess/cr_seminar.html', context={'dept':department_id, 'form':form, 'assessments':assessments})

    def post(self, request, dept_id, type_id, prog_id, sess_id):
        department_id = dept_id

        assessments = SeminarAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id).order_by('-created')
        form = SuperSeminarAssessmentForm(request.POST, dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id)

        if form.is_valid():
            grading = form.save(commit=False)
            student_id = grading.student_id

            if request.user.is_superuser:
                super_id = assessments.latest('created').assessor_id
            else:
                super_id = SupervisorProfile.objects.get(user_id=request.user)

            assessor = super_id

            try:
                assessment = SeminarAssessment.objects.get(dept_id=assessor.dept_id, type_id=type_id, prog_id=prog_id, sess_id=sess_id, student_id=student_id)

                assessment.seminar_defense_grade = grading.seminar_defense_grade
                assessment.save()

            except SeminarAssessment.DoesNotExist:

                grading.assessor_id = super_id
                grading.venue = grading.student_id.venue_id
                grading.dept_id = dept_id
                grading.sess_id = Session.objects.get(id=sess_id)
                grading.prog_id = Programme.objects.get(id=prog_id)
                grading.type_id = StudentType.objects.get(id=type_id)
                grading.save()

                messages.success(request, f'{grading.student_id} seminar has been graded')
                return redirect('assess:super_assess_seminar', department_id.pk, type_id, prog_id, sess_id)


        messages.error(request, f'{form.errors.as_text()}')
        return render(request, 'assess/cr_seminar.html', context={'dept':department_id, 'form':form, 'assessments':assessments})

@method_decorator(is_super_assessor, name="get")
@method_decorator(is_super_assessor, name="post")
class CRSuperAssessorProjectAssessmentView(LoginRequiredMixin, View):
    def get(self, request, dept_id, type_id, prog_id, sess_id):
        department_id = dept_id
        assessments = ProjectAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, project_defense_grade__gt=0).order_by('-created')

        form = SuperProjectAssessmentForm(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id)
        return render(request, 'assess/cr_project.html', context={'dept':department_id, 'form':form, 'assessments':assessments})

    def post(self, request, dept_id, type_id, prog_id, sess_id):
        department_id = dept_id
        assessments = ProjectAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, project_defense_grade__gt=0).order_by('-created')
        form = SuperProjectAssessmentForm(request.POST, dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id)

        if form.is_valid():
            grading = form.save(commit=False)
            student_id = grading.student_id

            if request.user.is_superuser:
                super_id = assessments.latest('created').assessor_id
            else:
                super_id = SupervisorProfile.objects.get(user_id=request.user)

            assessor = super_id

            try:
                assessment = ProjectAssessment.objects.get(dept_id=assessor.dept_id, type_id=type_id, prog_id=prog_id, sess_id=sess_id, student_id=student_id)

                assessment.project_defense_grade = grading.project_defense_grade
                assessment.assessor_id = super_id
                assessment.venue = grading.student_id.venue_id
                assessment.save()

            except ProjectAssessment.DoesNotExist:

                grading.assessor_id = super_id
                grading.venue = grading.student_id.venue_id
                grading.dept_id = dept_id
                grading.sess_id = Session.objects.get(id=sess_id)
                grading.prog_id = Programme.objects.get(id=prog_id)
                grading.type_id = StudentType.objects.get(id=type_id)
                grading.save()

                messages.success(request, f'{grading.student_id} project defense has been graded')
                return redirect('assess:super_assess_project', department_id.pk, type_id, prog_id, sess_id)


        messages.error(request, f'{form.errors.as_text()}')
        return render(request, 'assess/cr_project.html', context={'dept':department_id, 'form':form, 'assessments':assessments})


@method_decorator(is_super_assessor, name="get")
@method_decorator(is_super_assessor, name="post")
class UDSuperAssessorSeminarAssessmentView(LoginRequiredMixin, View):
    view_type = 'edit'
    def get(self, request, dept_id, type_id, prog_id, sess_id, assess_id):
        department_id = dept_id

        assessments = SeminarAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id).order_by('-created')
        assessment = SeminarAssessment.objects.get(assess_id=assess_id)

        form = SuperSeminarAssessmentForm(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, instance=assessment)

        return render(request, 'assess/cr_seminar.html', context={'dept':department_id, 'form':form, 'assessments':assessments, 'type':self.view_type})

    def post(self, request, dept_id, type_id, prog_id, sess_id, assess_id):
        department_id = dept_id
        assessment = SeminarAssessment.objects.get(assess_id=assess_id)

        assessments = SeminarAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id).order_by('-created')

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

                return redirect('assess:super_assess_seminar', department_id.pk, type_id, prog_id, sess_id)

            messages.error(request, f'{form.errors.as_text()}')

            return render(request, 'assess/cr_seminar.html', context={'dept':department_id, 'form':form, 'assessments':assessments, 'type':self.view_type})

        elif 'delete' in request.POST:
            assessment.delete()
            messages.success(request, f'Seminar assessment deleted!')

        else:
            messages.warning(request, f'Something went wrong!')

        return redirect('assess:super_assess_seminar', department_id.pk, type_id, prog_id, sess_id)

@method_decorator(is_super_assessor, name="get")
@method_decorator(is_super_assessor, name="post")
class UDSuperAssessorProjectAssessmentView(LoginRequiredMixin, View):
    view_type = 'edit'
    def get(self, request, dept_id, type_id, prog_id, sess_id, assess_id):
        department_id = dept_id
        assessments = ProjectAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, project_defense_grade__gt=0).order_by('-created')
        assessment = ProjectAssessment.objects.get(assess_id=assess_id)

        form = SuperProjectAssessmentForm(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, instance=assessment)

        return render(request, 'assess/cr_project.html', context={'dept':department_id, 'form':form, 'assessments':assessments, 'type':self.view_type})

    def post(self, request, dept_id, type_id, prog_id, sess_id, assess_id):
        department_id = dept_id
        assessments = ProjectAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, project_defense_grade__gt=0).order_by('-created')
        assessment = ProjectAssessment.objects.get(assess_id=assess_id)

        if 'edit' in request.POST:
            form = SuperProjectAssessmentForm(request.POST, dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, instance=assessment)

            if form.is_valid():
                grading = form.save(commit=False)
                if request.user.is_superuser:
                    super_id = assessment.assessor_id
                else:
                    super_id = SupervisorProfile.objects.get(user_id=request.user)
                grading.assessor_id = super_id
                grading.save()

                messages.success(request, f'{grading.student_id} project defense grade has been edited')

                return redirect('assess:super_assess_project', department_id.pk, type_id, prog_id, sess_id)

            messages.error(request, f'{form.errors.as_text()}')

            return render(request, 'assess/cr_project.html', context={'dept':department_id, 'form':form, 'assessments':assessments, 'type':self.view_type})

        elif 'delete' in request.POST:
            if assessment.supervisor_grade > 0:
                assessment.project_defense_grade = 0
                assessment.save()
            else:
                assessment.delete()
            messages.success(request, f'Project assessment deleted!')

        else:
            messages.warning(request, f'Something went wrong!')

        return redirect('assess:super_assess_project', department_id.pk, type_id, prog_id, sess_id)

# PROJECT
@method_decorator(is_chief_assessor, name="get")
@method_decorator(is_chief_assessor, name="post")
class CRProjectAssessmentView(LoginRequiredMixin, View):
    def get(self, request, dept_id):
        try:
            if not request.user.is_staff:
                supervisor = SupervisorProfile.objects.get(user_id=request.user)
                assessor = AssessorHallAllocation.objects.get(chief_assessor=supervisor)

                form = ProjectAssessmentForm(assessor=assessor)

                assessments = ProjectAssessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, venue=assessor.venue_id, project_defense_grade__gt=0).order_by('-created')

                return render(request, 'assess/cr_project.html', context={'form':form, 'dept':dept_id, 'assessor':assessor, 'assessments':assessments})

            messages.error(request, 'You are not authorized!')
            return redirect('assess:what_assess', dept_id)

        except ObjectDoesNotExist():
            messages.error(request, 'You are not authorized!')
            return redirect('assess:what_assess', dept_id)

    def post(self, request, dept_id):
        if not request.user.is_staff:
            supervisor = SupervisorProfile.objects.get(user_id=request.user)
            assessor = AssessorHallAllocation.objects.get(chief_assessor=supervisor)

            assessments = ProjectAssessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, venue=assessor.venue_id, project_defense_grade__gt=0).order_by('-created')

            form = ProjectAssessmentForm(request.POST, assessor=assessor)


            if form.is_valid():

                grading = form.save(commit=False)
                student_id = grading.student_id

                try:
                    assessment = ProjectAssessment.objects.get(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, venue=assessor.venue_id, student_id=student_id)

                    assessment.project_defense_grade = grading.project_defense_grade
                    assessment.assessor_id = supervisor
                    assessment.save()

                except ProjectAssessment.DoesNotExist:
                    grading.assessor_id = supervisor
                    grading.venue = assessor.venue_id
                    grading.dept_id = assessor.dept_id
                    grading.sess_id = assessor.sess_id
                    grading.prog_id = assessor.prog_id
                    grading.type_id = assessor.type_id
                    grading.save()

                messages.success(request, f'{grading.student_id} project defense has been graded')
                return redirect('assess:assess_project', dept_id.pk)

            return render(request, 'assess/cr_project.html', context={'form':form, 'dept':dept_id, 'assessor':assessor, 'assessments':assessments})

        messages.error(request, 'Something went wrong!')
        return redirect('assess:what_assess', dept_id)


@method_decorator(is_chief_assessor, name="get")
@method_decorator(is_chief_assessor, name="post")
class UDProjectAssessmentView(LoginRequiredMixin, View):
    view_type = 'edit'
    def get(self, request, dept_id, assess_id):
        try:
            if not request.user.is_staff:
                supervisor = SupervisorProfile.objects.get(user_id=request.user)
                assessor = AssessorHallAllocation.objects.get(chief_assessor=supervisor)
                assessment = ProjectAssessment.objects.get(assess_id=assess_id)

                form = ProjectAssessmentForm(assessor=assessor, instance=assessment)

                assessments = ProjectAssessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id, venue=assessor.venue_id, project_defense_grade__gt=0).order_by('-created')


                return render(request, 'assess/cr_project.html', context={'form':form, 'dept':dept_id, 'assessor':assessor, 'assessments':assessments, 'type':self.view_type})

            messages.error(request, 'You are not authorized!')
            return redirect('assess:what_assess', dept_id)
        except ObjectDoesNotExist():
            messages.error(request, 'You are not authorized!')
            return redirect('assess:what_assess', dept_id)

    def post(self, request, dept_id, assess_id):

        if not request.user.is_staff:

            supervisor = SupervisorProfile.objects.get(user_id=request.user)
            assessor = AssessorHallAllocation.objects.get(chief_assessor=supervisor)

            assessments = ProjectAssessment.objects.filter(dept_id=assessor.dept_id, type_id=assessor.type_id, prog_id=assessor.prog_id, sess_id=assessor.sess_id,  venue=assessor.venue_id, project_defense_grade__gt=0).order_by('-created')

            assessment = ProjectAssessment.objects.get(assess_id=assess_id)

            if 'edit' in request.POST:
                form = ProjectAssessmentForm(request.POST, assessor=assessor, instance=assessment)

                if form.is_valid():
                    grading = form.save(commit=False)
                    grading.assessor_id = supervisor
                    grading.save()
                    messages.success(request, f'{grading.student_id} project grade has been edited')
                    return redirect('assess:assess_project', dept_id.pk)

                messages.error(request, f'{form.errors.as_text()}')
                return render(request, 'assess/cr_project.html', context={'form':form, 'dept':dept_id, 'assessor':assessor, 'assessments':assessments})

            elif 'delete' in request.POST:
                if assessment.supervisor_grade > 0:
                    assessment.project_defense_grade = 0
                    assessment.save()
                else:
                    assessment.delete()
                messages.success(request, 'Assessment has been deleted!')

            else:
                messages.error(request, 'Something went wrong!')

            return redirect('assess:assess_project', dept_id.pk)

        messages.error(request, 'Something went wrong!')
        return redirect('assess:what_assess', dept_id)

@method_decorator(has_updated, name="get")
@method_decorator(has_updated, name="post")
class GradeStudentView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    programmes = Programme.objects.all()

    def get(self, request):
        try:

            assessor = SupervisorProfile.objects.get(user_id=request.user)

            form1 = SupervisorAssessmentForm(assessor=assessor, programme='nd')
            form2 = SupervisorAssessmentForm(assessor=assessor, programme='hnd')

            allocation_nd = Allocate.objects.filter(super_id=assessor, prog_id=Programme.objects.get(programme_title='ND'))
            value_to_filter_nd = allocation_nd.values('stud_id')
            student_hall = StudHallAllocation.objects.filter(stud_id__in=value_to_filter_nd)

            assessments_nd = ProjectAssessment.objects.filter(student_id__in=student_hall, supervisor_grade__gt=0).order_by('-created')

            allocation_hnd = Allocate.objects.filter(super_id=assessor, prog_id=Programme.objects.get(programme_title='HND'))

            value_to_filter = allocation_hnd.values('stud_id')
            student_hall = StudHallAllocation.objects.filter(stud_id__in=value_to_filter)
            assessments_hnd = ProjectAssessment.objects.filter(student_id__in=student_hall, supervisor_grade__gt=0).order_by('-created')


            return render(request, 'assess/grade_students.html', context={'programmes':self.programmes, 'form1':form1, 'form2':form2, 'assessments_nd':assessments_nd, 'assessments_hnd':assessments_hnd, 'allocation_nd':allocation_nd, 'allocation_hnd':allocation_hnd})

        except SupervisorProfile.DoesNotExist:
            messages.success(request, 'Unable to get your account profile')
            return redirect('auth:dashboard')

    def post(self, request):

        assessor = SupervisorProfile.objects.get(user_id=request.user)

        allocation_nd = Allocate.objects.filter(super_id=assessor, prog_id=Programme.objects.get(programme_title='ND'))
        value_to_filter_nd = allocation_nd.values('stud_id')
        student_hall = StudHallAllocation.objects.filter(stud_id__in=value_to_filter_nd)

        assessments_nd = ProjectAssessment.objects.filter(student_id__in=student_hall, supervisor_grade__gt=0).order_by('-created')

        allocation_hnd = Allocate.objects.filter(super_id=assessor, prog_id=Programme.objects.get(programme_title='HND'))

        value_to_filter = allocation_hnd.values('stud_id')
        student_hall = StudHallAllocation.objects.filter(stud_id__in=value_to_filter)
        assessments_hnd = ProjectAssessment.objects.filter(student_id__in=student_hall, supervisor_grade__gt=0).order_by('-created')


        try:

            form1 = SupervisorAssessmentForm(request.POST, assessor=assessor, programme='nd')
            form2 = SupervisorAssessmentForm(request.POST, assessor=assessor, programme='hnd')

            if 'ND' in request.POST:
                form1 = SupervisorAssessmentForm(request.POST, assessor=assessor, programme='nd')

                if form1.is_valid():

                    grading = form1.save(commit=False)
                    student_id = grading.student_id

                    try:
                        assessment = ProjectAssessment.objects.get(student_id=student_id)

                        assessment.supervisor_grade = grading.supervisor_grade
                        assessment.supervisor = assessor
                        assessment.save()

                    except ProjectAssessment.DoesNotExist:

                        grading.supervisor = assessor
                        grading.dept_id = student_id.dept_id
                        grading.sess_id = student_id.sess_id
                        grading.prog_id = student_id.prog_id
                        grading.type_id = student_id.type_id
                        grading.save()

                        messages.success(request, f'{grading.student_id} has been graded')
                        return redirect('assess:grade_student')

                messages.error(request, f'{form1.errors.as_text()}')
                return render(request, 'assess/grade_students.html', context={'programmes':self.programmes, 'form1':form1, 'form2':SupervisorAssessmentForm(assessor=assessor, programme='hnd'), 'assessments_nd':assessments_nd, 'assessments_hnd':assessments_hnd, 'allocation_nd':allocation_nd, 'allocation_hnd':allocation_hnd})


            if 'HND' in request.POST:
                form2 = SupervisorAssessmentForm(request.POST, assessor=assessor, programme='hnd')


                if form2.is_valid():

                    grading = form2.save(commit=False)
                    student_id = grading.student_id

                    try:
                        assessment = ProjectAssessment.objects.get(student_id=student_id)

                        assessment.supervisor_grade = grading.supervisor_grade
                        assessment.supervisor = assessor
                        assessment.save()

                    except ProjectAssessment.DoesNotExist:

                        grading.supervisor = assessor
                        grading.dept_id = student_id.dept_id
                        grading.sess_id = student_id.sess_id
                        grading.prog_id = student_id.prog_id
                        grading.type_id = student_id.type_id
                        grading.save()

                    messages.success(request, f'{grading.student_id} has been graded')
                    return redirect('assess:grade_student')


                messages.error(request, f'{form2.errors.as_text()}')

                return render(request, 'assess/grade_students.html', context={'programmes':self.programmes, 'form1':SupervisorAssessmentForm(assessor=assessor, programme='nd'), 'form2':form2, 'assessments_nd':assessments_nd, 'assessments_hnd':assessments_hnd, 'allocation_nd':allocation_nd, 'allocation_hnd':allocation_hnd})


            messages.error(request, f'Unable to process request')
            return redirect('assess:grade_student')

        except SupervisorProfile.DoesNotExist:
            messages.success(request, 'Unable to fetch your account profile')
            return redirect('auth:dashboard')

@method_decorator(has_updated, name="get")
@method_decorator(has_updated, name="post")
class UDGradeStudentView(LoginRequiredMixin, View):
    view_type = 'edit'
    programmes = Programme.objects.all()

    def get(self, request, assess_id, type_id):
        try:
            assessor = SupervisorProfile.objects.get(user_id=request.user)
            assessment = ProjectAssessment.objects.get(assess_id=assess_id)

            form1 = SupervisorAssessmentForm(assessor=assessor, programme='nd')
            form2 = SupervisorAssessmentForm(assessor=assessor, programme='hnd')

            if type_id == '1':
                form1 = SupervisorAssessmentForm(assessor=assessor, programme='nd', instance=assessment)
            if type_id == '2':
                form2 = SupervisorAssessmentForm(assessor=assessor, programme='hnd', instance=assessment)

            allocation_nd = Allocate.objects.filter(super_id=assessor, prog_id=Programme.objects.get(programme_title='ND'))
            value_to_filter_nd = allocation_nd.values('stud_id')
            student_hall = StudHallAllocation.objects.filter(stud_id__in=value_to_filter_nd)

            assessments_nd = ProjectAssessment.objects.filter(student_id__in=student_hall, supervisor_grade__gt=0).order_by('-created')

            allocation_hnd = Allocate.objects.filter(super_id=assessor, prog_id=Programme.objects.get(programme_title='HND'))

            value_to_filter = allocation_hnd.values('stud_id')
            student_hall = StudHallAllocation.objects.filter(stud_id__in=value_to_filter)
            assessments_hnd = ProjectAssessment.objects.filter(student_id__in=student_hall, supervisor_grade__gt=0).order_by('-created')


            return render(request, 'assess/grade_students.html', context={'programmes':self.programmes, 'form1':form1, 'form2':form2, 'assessments_nd':assessments_nd, 'assessments_hnd':assessments_hnd, 'allocation_nd':allocation_nd, 'allocation_hnd':allocation_hnd, 'type':self.view_type})

        except SupervisorProfile.DoesNotExist:
            messages.error(request, 'You are not authorized!')
        except Assessment.DoesNotExist:
            messages.error(request, 'Failed to get assessment!')
        return redirect('assess:grade_student')

    def post(self, request, assess_id, type_id):

        assessor = SupervisorProfile.objects.get(user_id=request.user)
        assessment = ProjectAssessment.objects.get(assess_id=assess_id)

        form1 = SupervisorAssessmentForm(assessor=assessor, programme='nd')
        form2 = SupervisorAssessmentForm(assessor=assessor, programme='hnd')

        allocation_nd = Allocate.objects.filter(super_id=assessor, prog_id=Programme.objects.get(programme_title='ND'))
        value_to_filter_nd = allocation_nd.values('stud_id')
        student_hall = StudHallAllocation.objects.filter(stud_id__in=value_to_filter_nd)

        assessments_nd = ProjectAssessment.objects.filter(student_id__in=student_hall, supervisor_grade__gt=0).order_by('-created')

        allocation_hnd = Allocate.objects.filter(super_id=assessor, prog_id=Programme.objects.get(programme_title='HND'))

        value_to_filter = allocation_hnd.values('stud_id')
        student_hall = StudHallAllocation.objects.filter(stud_id__in=value_to_filter)
        assessments_hnd = ProjectAssessment.objects.filter(student_id__in=student_hall, supervisor_grade__gt=0).order_by('-created')


        if 'edit' in request.POST and 'ND' in request.POST:

            form1 = SupervisorAssessmentForm(request.POST, assessor=assessor, programme='nd', instance=assessment)

            if form1.is_valid():
                grading = form1.save(commit=False)
                grading.supervisor = assessor
                grading.save()
                messages.success(request, f'{grading.student_id} supervisor grade has been edited')
                return redirect('assess:grade_student')

            messages.error(request, f'{form1.errors.as_text()}')

            return render(request, 'assess/grade_students.html', context={'programmes':self.programmes, 'form1':form1, 'form2':SupervisorAssessmentForm(assessor=assessor, programme='hnd'), 'assessments_nd':assessments_nd, 'assessments_hnd':assessments_hnd, 'allocation_nd':allocation_nd, 'allocation_hnd':allocation_hnd, 'type':self.view_type})

        if 'edit' in request.POST and 'HND' in request.POST:

            form2 = SupervisorAssessmentForm(request.POST, assessor=assessor, programme='hnd', instance=assessment)


            if form2.is_valid():
                grading = form2.save(commit=False)
                grading.supervisor = assessor
                grading.save()
                messages.success(request, f'{grading.student_id} supervisor grade has been edited')
                return redirect('assess:grade_student')

            messages.error(request, f'{form2.errors.as_text()}')

            return render(request, 'assess/grade_students.html', context={'programmes':self.programmes, 'form1':SupervisorAssessmentForm(assessor=assessor, programme='nd'), 'form2':form2, 'assessments_nd':assessments_nd, 'assessments_hnd':assessments_hnd, 'allocation_nd':allocation_nd, 'allocation_hnd':allocation_hnd, 'type':self.view_type})

        elif 'delete' in request.POST:
            if assessment.project_defense_grade > 0:
                assessment.supervisor_grade = 0
                assessment.save()
            else:
                assessment.delete()

            messages.success(request, 'Assessment has been deleted!')
            return redirect('assess:grade_student')

        else:
            messages.error(request, 'Something went wrong!')

        return redirect('assess:grade_student')

@method_decorator(is_super_assessor, name="get")
@method_decorator(is_super_assessor, name="post")
class CRSuperSupervisorAssessmentView(LoginRequiredMixin, View):
    def get(self, request, dept_id, type_id, prog_id, sess_id):
        department_id = dept_id
        assessments = ProjectAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, supervisor_grade__gt=0).order_by('-created')

        form = SuperSupervisorAssessmentForm(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id)
        return render(request, 'assess/cr_supervisor_grade.html', context={'dept':department_id, 'form':form, 'assessments':assessments})

    def post(self, request, dept_id, type_id, prog_id, sess_id):
        department_id = dept_id
        assessments = ProjectAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, supervisor_grade__gt=0).order_by('-created')
        form = SuperSupervisorAssessmentForm(request.POST, dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id)

        if form.is_valid():
            grading = form.save(commit=False)
            student_id = grading.student_id

            if request.user.is_superuser:
                super_id = assessments.latest('created').assessor_id
            else:
                super_id = SupervisorProfile.objects.get(user_id=request.user)

            assessor = super_id

            try:
                assessment = ProjectAssessment.objects.get(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, student_id=student_id)

                assessment.supervisor_grade = grading.supervisor_grade
                assessment.supervisor = super_id
                assessment.save()

            except ProjectAssessment.DoesNotExist:

                grading.supervisor = super_id
                grading.venue = grading.student_id.venue_id
                grading.dept_id = dept_id
                grading.sess_id = Session.objects.get(id=sess_id)
                grading.prog_id = Programme.objects.get(id=prog_id)
                grading.type_id = StudentType.objects.get(id=type_id)
                grading.save()

                messages.success(request, f'{grading.student_id} supervisor grade has been graded')
                return redirect('assess:super_assess_supervisor', department_id.pk, type_id, prog_id, sess_id)


        messages.error(request, f'{form.errors.as_text()}')
        return render(request, 'assess/cr_supervisor_grade.html', context={'dept':department_id, 'form':form, 'assessments':assessments})

@method_decorator(is_super_assessor, name="get")
@method_decorator(is_super_assessor, name="post")
class UDSuperAssessorProjectAssessmentView(LoginRequiredMixin, View):
    view_type = 'edit'

    def get(self, request, dept_id, type_id, prog_id, sess_id, assess_id):
        department_id = dept_id
        assessments = ProjectAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, supervisor_grade__gt=0).order_by('-created')
        assessment = ProjectAssessment.objects.get(assess_id=assess_id)

        form = SuperSupervisorAssessmentForm(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, instance=assessment)

        return render(request, 'assess/cr_supervisor_grade.html', context={'dept':department_id, 'form':form, 'assessments':assessments, 'type':self.view_type})

    def post(self, request, dept_id, type_id, prog_id, sess_id, assess_id):
        department_id = dept_id
        assessments = ProjectAssessment.objects.filter(dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, supervisor_grade__gt=0).order_by('-created')
        assessment = ProjectAssessment.objects.get(assess_id=assess_id)

        if 'edit' in request.POST:
            form = SuperSupervisorAssessmentForm(request.POST, dept_id=department_id.pk, type_id=type_id, prog_id=prog_id, sess_id=sess_id, instance=assessment)

            if form.is_valid():
                grading = form.save(commit=False)
                if request.user.is_superuser:
                    super_id = assessment.assessor_id
                else:
                    super_id = SupervisorProfile.objects.get(user_id=request.user)
                grading.supervisor = super_id
                grading.save()

                messages.success(request, f'{grading.student_id} supervisor grade has been edited')

                return redirect('assess:super_assess_supervisor', department_id.pk, type_id, prog_id, sess_id)

            messages.error(request, f'{form.errors.as_text()}')

            return render(request, 'assess/cr_supervisor_grade.html', context={'dept':department_id, 'form':form, 'assessments':assessments, 'type':self.view_type})

        elif 'delete' in request.POST:
            if assessment.project_defense_grade > 0:
                assessment.supervisor_grade = 0
                assessment.save()
            else:
                assessment.delete()
            messages.success(request, f'Supervisor assessment deleted!')

        else:
            messages.warning(request, f'Something went wrong!')

        return redirect('assess:super_assess_supervisor', department_id.pk, type_id, prog_id, sess_id)


