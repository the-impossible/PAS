# My Django imports
from django.shortcuts import render, redirect, reverse
from django.views import View
from django.core.files.storage import default_storage
import csv, io, codecs, random, os
from pprint import pprint
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
from django.utils.decorators import method_decorator
#Email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from PAS_auth.utils import EmailThread, email_activation_token, Email
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

# My App imports
from PAS_app.models import (
    Files,
    Programme,
    Department,
    Session,
    SupervisorsFiles,
    StudentType,
    SupervisorRank,
    Title,
)
from PAS_auth.models import (
    User,
    Allocate,
    StudentProfile,
    SupervisorProfile,
    Coordinators,
    Groups,
    EmailSendCount,
)
from PAS_app.form import (
    FilesForm,
    SuperFilesForm,
    SupervisorProfileForm,
    StudentProfileForm,
    MultipleStudentForm,
    MultipleSuperForm,
    CoordinatorsForm,
    AllocationForm,
    MAllocationForm,
    RAllocationForm,
    DepartmentForm,
)
from PAS_auth.form import (
    UserForm,
    UpdateProfileForm,
)

from PAS_auth.decorator import *

PASSWORD = '12345678'
SPLIT = 6
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
    @method_decorator(only_authenticated_users)
    def post(self, request):
        logout(request)
        messages.success(request, 'You are successfully logged out, to continue login again')
        return redirect('auth:login')
class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'auth/password_reset.html')

    def post(self, request):
        email = request.POST.get('email').lower()
        if email:
            user = User.objects.filter(email=email)
            if user.exists():
                current_site = get_current_site(request).domain
                data = user[0]
                user_details = {
                    'fullname':data.get_fullname(),
                    'email': data.email,
                    'domain':current_site,
                    'uid': urlsafe_base64_encode(force_bytes(data.user_id)),
                    'token': email_activation_token.make_token(data),
                }
                Email.send(user_details, 'reset')
                messages.success(request, 'A mail has been sent to your mailbox to enable you reset your password!')
            else:
                messages.error(request, "Email address doesn't exist!")
        return render(request, 'auth/password_reset.html')
class ResetPasswordActivationView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        user_id = force_str(force_bytes(urlsafe_base64_decode(uidb64)))
        try:
            user = User.objects.get(user_id=user_id)
            if email_activation_token.check_token(user, token):
                messages.info(request, 'Create a password for your account!')
                return render(request, 'auth/complete_password_reset.html', context)
            else:
                messages.info(request, 'Link broken or Invalid reset link, Please Request a new one!')
                return redirect('auth:reset_password')

        except User.DoesNotExist:
            messages.error(request, 'Oops User not found, hence password cannot be changed, kindly request for a new link!')
            return redirect('auth:reset_password')

    def post(self, request, uidb64, token):
        user_id = force_str(force_bytes(urlsafe_base64_decode(uidb64)).decode())
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user = User.objects.get(user_id=user_id)
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if(password1 != password2):
                messages.error(request, 'Password don\'t match!')
                return render(request, 'auth/complete_password_reset.html', context)

            if(len(password1) < 6):
                messages.error(request, 'Password too short!')
                return render(request, 'auth/complete_password_reset.html', context)

            user.set_password(password1)
            user.save()
            messages.success(request, 'Password Changed you can now login with new password')

            return redirect('auth:login')

        except User.DoesNotExist:
            messages.error(request, 'Oops user does not exist!')
            return redirect('auth:reset_password')
class DashboardView(LoginRequiredMixin, View):
    login_url = 'auth:login'
    @method_decorator(has_updated)
    def get(self, request):
        return render(request, 'auth/dashboard.html')

@method_decorator(is_staff, name="get")
@method_decorator(is_staff, name='post')
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
        form = FilesForm(data=request.POST, files=request.FILES, dept_id=dept_id)

        self.check_department(dept_id, request)
        if self.dept != None:
            if form.is_valid():
                data = form.save(commit=False)
                data.dept = self.dept
                data.file = request.FILES['file']
                data.save()
                messages.success(request, 'Student File has been added!')
                return redirect('auth:files_stud', self.dept.dept_id)
            messages.error(request, f'{form.errors.as_text()}')
            return render(request, 'auth/student_files.html', context={'programmes':self.programmes, 'dept':self.dept , 'form':form})
        else:
            return redirect('auth:list_department')

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

