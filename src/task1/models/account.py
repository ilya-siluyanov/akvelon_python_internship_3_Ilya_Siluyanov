from django.db import models
from django.db.models import fields


class Account(models.Model):
    id = fields.AutoField(primary_key=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    email = fields.EmailField(max_length=50)
