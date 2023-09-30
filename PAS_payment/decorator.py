# My django imports
from django.contrib.auth.models import AnonymousUser
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages

# My app imports
from PAS_payment.models import Payments
from PAS_app.models import Session

# Determining if the user is an admin
def has_paid(func):
    def wrapper_func(request, *args, **kwargs):

        session = Session.objects.filter(is_current=True).first()
        payment = Payments.objects.filter(student=request.user, status="success", session=session).exists()

        if payment:
            return func(request, *args, **kwargs)
        else:
            messages.warning(request, 'You have no payment record, you are not authorized to view that page')
            return redirect('payment:make_payment')
    return wrapper_func

def double_payment(func):
    def wrapper_func(request, *args, **kwargs):

        session = Session.objects.filter(is_current=True).first()
        payment = Payments.objects.filter(student=request.user, status="success", session=session).exists()

        if payment:
            messages.warning(request, 'You have an existing payment record!!')
            return redirect('auth:dashboard')
        else:
            payment = Payments.objects.filter(student=request.user, status="pending", session=session).exists()

            if not payment:

                return func(request, *args, **kwargs)
            else:
                messages.warning(request, 'You have pending transaction, kindly re-query pending transaction')
                return redirect('payment:my_payments')

    return wrapper_func
