from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.http import JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.utils.decorators import method_decorator
from PAS_payment.models import *
from PAS_payment.decorator import *
from django.conf import settings
import uuid
import requests
# Create your views here.

class MakePaymentView(LoginRequiredMixin, ListView):
    model = PaymentBreakDown
    queryset = PaymentBreakDown.objects.all()
    template_name = "payment/make_payment.html"

    def get_context_data(self, **kwargs):
        context = super(MakePaymentView, self).get_context_data(**kwargs)
        context['total'] = get_total()
        return context

def generate_transaction_reference():
    # Generate a random UUID
    unique_id = uuid.uuid4()

    # Create a unique transaction reference by combining the timestamp and UUID
    transaction_reference = f"PMS-{unique_id}"

    return transaction_reference


def get_total():
    total = 0
    for item in PaymentBreakDown.objects.all():
        total += item.amount
    return total

@method_decorator(double_payment, name="get")
class GetPaymentLink(LoginRequiredMixin, View):
    template_name = "payment/make_payment.html"

    def get(self, request):
        # Define your API endpoint
        flutterwave_endpoint = "https://api.flutterwave.com/v3/payments"

        # Set your Flutterwave API secret key
        api_secret_key = settings.FLUTTERWAVE_SECRET_KEY

        # Define the data you want to send to Flutterwave (adjust as needed)

        current_site = get_current_site(request).domain

        data = {
            "tx_ref": str(generate_transaction_reference()),
            "amount": str(get_total() + 100),  # Adjust the amount as needed
            "currency": "NGN",  # Currency code
            "redirect_url": "https://kadpolypms.ng/payment/verify_payment",  # Redirect URL after payment
            "meta": {
                'customer_id':request.user.username,
                'customer_mac':str(request.user.pk),
            },
            "customer":{
                'email': request.user.email,
                'phone': request.user.phone,
                'name': request.user.get_fullname(),
            },
            "customizations":{
                'title':"PMS Payment",
                'logo':"https://kadpolypms.ng/static/img/comlogo.png",
                'description':'Departmental project fee'
            },
            # Add other required parameters here
            "payment_options": "card, ussd, banktransfer",
        }

        # Set headers with your API key
        headers = {
            "Authorization": f"Bearer {api_secret_key}",
            "Content-Type": "application/json",
        }

        # Make the POST request to create the payment link
        try:
            response = requests.post(flutterwave_endpoint, json=data, headers=headers)

            # Check for a successful response
            if response.status_code == 200:
                # You can parse the response JSON here
                flutterwave_data = response.json()

                # create a payment invoice
                session = Session.objects.filter(is_current=True).first()
                Payments.objects.create(amount=get_total(), tx_ref=data['tx_ref'], student=request.user, status='pending', description="Project Fee", session=session)

                return redirect(flutterwave_data['data']['link'])
            else:
                messages.error(request, 'Failed to initialize payment try again!!')
                return redirect('payment:make_payment')

        except Exception as e:
            messages.error(request, f'An error occurred here check your internet connection!!')
            return redirect('payment:make_payment')


class MyPaymentView(LoginRequiredMixin, ListView):
    model = Payments
    queryset = Payments.objects.all()
    template_name = "payment/my_payments.html"

    def get_queryset(self):
        return Payments.objects.filter(student=self.request.user).order_by('-date_created')


class AllPaymentView(LoginRequiredMixin, ListView):
    model = Payments
    queryset = Payments.objects.all().order_by('-date_created')
    template_name = "payment/my_payments.html"

class VerifyPayment(LoginRequiredMixin, View):

    def get(self, request):

        if request.GET.get('status') == 'successful':
            tx_ref = request.GET.get('tx_ref')
            transaction_id = request.GET.get('transaction_id')

            verify_payment(request, tx_ref, transaction_id, True)
        else:
            messages.error(request, f'Transaction Failed!!')

        if request.user.is_staff:
            return redirect('payment:verify_payments')

        return redirect('payment:my_payments')

class ReVerifyPayment(LoginRequiredMixin, View):
    template_name = "payment/make_payment.html"

    def get(self, request, payment_id):
        try:
            transaction = Payments.objects.get(payment_id=payment_id)
            verify_payment(request, transaction.tx_ref, transaction.transaction_id, False)

        except Payments.DoesNotExist:
            messages.error(request, f'Failed to Re-query Transaction')

        if request.user.is_staff:
            return redirect('payment:verify_payments')

        return redirect('payment:my_payments')


def verify_payment(request, tx_ref, transaction_id, fresh=True):
    try:

        transaction_details = Payments.objects.get(tx_ref=tx_ref)

        if fresh:
            transaction_details.transaction_id=transaction_id
            # Define your API endpoint
            flutterwave_endpoint = f"https://api.flutterwave.com/v3/transactions/{transaction_id}/verify"
        else:
            flutterwave_endpoint = f"https://api.flutterwave.com/v3/transactions/verify_by_reference?tx_ref={transaction_details.tx_ref}"

        # Set your Flutterwave API secret key
        api_secret_key = settings.FLUTTERWAVE_SECRET_KEY

        # Set headers with your API key
        headers = {
            "Authorization": f"Bearer {api_secret_key}",
            "Content-Type": "application/json",
        }

        # Send a GET request to Flutterwave's verification endpoint
        response = requests.get(flutterwave_endpoint, headers=headers)

        # Check for a successful response
        if response.status_code == 200:
            # You can parse the response JSON here
            flutterwave_data = response.json()

            if (
                flutterwave_data["data"]["status"] == "successful"
                and flutterwave_data["data"]["amount"] >= transaction_details.amount
            ):
                # Success! Confirm the customer's payment
                transaction_details.status = "success"
                messages.success(request, 'Transaction successful, print out your receipt!!')
            else:
                transaction_details.status = "failed"
                messages.error(request, 'Transaction Failed!!')

        else:
            transaction_details.status = "failed"
            messages.error(request, 'Transaction failed')

        transaction_details.save()
    except Payments.DoesNotExist:
        messages.error(request, f'Failed in getting transaction reference!!')

    except Exception as e:
        messages.error(request, f'An error occurred while performing verification!!')