@method_decorator(is_staff, name="get")
@method_decorator(is_staff, name='post')
class SupervisorFilesView(LoginRequiredMixin, View):
    login_url = 'auth:login'

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
                data.file = request.FILES['file']
                data.dept = self.dept
                data.prog = Programme.objects.get(programme_title=form.cleaned_data['prog'])
                data.save()
                messages.success(request, 'Supervisors File has been added!')
                return redirect('auth:files_super', self.dept.dept_id)

            messages.error(request, f'{form.errors.as_text()}')
            return render(request, 'auth/supervisor_files.html', context={'dept':self.dept, 'form':form})
        else:
            return redirect('auth:list_department')

@method_decorator(is_staff, name="get")
@method_decorator(is_staff, name='post')
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

                    csv_obj = csv.reader(codecs.iterdecode(request.FILES['file'], 'utf-8'))
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

@method_decorator(is_staff, name="get")
@method_decorator(is_staff, name='post')
class ManageSupervisorsView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    form1 = UserForm()
    form2 = SupervisorProfileForm()
    form3 = MultipleSuperForm()

    def get(self, request, dept_id):
        try:
            dept = Department.objects.get(dept_id=dept_id)
            object_list = SupervisorProfile.objects.filter(dept_id=dept_id).order_by('-pk')
            return render(request, 'auth/manage_supervisors.html', context={'dept':dept, 'form1':self.form1, 'form2':self.form2, 'form3':self.form3, 'object_list':object_list})
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

                    user.is_super = True
                    user.save()
                    user_form.save()
                    messages.success(request, 'Account Created Successfully!')
                    return redirect('auth:manage_supervisors', dept_id)

                messages.error(request, 'Error Creating Account Check form for more details!')
                return render(request, 'auth/manage_supervisors.html', context={'dept':dept, 'form1':form1, 'form2':form2})

            elif 'multiple' in request.POST:
                form3 = MultipleSuperForm(request.POST,request.FILES)

                if form3.is_valid():
                    file = request.FILES['file']
                    prog_id = Programme.objects.get(programme_title=form3.cleaned_data['prog'])

                    csv_obj = csv.reader(codecs.iterdecode(file, 'utf-8'))
                    next(csv_obj)

                    objs = []
                    sub_objs = []
                    super_levels = []
                    super_titles = []
                    super_rg_capacity = []
                    super_ev_capacity = []
                    super_nd = []

                    dept = Department.objects.get(dept_id=dept_id)
                    for row in csv_obj:
                        objs.append(User(username=row[0], name=row[2], password=make_password(PASSWORD), is_super=True))
                        super_levels.append(row[3])
                        super_titles.append(row[1])
                        super_rg_capacity.append(row[4])
                        super_ev_capacity.append(row[5])
                        super_nd.append(row[6])

                    created_users = User.objects.bulk_create(objs)

                    for (user, level, title, rg_capacity, ev_capacity, super_nd) in zip(created_users, super_levels, super_titles, super_rg_capacity, super_ev_capacity, super_nd):
                        rank_id = SupervisorRank.objects.get(rank_number=level)
                        title = Title.objects.get(title_number=title)
                        can_super = False
                        if super_nd == '1':
                            can_super = True
                        sub_objs.append(SupervisorProfile(user_id=user, dept_id=dept, rank_id=rank_id, prog_id=prog_id, title=title, RG_capacity=rg_capacity, Ev_capacity=ev_capacity, super_nd=can_super))
                    created_user_profiles = SupervisorProfile.objects.bulk_create(sub_objs)

                    messages.success(request, 'Account Created Successfully!')
                    return redirect('auth:manage_supervisors', dept_id)

            messages.error(request, 'Error Creating Account from file Check form for more details!')
            return render(request, 'auth/manage_supervisors.html', context={'dept':dept, 'form1':form1, 'form2':form2, 'form3':form3})

class ManageAdministratorsView(View):
    def get(self, request):
        return render(request, 'auth/manage_administrators.html')
