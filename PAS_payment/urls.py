from django.urls import path

app_name = "payment"

from PAS_payment.views import *

urlpatterns = [
    path('make_payment', MakePaymentView.as_view(), name='make_payment'),
    path('initialize_payment', GetPaymentLink.as_view(), name='initialize_payment'),

    path('my_payments', MyPaymentView.as_view(), name='my_payments'),
    path('verify_payments', AllPaymentView.as_view(), name='verify_payments'),

    path('verify_payment', VerifyPayment.as_view(), name='verify_payment'),
    path('re_verify_payment/<str:payment_id>', ReVerifyPayment.as_view(), name='re_verify_payment'),

]
