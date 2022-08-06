# My Django imports
from django.urls import path

# My App imports
from PAS_auth.views import (
    LoginView,
    ResetPasswordView,
    DashboardView,
)

app_name = 'auth'

urlpatterns = [
    # Authentication
    path('login', LoginView.as_view(), name='login'),
    path('reset_password', ResetPasswordView.as_view(), name='reset_password'),
    # Dashboard
    path('dashboard', DashboardView.as_view(), name='dashboard'),

]
