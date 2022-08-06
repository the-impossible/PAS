# My Django imports
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

# My App imports

# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

class ResetPasswordView(View):
    def get(self, request):
        return render(request, 'auth/password_reset.html')

class DashboardView(View):
    def get(self, request):
        return render(request, 'auth/dashboard.html')