class ManageProfileView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            form = UpdateProfileForm(instance=user)
            return render(request, 'auth/manage_profile.html', context={'info':user, 'form':form})
        except ObjectDoesNotExist:
            return redirect('auth:dashboard')

    def post(self, request, user_id):
        try:
            user = User.objects.get(user_id=user_id)
            form = UpdateProfileForm(request.POST, request.FILES, instance=user)

            old_email = user.email

            if 'profile' in request.POST:
                if form.is_valid():
                    user = form.save(commit=False)

                    #Retrieve user details
                    email = user.email
                    fullname = user.get_fullname()

                    # Send an email if old email is not same as new email
                    # if email != old_email:
                    #     user.is_verified = False

                    #     count, created = EmailSendCount.objects.get_or_create(user=user)
                    #     count.resetCount
                    #     count.save()

                    #     current_site = get_current_site(request).domain
                    #     user_details = {
                    #         'fullname':fullname,
                    #         'email': email,
                    #         'domain':current_site,
                    #         'uid': urlsafe_base64_encode(force_bytes(user.user_id)),
                    #         'token': email_activation_token.make_token(user),
                    #     }
                    #     user.save()

                    #     messages.success(request, 'Profile updated!')
                    #     # return redirect('auth:resend_email')0
                    # else:
                    user.is_verified = True
                    user.save()
                    messages.success(request, 'Profile updated!')

                    return redirect('auth:manage_profile', user.user_id)
                messages.error(request, 'Error updating profile')

            if 'changeP' in request.POST:
                password1 = request.POST.get('password1')
                password2 = request.POST.get('password2')

                if password1 and password2:
                    if password1 == password2:
                        if len(password1) >= 6:
                            user.password = make_password(password1)
                            messages.success(request, 'Password has been updated successfully! You have to re-login to continue')
                            user.save()
                            return redirect('auth:logout')
                        else:
                            messages.error(request, 'Passwords should not be less than 6 characters!')
                    else:
                        messages.error(request, 'Passwords do not match!')
                else:
                    messages.error(request, 'All fields are required!')

            return render(request, 'auth/manage_profile.html', context={'info':user, 'form':form})
        except ObjectDoesNotExist:
            return redirect('auth:manage_profile', user.user_id)
class SettingsView(View):
    def get(self, request):
        return render(request, 'auth/settings.html')
class NotificationsView(View):
    def get(self, request):
        return render(request, 'auth/notifications.html')
class HelpView(View):
    def get(self, request):
        return render(request, 'auth/help.html')
class ReVerifyEmailView(View):
    def get(self, request):
        try:
            user = User.objects.get(user_id=request.user.user_id)
            email = user.email
            return render(request, 'auth/reverify_email.html', context={'email':email})
        except ObjectDoesNotExist:
            return redirect('auth:manage_profile', request.user.user_id)
class ResendEmailVerificationView(View):
    def get(self, request):
        try:
            user = User.objects.get(user_id=request.user.user_id)
            count, created = EmailSendCount.objects.get_or_create(user=user)
            count.increaseCount
            count.save()

            if count.getCount >= 9:
                messages.warning(request, (f'Email address cannot be Verified, verification has exceeded it limit'))
                return render(request, 'auth/reverify_email.html', {'email':user.email, 'check':'check'})

            else:
                # send verification email
                current_site = get_current_site(request).domain

                user_details = {
                    'fullname':user.get_fullname(),
                    'email': user.email,
                    'domain':current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.user_id)),
                    'token': email_activation_token.make_token(user),
                }

                Email.send(user_details, 'verify')
                messages.success(request, 'Email 📧 has been sent to your mailbox 📫, kindly verify')

                context = {
                    'email':user.email,
                }
                return render(request, 'auth/reverify_email.html', context)
        except:
            messages.error(request, 'User not found')
            context = {
                'email':request.user.email,
            }
            return render(request, 'auth/reverify_email.html', context)
class EmailActivationView(View):
    def get(self, request, uidb64, token):
        user_id = force_str(force_bytes(urlsafe_base64_decode(uidb64)))

        try:
            user = User.objects.get(user_id=user_id)

            if user.is_verified:
                messages.warning(request, 'Your email has already been verified!')
                return redirect('auth:dashboard')

            if email_activation_token.check_token(user, token):
                user.is_verified = True
                user.save()

                # Reset EmailCount
                count, created = EmailSendCount.objects.get_or_create(user=user)
                count.resetCount
                count.save()

                messages.success(request, 'Email activated successfully')
                return redirect('auth:manage_profile', request.user.user_id)
            else:
                messages.info(request, 'Email not verified, Link broken or Invalid reset link, Please Request a new one')
                return redirect('auth:reverify_email')

        except User.DoesNotExist:
            messages.warning(request, 'Oops User not found, hence email not verified!')
            return redirect('auth:manage_profile', request.user.user_id)

@method_decorator(is_staff, name="get")
@method_decorator(is_staff, name='post')
class ListDepartmentView(LoginRequiredMixin, View):
    login_url = 'auth:login'
    form = DepartmentForm()
    def get(self, request):
        dept = Department.objects.all()
        return render(request, 'auth/list_department.html', context={'dept':dept, 'form':self.form})

    def post(self, request):
        form = DepartmentForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Department has been created!')
            return redirect('auth:list_department')

        messages.error(request, 'Error creating Department!')
        dept = Department.objects.all()

        return render(request, 'auth/list_department.html', context={'dept':dept, 'form':form})

