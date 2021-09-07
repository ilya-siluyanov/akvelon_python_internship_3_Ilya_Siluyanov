from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Account, Transaction


class TransactionSetView(APIView):

    @staticmethod
    def get(request: Request, user_id: int) -> Response:
        try:
            user = Account.objects.get(pk=user_id)
        except Account.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        transactions = user.transactions.all()
        return Response(data={
            'transactions': transactions
        })

    @staticmethod
    def post(request: Request, user_id: int) -> Response:
        # TODO: validate input
        try:
            user = Account.objects.get(pk=user_id)
            idem_key = request.data['idempotency_key']
            transaction = user.transactions.filter(idempotency_key=idem_key)
            if transaction is not None:
                raise ValueError('Try to duplicate transactions with key %s', idem_key)
        except Account.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response(data={}, status=status.HTTP_409_CONFLICT)

        request.data['user_id'] = user_id
        new_transaction = Transaction(**request.data)
        new_transaction.save()
        return Response(data={}, status=status.HTTP_201_CREATED)


class TransactionView(APIView):

    @staticmethod
    def get(request: Request, user_id: int, transaction_id: int) -> Response:
        try:
            user = Account.objects.get(pk=user_id)
        except Account.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)

        try:
            transaction = user.transactions.get(pk=transaction_id)
        except Transaction.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)

        # TODO: add a validator
        return Response(data={
            'amount': transaction.amount,
            'date': transaction.date,
        })

    @staticmethod
    def patch(request: Request, user_id: int, transaction_id: int):
        try:
            user = Account.objects.get(pk=user_id)
        except Account.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)

        try:
            transaction = user.transactions.get(pk=transaction_id)
        except Transaction.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)

        # TODO: update fields and check for validity of fields
        return Response(data={}, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request: Request, user_id: int, transaction_id: int):
        try:
            user = Account.objects.get(pk=user_id)
        except Account.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)

        try:
            transaction = user.transactions.get(pk=transaction_id)
        except Transaction.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)

        transaction.delete()
        return Response(data={}, status=status.HTTP_200_OK)
