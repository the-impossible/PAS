from django.urls import path

app_name = "payment"

from PAS_payment.views import *

urlpatterns = [
    path('make_payment', MakePaymentView.as_view(), name='make_payment'),

]