@method_decorator(is_staff, name='get')
class DepartmentView(LoginRequiredMixin, View):
    login_url = 'auth:login'
    def get(self, request, dept_id):
        try:
            dept = Department.objects.get(dept_id=dept_id)
            return render(request, 'auth/department/department.html', context={'dept':dept})
        except ObjectDoesNotExist:
            messages.error(request, 'Error Retrieving department!')
        except ValidationError:
            messages.error(request, 'Error Retrieving department!')
        return redirect('auth:list_department')

@method_decorator(is_staff, name="get")
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

@method_decorator(is_staff, name="post")
class BatchCreateView(View):
    def post(self, request, dept_id, file_id):
        try:
            if 'super' in request.POST:
                et_file = SupervisorsFiles.objects.get(id=file_id)
                prog_id = Programme.objects.get(id=et_file.prog.id)

            if 'student' in request.POST:
                et_file = Files.objects.get(id=file_id)

                prog_id = Programme.objects.get(id=et_file.programme_id)
                sess_id = Session.objects.get(id=et_file.session_id)
                type_id = StudentType.objects.get(type_title=et_file.student_type)

            dept = Department.objects.get(dept_id=et_file.dept_id)

            file = default_storage.open(f'{et_file}', mode='r')
            data = file.readlines()
            file.close()

            csv_obj = csv.reader(data)
            next(csv_obj)

            objs = []
            sub_objs = []
            super_levels = []
            super_titles = []
            super_rg_capacity = []
            super_ev_capacity = []
            super_nd = []

            for row in csv_obj:

                if 'super' in request.POST:
                    objs.append(User(username=row[0], name=row[2], password=make_password(PASSWORD), is_super=True))
                    super_levels.append(row[3])
                    super_titles.append(row[1])
                    super_rg_capacity.append(row[4])
                    super_ev_capacity.append(row[5])
                    super_nd.append(row[6])

                if 'student' in request.POST:
                    objs.append(User(username=row[0], name=row[1], password=make_password(PASSWORD)))

            created_users = User.objects.bulk_create(objs)

            if 'student' in request.POST:
                for user in created_users:
                    sub_objs.append(StudentProfile(user_id=user, programme_id=prog_id, session_id=sess_id, dept_id=dept, type_id=type_id))
                created_user_profiles = StudentProfile.objects.bulk_create(sub_objs)

            if 'super' in request.POST:
                for (user, level, title, rg_capacity, ev_capacity, super_nd) in zip(created_users, super_levels, super_titles, super_rg_capacity, super_ev_capacity, super_nd):
                    rank_id = SupervisorRank.objects.get(rank_number=level)
                    title = Title.objects.get(title_number=title)
                    can_super = False
                    if super_nd == '1':
                        can_super = True
                    sub_objs.append(SupervisorProfile(user_id=user, dept_id=dept, rank_id=rank_id, prog_id=prog_id, title=title, RG_capacity=rg_capacity, Ev_capacity=ev_capacity, super_nd=can_super))
                created_user_profiles = SupervisorProfile.objects.bulk_create(sub_objs)

            et_file.used = True
            et_file.save()

        except ObjectDoesNotExist:
            messages.error(request, 'Error bulk creating from File!')
        except ValidationError:
            messages.error(request, 'Error bulk creating from File!')
        except IntegrityError:
            messages.error(request, 'Error bulk creating from File!, Duplicate record found!')
        else:
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

@method_decorator(is_staff, name="get")
@method_decorator(is_staff, name='post')
class ManageCoordinatorsView(LoginRequiredMixin, View):
    login_url = 'auth:login'

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

                coordinators = Coordinators.objects.filter(dept_id=dept_id, prog_id=form_prog)
                if coordinators:
                    coordinators = coordinators[0]

                    existing_coordinator_hnd = Coordinators.objects.filter(dept_id=dept_id, prog_id=Programme.objects.get(programme_title='HND'))
                    existing_coordinator_nd = Coordinators.objects.filter(dept_id=dept_id, prog_id=Programme.objects.get(programme_title='ND'))

                    if form_chief_coord:

                        if existing_coordinator_nd and existing_coordinator_hnd:
                            user = User.objects.get(username=coordinators.chief_coord_id.user_id)

                            if existing_coordinator_nd[0].chief_coord_id.user_id.username != existing_coordinator_hnd[0].chief_coord_id.user_id.username:
                                user.is_staff = False

                            user.save()

                            if existing_coordinator_nd[0].asst_coord_id.user_id.username != existing_coordinator_hnd[0].asst_coord_id.user_id.username:
                                user.is_staff = False
                            user.save()


                        coordinators.chief_coord_id = form_chief_coord
                        coordinators.asst_coord_id = form_asst_coord
                        coordinators.save()

                    user = User.objects.get(username=form_asst_coord.user_id)
                    user.is_staff = True
                    user.save()

                    user = User.objects.get(username=form_chief_coord.user_id)
                    user.is_staff = True
                    user.save()

                    messages.success(request, f'{form_prog} Coordinators has been updated!!')
                else:
                    for content in form.cleaned_data:
                        if form.cleaned_data[content] == None:
                            messages.warning(request, 'All fields are required!!')
                            return render(request, 'auth/manage_coordinators.html', context={"dept": dept, 'form':form, 'programmes':self.programmes, 'coordinators':coordinators})

                    user = User.objects.get(username=form_asst_coord.user_id)
                    user.is_staff = True
                    user.save()

                    user = User.objects.get(username=form_chief_coord.user_id)
                    user.is_staff = True
                    user.save()

                    messages.success(request, f'Coordinators has been registered!!')
                    data.save()
                return redirect('auth:manage_coordinators', dept_id)

            else:
                messages.error(request, f'Error processing form!!')
                return render(request, 'auth/manage_coordinators.html', context={"dept": dept, 'form':form, 'programmes':self.programmes, 'coordinators':coordinators})

        except ObjectDoesNotExist:
            return redirect('auth:list_department')

