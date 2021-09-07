from django.db import models
from django.db.models import fields


class Transaction(models.Model):
    id = fields.AutoField(primary_key=True)
    user_id = models.ForeignKey(to='Account', on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(decimal_places=10, max_digits=100)  # FIXME
    date = models.DateTimeField()
    idempotency_key = models.CharField(max_length=100)

    class Meta:
        """Define indexes for fast search
        and not creating new transaction records"""
        indexes = [
            models.Index(fields=['idempotency_key'])
        ]
