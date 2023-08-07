from django.db import models

# Create your models here.

class PaymentBreakDown(models.Model):
    item = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'{self.item} | {self.amount}'

    class Meta:
        db_table = 'Payment Breakdown'
        verbose_name_plural = "Payment Breakdown"