@method_decorator(is_staff, name="get")
@method_decorator(is_staff, name='post')
class AllocateView(View):
    form = AllocationForm()
    def get(self, request, dept_id):
        try:
            dept = Department.objects.get(dept_id=dept_id)
            form2 = MAllocationForm(dept_id=dept)
            return render(request, 'auth/allocate.html', context={"dept": dept, 'form':self.form, 'form2':form2})
        except ObjectDoesNotExist:
            return redirect('auth:list_department')

    def post(self, request, dept_id):
        try:
            dept = Department.objects.get(dept_id=dept_id)
            form2 = MAllocationForm(dept_id=dept)

            if 'authA' in request.POST:
                form = AllocationForm(request.POST)
                if form.is_valid():
                    prog_id = form.cleaned_data.get('prog_id')
                    sess_id = form.cleaned_data.get('sess_id')
                    type_id = form.cleaned_data.get('type_id')

                    stud_type = StudentType.objects.get(type_title='Evening')

                    # GET STUDENTS AND SUPERVISOR
                    match_studs = StudentProfile.objects.filter(programme_id=prog_id, session_id=sess_id, type_id=type_id)
                    if prog_id.programme_title == 'ND':
                        match_super = SupervisorProfile.objects.filter(dept_id=dept_id, super_nd=True)
                    else:
                        match_super = SupervisorProfile.objects.filter(dept_id=dept_id, prog_id=prog_id)

                    # DETERMINE IF ALLOCATION FOR THAT SESSION AND DEPT EXISTS
                    allocation_exists = Allocate.objects.filter(dept_id=dept, sess_id=sess_id, prog_id=prog_id, type_id=type_id).exists()

                    if not allocation_exists:
                        # ALLOCATION STARTS
                        allocation = {}
                        match_studs_list = list(match_studs)
                        match_super_list = list(match_super)

                        if match_studs and match_super:
                            # SETTING THE SIZE OF THE GROUP BASED ON THE LEVEL (ND|HND)
                            if prog_id.programme_title == 'ND':
                                size = round(len(match_studs)/SPLIT)
                                if size * SPLIT < len(match_studs):
                                    size += 1

                                # GENERATE THE GROUPS
                                groups = [Groups.objects.get(group_num=f"Group {i}") for i in range(1, size + 1)]

                                count = 0
                                flag = False #To detect if student was assigned successfully

                                # FOR ND STUDENTS
                                if len(match_studs_list) >= SPLIT:

                                    # ASSIGN STUDENTS
                                    for i in range(len(groups)):
                                        temp_list = []

                                        while count < SPLIT:
                                            temp_list.append(match_studs_list.pop())
                                            count += 1

                                        allocation[groups[i]] = [temp_list]
                                        count = 0

                                        if len(match_studs_list) < SPLIT and len(match_studs_list) > 0:
                                            allocation[groups[i + 1]] = [match_studs_list]
                                            break

                                    flag = True

                                # ERROR MESSAGE
                                else:
                                    messages.error(request, f'You need at-least {SPLIT} students records before allocation can take place for ND student')
                                    return render(request, 'auth/allocate.html', context={"dept": dept, 'form':self.form, 'form2':form2})

                            else:
                                # GENERATE THE GROUPS
                                groups = [Groups.objects.get(group_num=f"Group {i}") for i in range(1, len(match_studs) + 1)]

                                # ASSIGN STUDENTS
                                for i in range(len(groups)):
                                    temp_list = []
                                    temp_list.append(match_studs_list.pop())
                                    allocation[groups[i]] = [temp_list]

                                flag = True

                            # ASSIGN LECTURES
                            index = 1
                            count = 0
                            if flag:
                                for i in range(1, len(groups)+ 1):

                                    if index <= len(match_super_list):
                                        allocation[groups[i - 1]].insert(0, match_super_list[index - 1])
                                    else:
                                        if prog_id.programme_title != 'ND': #For HND only where supervisor capacity matters
                                            count += 1
                                            for j in match_super_list:
                                                if stud_type == type_id:
                                                    if int(j.Ev_capacity) == count:
                                                        match_super_list.remove(j)
                                                else:
                                                    if int(j.RG_capacity) == count:
                                                        match_super_list.remove(j)
                                        index = 1
                                        allocation[groups[i - 1]].insert(0, match_super_list[index - 1])
                                    index += 1
                                objs = []

                                # PREPARE OBJECTS FOR BATCH CREATE
                                for (key, value) in allocation.items():
                                    for v in range(len(value[1])):
                                        objs.append(Allocate(super_id=value[0], group_id=key, type_id=type_id, stud_id=value[1][v], dept_id=dept, sess_id=sess_id, prog_id=prog_id))

                                # SAVE RECORD TO TABLE: -> ALLOCATE
                                allocations = Allocate.objects.bulk_create(objs)

                                groupings = ManageAllocationsView().retrieve(prog_id, sess_id, type_id)

                                messages.success(request, 'Student to supervisor allocation successful!')
                                return render(request, 'auth/allocate.html', context={"dept": dept, 'form':self.form, 'form2':form2, 't_students':len(match_studs), 't_super':len(match_super), 'groups':len(groups), 'groupings':groupings})
                            else:
                                messages.error(request, 'Something went wrong!')
                                return redirect('auth:allocate')
                        #ERROR
                        else:
                            if len(match_studs) == 0 and len(match_super) == 0:
                                messages.error(request, 'Students and Supervisors Records not found!, allocation aborted!')

                            elif len(match_studs) == 0:
                                messages.error(request, 'Students Records not found!, allocation aborted!')

                            elif len(match_super) == 0:
                                messages.error(request, 'Supervisors Records not found!, allocation aborted!')
                    else:
                        messages.error(request, 'Allocation already exist for the supplied information!,  try allocating manually')

                return render(request, 'auth/allocate.html', context={"dept": dept, 'form':self.form, 'form2':form2})

            if 'mAllocate' in request.POST:
                form2 = MAllocationForm(request.POST, dept_id=dept)

                groupings = []

                if form2.is_valid():
                    group_id = form2.cleaned_data.get('group_id')
                    sess_id = form2.cleaned_data.get('sess_id')
                    super_id = form2.cleaned_data.get('super_id')
                    stud_id = form2.cleaned_data.get('stud_id')

                    allocation_exists = Allocate.objects.filter(sess_id=sess_id, stud_id=stud_id).exists()

                    if allocation_exists:
                        messages.error(request, 'Allocation exist!, Attempt deleting current student allocation')
                    else:
                        user_id = User.objects.get(username=stud_id)
                        stud_type = StudentProfile.objects.get(user_id=user_id)

                        group_occupied = Allocate.objects.filter(group_id=group_id, prog_id=stud_type.programme_id)
                        if group_occupied:
                            if stud_type.programme_id.programme_title == 'ND':
                                if group_occupied and len(group_occupied) == 3:

                                    to_try = Allocate.objects.filter(sess_id=sess_id, prog_id=stud_type.programme_id, dept_id=dept_id).order_by('group_id').last()

                                    messages.warning(request, f'{group_id} is already filled up, try from above {to_try.group_id}')

                                    return render(request, 'auth/allocate.html', context={"dept": dept, 'form':self.form, 'form2':form2})
                                else:
                                    if group_occupied.first().super_id != super_id:

                                        messages.warning(request, f'{group_id} already contains a supervisor: {group_occupied.first().super_id} select the mentioned supervisor or try another group')

                                        return render(request, 'auth/allocate.html', context={"dept": dept, 'form':self.form, 'form2':form2})
                            else:
                                group_occupied = Allocate.objects.filter(group_id=group_id, prog_id=stud_type.programme_id)

                                if group_occupied:

                                    to_try = Allocate.objects.filter(sess_id=sess_id, prog_id=stud_type.programme_id, dept_id=dept_id).order_by('group_id').last()

                                    messages.warning(request, f'{group_id} is already filled up, try from above {to_try.group_id}')

                                    return render(request, 'auth/allocate.html', context={"dept": dept, 'form':self.form, 'form2':form2})

                        data = form2.save(commit=False)

                        data.prog_id = stud_type.programme_id
                        data.dept_id = stud_type.dept_id
                        data.type_id = stud_type.type_id

                        data.save()

                        groupings.append([data.group_id, [data.stud_id], data.super_id])

                        messages.success(request, f'{stud_id} has been allocated to group {group_id} Successfully')

            form2 = MAllocationForm(dept_id=dept)
            return render(request, 'auth/allocate.html', context={"dept": dept, 'form':self.form, 'form2':form2, 'grouping':groupings})

        except ObjectDoesNotExist:
            return redirect('auth:list_department')

