from datetime import datetime

import pydantic
from rest_framework import serializers

from ..models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class NewTransaction(pydantic.BaseModel):
    amount: float
    date: datetime
    idempotency_key: str
