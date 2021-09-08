import pydantic
from rest_framework import serializers

from ..models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'


class NewAccount(pydantic.BaseModel):
    first_name: str
    last_name: str
    email: str