@method_decorator(is_staff, name="get")
@method_decorator(is_staff, name='post')
class ManageAllocationsView(LoginRequiredMixin, View):
    login_url = 'auth:login'
    form = RAllocationForm()

    def get(self, request, dept_id):
        try:
            dept = Department.objects.get(dept_id=dept_id)
            return render(request, 'auth/manage_allocation.html', context={'dept':dept, 'form':self.form})
        except ObjectDoesNotExist:
            messages.error(request, 'Error Retrieving department!')
        except ValidationError:
            messages.error(request, 'Error Retrieving department!')
        return redirect('auth:list_department')

    def retrieve(self, prog_id, sess_id, type_id):
        allocations = Allocate.objects.filter(prog_id=prog_id, sess_id=sess_id, type_id=type_id).order_by('group_id')
        """
            [<SupervisorProfile: LEC12987: Mr.   MUHAMMAD HARUNA ISA>,
                <Groups: Group 51>,
                [<StudentProfile: CST20HND0788>,
                <StudentProfile: CST20HND0406>,
                <StudentProfile: CST20HND0156>,
                <StudentProfile: CST19HND48024>],
                UUID('e08a86ed-e6b3-4952-9320-2b218857db7f')
            ]
        """
        groupings = []
        for allocation in allocations:
            if not groupings:
                groupings.append([allocation.super_id, allocation.group_id, [allocation.stud_id], allocation.super_id.super_id])
            else:
                for mini in groupings:
                    if allocation.super_id in mini:
                        groupings[groupings.index(mini)][2].append(allocation.stud_id)
                        break
                else:
                    groupings.append([allocation.super_id, allocation.group_id, [allocation.stud_id], allocation.super_id.super_id])
        return groupings

    def post(self, request, dept_id):

        try:
            dept = Department.objects.get(dept_id=dept_id)

            if 'authR' in request.POST:

                form = RAllocationForm(request.POST)

                if form.is_valid():
                    prog_id = form.cleaned_data.get('prog_id')
                    sess_id = form.cleaned_data.get('sess_id')
                    type_id = form.cleaned_data.get('type_id')

                    groupings = self.retrieve(prog_id, sess_id, type_id)

                return render(request, 'auth/manage_allocation.html', context={'dept':dept, 'form':self.form, 'groupings':groupings, 'prog':prog_id, 'sess':sess_id, 'type':type_id})
            else:
                prog_id = Programme.objects.get(programme_title=request.POST.get('prog'))
                sess_id = Session.objects.get(session_title=request.POST.get('sess'))
                type_id = StudentType.objects.get(type_title=request.POST.get('type'))

                check_list = request.POST.getlist('to_delete')
                if check_list:
                    for item in check_list:
                        try:
                            Allocate.objects.filter(super_id=SupervisorProfile.objects.get(super_id=item), prog_id=prog_id, sess_id=sess_id, type_id=type_id).delete()

                        except ValidationError:
                            try:
                                Allocate.objects.filter(stud_id=StudentProfile.objects.get(user_id=User.objects.get(username=item))).delete()
                            except:
                                messages.warning(request, 'Failed deleting individual student allocations')
                                groupings = self.retrieve(prog_id, sess_id, type_id)
                                return render(request, 'auth/manage_allocation.html', context={'dept':dept, 'form':self.form, 'grouping':groupings, 'prog':prog_id, 'sess':sess_id})
                    groupings = self.retrieve(prog_id, sess_id, type_id)
                    messages.success(request, 'Successfully deleted the selected allocations')
                    return render(request, 'auth/manage_allocation.html', context={'dept':dept, 'form':self.form, 'groupings':groupings, 'prog':prog_id, 'sess':sess_id, 'type':type_id})

                messages.error(request, 'No allocation was selected, Try again!')
                return render(request, 'auth/manage_allocation.html', context={'dept':dept, 'form':self.form, 'prog':prog_id, 'sess':sess_id, 'type':type_id})

        except ObjectDoesNotExist:
            messages.error(request, 'Error Deleting!')
            return redirect('auth:manage_allocate', dept_id)
        except ValidationError:
            messages.error(request, 'Error Retrieving department!')
            return redirect('auth:list_department')

