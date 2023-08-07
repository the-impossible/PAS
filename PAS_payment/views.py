from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

# Create your views here.

class MakePaymentView(TemplateView):
    template_name = "payment/make_payment.html"
