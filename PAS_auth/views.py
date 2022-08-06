# My Django imports
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


# My App imports

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