@method_decorator(has_updated, name="get")
class AssignedStudentView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    programmes = Programme.objects.all()
    categories = StudentType.objects.all()
    def get(self, request):
        try:
            super_id = SupervisorProfile.objects.get(user_id=request.user)
            group_nums = Allocate.objects.filter(super_id=super_id).values_list('group_id', flat=True).distinct()
            allocations_nd = [Groups.objects.get(id=i) for i in group_nums]
            allocations_hnd = Allocate.objects.filter(super_id=super_id, prog_id=Programme.objects.get(programme_title='HND'))
            return render(request, 'auth/assigned_students.html', context={'programmes':self.programmes, 'categories':self.categories, 'allocations_nd':allocations_nd, 'allocations_hnd':allocations_hnd})
        except SupervisorProfile.DoesNotExist:
            messages.success(request, 'Unable to get your account profile')
            return redirect('auth:dashboard')

@method_decorator(has_updated, name="get")
class AssignedSupervisorView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request):
        try:
            stud_id = StudentProfile.objects.get(user_id=request.user)
            allocation = Allocate.objects.get(stud_id=stud_id)
            group_members = Allocate.objects.filter(group_id=allocation.group_id, prog_id=stud_id.programme_id)
            return render(request, 'auth/assigned_supervisor.html', context={'allocation':allocation, 'stud':stud_id, 'group_members':group_members})

        except StudentProfile.DoesNotExist:
            messages.error(request, 'Unable to get your account profile')

        except Allocate.MultipleObjectsReturned:
            messages.error(request, 'Something went wrong')

        except Allocate.DoesNotExist:
            messages.info(request, 'You are yet to be allocated!')
        return redirect('auth:dashboard')

