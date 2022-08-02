# My Django imports
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

# My App imports

# Create your views here.
def create_student(self):
    with open('../PAS_student.csv', r, encoding='utf-8') as file:
        print(file.readline())
