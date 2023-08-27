from django.db import models
from PAS_auth.models import User
from PAS_app.models import Session
import uuid

# Create your models here.

class PaymentBreakDown(models.Model):
    item = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.item} | {self.amount}'


    class Meta:
        db_table = 'Payment Breakdown'
        verbose_name_plural = "Payment Breakdown"

class Payments(models.Model):
    payment_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)

    tx_ref = models.CharField(max_length=500)
    transaction_id = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    amount = models.DecimalField(max_digits=7, decimal_places=2)
    status = models.CharField(max_length=500)

    student = models.ForeignKey(User,blank=True, null=True, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, blank=True, null=True, on_delete=models.CASCADE)

    date_created = models.DateTimeField(verbose_name='date_created', auto_now=True, null=True)

    def __str__(self):
        return f'{self.student} | {self.amount}'


    class Meta:
        db_table = 'Payments'
        verbose_name_plural = "Payments"
