# My Django imports
from django.shortcuts import render, redirect, reverse
from django.views import View
import csv
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse


# My App imports
from PAS_app.models import (
    Files,
    Programme,
    SupervisorsFiles,
)
from PAS_app.form import (
    FilesForm,
    SuperFilesForm,
)

# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username').strip().upper()
        password = request.POST.get('password').strip()

        if username and password:
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'You are now signed in {user}')
                    return redirect('auth:dashboard')
                else:
                    messages.warning(request, 'Account not active contact the administrator')
                    return redirect('auth:login')
            else:
                user = authenticate(request, email=username, password=password)
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

    def get(self, request):
        programmes = Programme.objects.all()
        return render(request, 'auth/student_files.html', context={'programmes':programmes})

    def post(self, request):
        form = FilesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student File has been added!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})
        return render(request, 'partials/files/stud_file_form.html', context={'form':form})

class UploadStudentFilesView(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request):
        form = FilesForm()
        return render(request, 'partials/files/stud_file_form.html', context={'form':form})

class UploadSupervisorFilesView(UploadStudentFilesView):
    def get(self, request):
        form = SuperFilesForm()
        return render(request, 'partials/files/super_file_form.html', context={'form':form})

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
        return Files.objects.filter(programme=self.kwargs['programme_id']).order_by('-pk')

class ListSupervisorFilesView(LoginRequiredMixin, ListView):
    login_url = 'auth:login'
    template_name = "partials/files/list_super.html"

    def get_queryset(self):
        return SupervisorsFiles.objects.all().order_by('-pk')

class SupervisorFilesView(View):
    def get(self, request):
        return render(request, 'auth/supervisor_files.html')

    def post(self, request):
        form = SuperFilesForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Supervisors File has been added!')
            return HttpResponse(status=204, headers={'Hx-Trigger':'listChanged'})
        return render(request, 'partials/files/super_file_form.html', context={'form':form})

class ManageStudentsView(StudentFilesView):
    def get(self, request):
        return render(request, 'auth/manage_students.html')

class ManageProfile(View):
    def get(self, request):
        return render(request, 'auth/manage_profile.html')