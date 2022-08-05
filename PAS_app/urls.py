# My Django imports
from django.urls import path

# My App imports
from PAS_app.views import (
    HomeView,
)

app_name = 'app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
