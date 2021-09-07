import logging

import pydantic
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Account, Transaction
from ..serializers import NewTransaction, TransactionSerializer


def check_user_exists(func):
    def wrapper(*args, **kwargs):
        user_id = kwargs['user_id']
        try:
            Account.objects.get(pk=user_id)
        except Account.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        return func(*args, **kwargs)

    return wrapper


class TransactionSetView(APIView):

    @staticmethod
    @check_user_exists
    def get(request: Request, user_id: int) -> Response:
        user = Account.objects.get(pk=user_id)
        transactions = user.transactions.all()
        return Response(data={
            'transactions': transactions
        })

    @staticmethod
    @check_user_exists
    def post(request: Request, user_id: int) -> Response:
        user = Account.objects.get(pk=user_id)
        try:
            new_transaction = NewTransaction(request.data)
            transaction = user.transactions.filter(idempotency_key=new_transaction.idempotency_key)
            if transaction is not None:
                raise ValueError('Try to duplicate transactions with key %s', new_transaction.idempotency_key)
        except pydantic.ValidationError as e:
            logging.warning(e.json())
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(data={}, status=status.HTTP_409_CONFLICT)

        request.data['user_id'] = user_id
        new_transaction = Transaction(**request.data)
        new_transaction.save()
        return Response(data={}, status=status.HTTP_201_CREATED)


def check_transaction_exists(func):
    def wrapper(*args, **kwargs):
        user_id = kwargs['user_id']
        transaction_id = kwargs['transaction_id']
        try:
            user = Account.objects.get(pk=user_id)
            transaction = user.transactions.get(pk=transaction_id)
        except (Account.DoesNotExist, Transaction.DoesNotExist) as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        return func(*args, **kwargs)

    return wrapper


class TransactionView(APIView):

    @staticmethod
    @check_transaction_exists
    def get(request: Request, user_id: int, transaction_id: int) -> Response:
        transaction = Transaction.objects.get(pk=transaction_id)
        transaction = TransactionSerializer(transaction).data

        if 'idempotency_key' in transaction:
            del transaction['idempotency_key']
        return Response(transaction)

    @staticmethod
    @check_transaction_exists
    def patch(request: Request, user_id: int, transaction_id: int):
        transaction = Transaction.objects.get(pk=transaction_id)
        serializer = TransactionSerializer(
            instance=transaction,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data={}, status=status.HTTP_200_OK)

    @staticmethod
    @check_transaction_exists
    def delete(request: Request, user_id: int, transaction_id: int):
        transaction = Transaction.objects.get(pk=transaction_id)
        transaction.delete()
        return Response(data={}, status=status.HTTP_200_OK)
