from django.db import models
from django.db.models import fields


class Transaction(models.Model):
    id = fields.AutoField(pk=True)
    user_id = models.ForeignKey(to='Account', on_delete=models.CASCADE)
    amount = models.DecimalField()
    date = models.DateTimeField()

