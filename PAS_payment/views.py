from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from PAS_payment.models import *
# Create your views here.

class MakePaymentView(LoginRequiredMixin, ListView):
    model = PaymentBreakDown
    queryset = PaymentBreakDown.objects.all()
    template_name = "payment/make_payment.html"
