# My Django imports
from django.urls import path

# My App imports
from PAS_auth.views import create_student

app_name = 'auth'

urlpatterns = [
    path('', create_student, name='home'),
]
