# My Django imports
from django.shortcuts import render, redirect, reverse
from django.views import View
import csv
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

# My App imports
from PAS_app.models import (
    Files,
    Programme,
    Department,
    Session,
    SupervisorsFiles,
    StudentType,
    SupervisorRank,
)
from PAS_auth.models import (
    User,
    StudentProfile,
    SupervisorProfile,
    Coordinators,
)
from PAS_app.form import (
    FilesForm,
    SuperFilesForm,
    SupervisorProfileForm,
    StudentProfileForm,
    MultipleStudentForm,
    MultipleSuperForm,
    CoordinatorsForm,
)
from PAS_auth.form import (
    UserForm,
)

PASSWORD = '12345678'

# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        if username and password:
            # Authenticate user
            user = authenticate(request, username=username.upper(), password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'You are now signed in {user}')
                    return redirect('auth:dashboard')
                else:
                    messages.warning(request, 'Account not active contact the administrator')
                    return redirect('auth:login')
            messages.warning(request, 'Invalid login credentials')
            return redirect('auth:login')
        else:
            messages.error(request, 'All fields are required!!')
            return redirect('auth:login')

class LogoutView(LoginRequiredMixin, View):
    login_url = 'auth:login'
    def post(self, request):
        logout(request)
        messages.success(request, 'You are successfully logged out, to continue login again')
        return redirect('auth:login')

class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'auth/password_reset.html')

class DashboardView(LoginRequiredMixin, View):
    login_url = 'auth:login'
    def get(self, request):
        return render(request, 'auth/dashboard.html')

class StudentFilesView(LoginRequiredMixin, View):
    login_url = 'auth:login'
    programmes = Programme.objects.all()
    dept = None
    def check_department(self, dept_id, request):
        try:
            self.dept = Department.objects.get(pk=dept_id)
        except ObjectDoesNotExist:
            if request.method == 'POST':
                messages.error(request, 'error uploading files, department not found!')
            else:
                messages.error(request, 'error locating department')
        except ValidationError:
            if request.method == 'POST':
                messages.error(request, 'error uploading files, department not found!')
            else:
                messages.error(request, 'error locating department')

    def get(self, request, dept_id):
        form = FilesForm()
        self.check_department(dept_id, request)
        if self.dept != None:
            return render(request, 'auth/student_files.html', context={'programmes':self.programmes, 'dept':self.dept , 'form':form})
        else:
            return redirect('auth:list_department')

    def post(self, request, dept_id):
        form = FilesForm(request.POST, request.FILES, dept_id=dept_id)
        self.check_department(dept_id, request)
        if self.dept != None:
            if form.is_valid():
                data = form.save(commit=False)
                data.dept = self.dept
                data.save()
                messages.success(request, 'Student File has been added!')
                return redirect('auth:files_stud', self.dept.dept_id)
            messages.error(request, f'{form.errors.as_text()}')
            return render(request, 'auth/student_files.html', context={'programmes':self.programmes, 'dept':self.dept , 'form':form})
        else:
            return redirect('auth:list_department')

class DisplayForm(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request):
        form = FilesForm()
        return render(request, 'partials/files/stud_file_form.html', context={'form':form})

