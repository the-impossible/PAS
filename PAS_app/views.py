# My Django imports
from django.shortcuts import render
from django.views import View

# My App imports


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'pas/index.html')