class DisplayGroupMembersView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request, group_id, prog_id, type_id):
        try:
            super_id = SupervisorProfile.objects.get(user_id=request.user) #GET the logged in staff
            #Filter all the groups by prog, group_id and type
            members = Allocate.objects.filter(super_id=super_id, prog_id=prog_id, type_id=type_id, group_id=group_id)

            return render(request, 'partials/group_members_modal.html', context={'members':members, 'group_id':group_id})
        except:
            messages.error(request, 'Unable to fetch group members')
            return HttpResponse(status=204)

class DisplayMembersView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request, prog_id, type_id):
        try:
            super_id = SupervisorProfile.objects.get(user_id=request.user) #GET the logged in staff

            #Filter all the groups by prog, group_id and type
            members = Allocate.objects.filter(super_id=super_id, prog_id=prog_id, type_id=type_id)
            return render(request, 'partials/group_members_modal.html', context={'members':members})
        except:
            messages.error(request, 'Unable to fetch group members')
            return HttpResponse(status=204)

class DisplayGroupsView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request, prog_id, type_id):
        try:
            super_id = SupervisorProfile.objects.get(user_id=request.user) #GET the logged in staff
            group_nums = Allocate.objects.filter(super_id=super_id, prog_id=prog_id, type_id=type_id).values_list('group_id', flat=True).distinct() #Filter all the groups by prog and type

            groups = [Groups.objects.get(id=i) for i in group_nums]
            prog_id = Programme.objects.get(id=prog_id)
            type_id = StudentType.objects.get(id=type_id)
            return render(request, 'partials/groups_modal.html', context={'groups':groups, 'prog_id':prog_id, 'type_id':type_id})

        except:
            messages.error(request, 'Unable to fetch group')
            return HttpResponse(status=204)

@method_decorator(has_updated, name="get")
class ViewProjectCoordinator(LoginRequiredMixin, View):
    login_url = 'auth:login'

    programmes = Programme.objects.all()
    def get(self, request):
        try:
            if request.user.is_super:
                user_id = SupervisorProfile.objects.get(user_id=request.user)
                coordinators = Coordinators.objects.filter(dept_id=user_id.dept_id)
            elif not request.user.is_staff:
                user_id = StudentProfile.objects.get(user_id=request.user)
                coordinators = Coordinators.objects.get(prog_id=user_id.programme_id, dept_id=user_id.dept_id)
            else:
                messages.info(request, 'You are not allowed to view that page')
                return redirect('auth:dashboard')

            return render(request, 'auth/view_project_coordinator.html', context={'coordinators':coordinators, 'stud':user_id, 'programmes':self.programmes})

        except StudentProfile.DoesNotExist:
            messages.info(request, 'Unable to get your account profile')
        except Coordinators.DoesNotExist:
            messages.info(request, 'Unable to get coordinator for your programme try again!')

        return redirect('auth:dashboard')