# DELETE FILES START ---------------
class DeleteStudentFilesView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request, pk):
        try:
            file = Files.objects.get(pk=pk)
            return render(request, 'partials/files/delete_modal.html', context={'file':file})
        except:
            messages.error(request, 'File not found!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})

    def post(self, request, pk):
        try:
            file = Files.objects.get(pk=pk)
            file.delete()
            messages.success(request, 'Student File has been deleted!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})
        except:
            messages.error(request, 'Failed to delete File!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})

class DeleteSupervisorFilesView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request, pk):
        try:
            file = SupervisorsFiles.objects.get(pk=pk)
            return render(request, 'partials/files/delete_super_files_modal.html', context={'file':file})
        except:
            messages.error(request, 'File not found!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})

    def post(self, request, pk):
        try:
            file = SupervisorsFiles.objects.get(pk=pk)
            file.delete()
            messages.success(request, 'Supervisors File has been deleted!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})
        except:
            messages.error(request, 'Failed to delete File!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})
# END DELETE FILES ---------------

class ListFilesView(LoginRequiredMixin, ListView):
    login_url = 'auth:login'
    template_name = "partials/files/list_files.html"

    def get_queryset(self):
        return Files.objects.filter(programme=self.kwargs['programme_id'], dept=self.kwargs['dept_id']).order_by('-pk')

class ListSupervisorFilesView(LoginRequiredMixin, ListView):
    login_url = 'auth:login'
    template_name = "partials/files/list_super.html"

    def get_queryset(self):
        return SupervisorsFiles.objects.filter(dept=self.kwargs['dept_id']).order_by('-pk')

class SupervisorFilesView(View):
    dept = None
    def check_department(self, dept_id, request):
        dept = None
        try:
            self.dept = Department.objects.get(pk=dept_id)
        except ObjectDoesNotExist:
            if request.method == 'POST':
                messages.error(request, 'error uploading files, department not found!')
            else:
                messages.error(request, 'error locating department')
        except ValidationError:
            if request.method == 'POST':
                messages.error(request, 'error uploading files, department not found!')
            else:
                messages.error(request, 'error locating department')

    def get(self, request, dept_id):
        self.check_department(dept_id, request)
        if self.dept != None:
            return render(request, 'auth/supervisor_files.html', context={'dept':self.dept, 'form':SuperFilesForm()})
        return render(request, 'auth/supervisor_files.html')

    def post(self, request, dept_id):
        form = SuperFilesForm(request.POST, request.FILES, dept_id=dept_id)
        self.check_department(dept_id, request)
        if self.dept != None:
            if form.is_valid():
                data = form.save(commit=False)
                data.dept = self.dept
                data.save()
                messages.success(request, 'Supervisors File has been added!')
                return redirect('auth:files_super', self.dept.dept_id)

            messages.error(request, f'{form.errors.as_text()}')
            return render(request, 'auth/supervisor_files.html', context={'dept':self.dept, 'form':form})
        else:
            return redirect('auth:list_department')

# MANAGE USERS START -------------------
class ManageStudentsView(StudentFilesView):
    form1 = UserForm()
    form2 = StudentProfileForm()
    form3 = MultipleStudentForm()
    programmes = Programme.objects.all()

    def get(self, request, dept_id):
        try:
            dept = Department.objects.get(dept_id=dept_id)
            return render(request, 'auth/manage_students.html', context={'dept':dept, 'programmes':self.programmes, 'form1':self.form1, 'form2':self.form2, 'form3':self.form3})

        except ObjectDoesNotExist:
            messages.error(request, 'Error Retrieving department!')
        except ValidationError:
            messages.error(request, 'Error Retrieving department!')
        return redirect('auth:list_department')

    def post(self, request, dept_id):
        form1 = UserForm(request.POST)
        form2 = StudentProfileForm(request.POST)

        try:
            dept = Department.objects.get(dept_id=dept_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Error Retrieving department!')
            return redirect('auth:list_department')
        else:
            if 'single' in request.POST:
                if form1.is_valid() and form2.is_valid():
                    user = form1.save(commit=False)
                    user.password = make_password(PASSWORD)
                    user_form = form2.save(commit=False)
                    user_form.user_id = user
                    user_form.dept_id = dept
                    user_form.programme_id = Programme.objects.get(id=request.POST['programme'])
                    user_form.session_id = Session.objects.get(id=request.POST['session'])
                    user_form.type_id = StudentType.objects.get(id=request.POST['student_type'])

                    user.save()
                    user_form.save()
                    messages.success(request, 'Account Created Successfully!')
                    return redirect('auth:manage_students', dept_id)

                messages.error(request, 'Error Creating Account Check form for more details!')
                return render(request, 'auth/manage_students.html', context={'dept':dept, 'programmes':self.programmes, 'form1':form1, 'form2':form2})

            elif 'multiple' in request.POST:
                form3 = MultipleStudentForm(request.POST,request.FILES)

                if form3.is_valid():
                    data = form3.cleaned_data
                    with open(str(request.FILES['file']), 'r') as file:
                        csv_obj = csv.reader(file)
                        next(csv_obj)

                        objs = []
                        sub_objs = []

                        prog_id = Programme.objects.get(programme_title=data['programme'])
                        session_id = Session.objects.get(session_title=data['session'])
                        type_id = StudentType.objects.get(type_title=data['student_type'])
                        dept = Department.objects.get(dept_id=dept_id)

                        for row in csv_obj:
                            objs.append(User(username=row[0], firstname=row[1], lastname=row[2], password=make_password(PASSWORD)))
                        created_users = User.objects.bulk_create(objs)

                        for user in created_users:
                            sub_objs.append(StudentProfile(user_id=user, programme_id=prog_id, session_id=session_id, dept_id=dept, type_id=type_id))
                        created_user_profiles = StudentProfile.objects.bulk_create(sub_objs)

                    messages.success(request, 'Account Created Successfully!')
                    return redirect('auth:manage_students', dept_id)

            messages.error(request, 'Error Creating Account from file Check form for more details!')
            return render(request, 'auth/manage_students.html', context={'dept':dept, 'programmes':self.programmes, 'form1':form1, 'form2':form2, 'form3':form3})

class DeleteUserAccountView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            return render(request, 'partials/files/delete_acct.html', context={'user':user})
        except:
            messages.error(request, 'Failed to delete Account!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})

    def post(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            user.delete()
            messages.success(request, 'Account has been deleted!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})
        except:
            messages.error(request, 'Failed to delete Account!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})

class ManageSupervisorsView(View):
    form1 = UserForm()
    form2 = SupervisorProfileForm()
    form3 = MultipleSuperForm()

    def get(self, request, dept_id):
        try:
            dept = Department.objects.get(dept_id=dept_id)
            return render(request, 'auth/manage_supervisors.html', context={'dept':dept, 'form1':self.form1, 'form2':self.form2, 'form3':self.form3})
        except ObjectDoesNotExist:
            messages.error(request, 'Error Retrieving department!')
        except ValidationError:
            messages.error(request, 'Error Retrieving department!')
        return redirect('auth:list_department')

    def post(self, request, dept_id):
        form1 = UserForm(request.POST)
        form2 = SupervisorProfileForm(request.POST)

        try:
            dept = Department.objects.get(dept_id=dept_id)
        except ObjectDoesNotExist:
            messages.error(request, 'Error Retrieving department!')
            return redirect('auth:list_department')
        else:
            if 'single' in request.POST:
                if form1.is_valid() and form2.is_valid():
                    user = form1.save(commit=False)
                    user.password = make_password(PASSWORD)
                    user_form = form2.save(commit=False)
                    user_form.user_id = user
                    user_form.dept_id = dept

                    user.save()
                    user_form.save()
                    messages.success(request, 'Account Created Successfully!')
                    return redirect('auth:manage_supervisors', dept_id)

                messages.error(request, 'Error Creating Account Check form for more details!')
                return render(request, 'auth/manage_supervisors.html', context={'dept':dept, 'form1':form1, 'form2':form2})

            elif 'multiple' in request.POST:
                form3 = MultipleSuperForm(request.POST,request.FILES)

                if form3.is_valid():
                    data = form3.cleaned_data

                    with open(str(request.FILES['file']), 'r') as file:
                        csv_obj = csv.reader(file)
                        next(csv_obj)

                        objs = []
                        sub_objs = []
                        super_levels = []

                        dept = Department.objects.get(dept_id=dept_id)

                        for row in csv_obj:
                            objs.append(User(username=row[0], firstname=row[1], lastname=row[2], password=make_password(PASSWORD)))
                            super_levels.append(row[3])

                        created_users = User.objects.bulk_create(objs)

                        for (user, level) in zip(created_users, super_levels):
                            rank_id = SupervisorRank.objects.get(rank_number=level)
                            sub_objs.append(SupervisorProfile(user_id=user, dept_id=dept, rank_id=rank_id))
                        created_user_profiles = SupervisorProfile.objects.bulk_create(sub_objs)

                        messages.success(request, 'Account Created Successfully!')
                        return redirect('auth:manage_supervisors', dept_id)

            messages.error(request, 'Error Creating Account from file Check form for more details!')
            return render(request, 'auth/manage_supervisors.html', context={'dept':dept, 'form1':form1, 'form2':form2, 'form3':form3})

class ManageAdministratorsView(View):
    def get(self, request):
        return render(request, 'auth/manage_administrators.html')

class ManageProfileView(View):
    def get(self, request):
        return render(request, 'auth/manage_profile.html')

class SettingsView(View):
    def get(self, request):
        return render(request, 'auth/settings.html')

# NOTIFICATIONS
class NotificationsView(View):
    def get(self, request):
        return render(request, 'auth/notifications.html')

# HELP VIEW
class HelpView(View):
    def get(self, request):
        return render(request, 'auth/help.html')

class ListDepartmentView(ListView):
    login_url = 'auth:login'
    model = Department
    template_name = 'auth/list_department.html'

class DepartmentView(View):
    def get(self, request, dept_id):
        try:
            dept = Department.objects.get(dept_id=dept_id)
            return render(request, 'auth/department/department.html', context={'dept':dept})
        except ObjectDoesNotExist:
            messages.error(request, 'Error Retrieving department!')
        except ValidationError:
            messages.error(request, 'Error Retrieving department!')
        return redirect('auth:list_department')

class WhatFileView(View):
    def get(self, request, dept_id):
        try:
            dept = Department.objects.get(dept_id=dept_id)
            return render(request, 'auth/department/whatfile.html', context={'dept':dept})
        except ObjectDoesNotExist:
            messages.error(request, 'Error Retrieving department!')
        except ValidationError:
            messages.error(request, 'Error Retrieving department!')
        return redirect('auth:list_department')

class BatchCreateView(View):
    def post(self, request, dept_id, file_id):
        try:
            if 'super' in request.POST:
                et_file = SupervisorsFiles.objects.get(id=file_id)

            if 'student' in request.POST:
                et_file = Files.objects.get(id=file_id)
                prog_id = Programme.objects.get(id=et_file.programme_id)
                sess_id = Session.objects.get(id=et_file.session_id)
                type_id = StudentType.objects.get(type_title=et_file.student_type)

            dept = Department.objects.get(dept_id=et_file.dept_id)

            path = f'{settings.BASE_DIR}{staticfiles_storage.url(str(et_file.file))}'
            with open(path, 'r') as file:
                csv_obj = csv.reader(file)
                next(csv_obj)
                objs = []
                sub_objs = []
                super_levels = []
                for row in csv_obj:
                    objs.append(User(username=row[0], firstname=row[1], lastname=row[2], password=make_password(PASSWORD)))
                    if 'super' in request.POST:
                        super_levels.append(row[3])

                created_users = User.objects.bulk_create(objs)

                if 'student' in request.POST:
                    for user in created_users:
                        sub_objs.append(StudentProfile(user_id=user, programme_id=prog_id, session_id=sess_id, dept_id=dept, type_id=type_id))
                    created_user_profiles = StudentProfile.objects.bulk_create(sub_objs)

                if 'super' in request.POST:
                    for (user, level) in zip(created_users, super_levels):
                        rank_id = SupervisorRank.objects.get(rank_number=level)
                        sub_objs.append(SupervisorProfile(user_id=user, dept_id=dept, rank_id=rank_id))
                    created_user_profiles = SupervisorProfile.objects.bulk_create(sub_objs)

            et_file.used = True
            et_file.save()

        except ObjectDoesNotExist:
            messages.error(request, 'Error bulk creating from File!')
        except ValidationError:
            messages.error(request, 'Error bulk creating from File!')
        except IntegrityError:
            messages.error(request, 'Error bulk creating from File!, Duplicate record found!')

        messages.success(request, 'Account has been created successfully!')
        if 'student' in request.POST:
            return redirect('auth:files_stud', dept_id)

        if 'super' in request.POST:
            return redirect('auth:files_super', dept_id)

class ListStudentView(LoginRequiredMixin, ListView):
    login_url = 'auth:login'
    template_name = "partials/files/list_student.html"

    def get_context_data(self, **kwargs):
        context = super(ListStudentView, self).get_context_data(**kwargs)
        context['programme'] = Programme.objects.all()
        return context

    def get_queryset(self):
        return StudentProfile.objects.filter(programme_id=self.kwargs['programme_id'], dept_id=self.kwargs['dept_id']).order_by('-pk')

class ListSupervisorView(LoginRequiredMixin, ListView):
    login_url = 'auth:login'
    template_name = "partials/files/list_supervisors.html"

    def get_queryset(self):
        return SupervisorProfile.objects.filter(dept_id=self.kwargs['dept_id']).order_by('-pk')

class ManageCoordinatorsView(View):
    programmes = Programme.objects.all()
    def get(self, request, dept_id):
        try:
            dept = Department.objects.get(dept_id=dept_id)
            coordinators = Coordinators.objects.filter(dept_id=dept_id)
            form = CoordinatorsForm(dept)
            return render(request, 'auth/manage_coordinators.html', context={"dept": dept, 'form':form, 'programmes':self.programmes, 'coordinators':coordinators})
        except ObjectDoesNotExist:
            return redirect('auth:list_department')

    def post(self, request, dept_id):
        coordinators = Coordinators.objects.filter(dept_id=dept_id)
        try:
            dept = Department.objects.get(dept_id=dept_id)
            form = CoordinatorsForm(dept, request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.dept_id = dept

                # FROM FORM
                form_chief_coord = form.cleaned_data['chief_coord_id']
                form_asst_coord = form.cleaned_data['asst_coord_id']
                form_prog = data.prog_id

                try:
                    coord = Coordinators.objects.get(prog_id=form_prog)
                    if form_chief_coord:
                        coord.chief_coord_id = form_chief_coord

                    if form_asst_coord:
                        coord.asst_coord_id = form_asst_coord
                    coord.save()
                    messages.success(request, f'{form_prog} Coordinators has been updated!!')
                    return redirect('auth:manage_coordinators', dept_id)

                except ObjectDoesNotExist:

                    for content in form.cleaned_data:
                        if form.cleaned_data[content] == None:
                            messages.warning(request, 'All fields are required!!')
                            return render(request, 'auth/manage_coordinators.html', context={"dept": dept, 'form':form, 'programmes':self.programmes, 'coordinators':coordinators})

                    messages.success(request, f'Coordinators has been registered!!')
                    data.save()
                return redirect('auth:manage_coordinators', dept_id)

            messages.error(request, f'Error processing form!!')
            return render(request, 'auth/manage_coordinators.html', context={"dept": dept, 'form':form, 'programmes':self.programmes, 'coordinators':coordinators})

        except ObjectDoesNotExist:
            return redirect('auth:list_department')

# Allocate
class AllocateView(View):
    def get(self, request):
        return render(request, 'auth/allocate.html')