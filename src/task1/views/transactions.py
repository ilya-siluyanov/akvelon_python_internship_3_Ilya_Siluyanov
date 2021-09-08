import logging
from collections import defaultdict
from datetime import date

import pydantic
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..logs import StringFormatter
from ..models import Account, Transaction
from ..serializers import NewTransaction, TransactionSerializer
from ..services.transactions import get_transactions
from ..utils import check_account_exists, check_transaction_exists

logger = logging.getLogger(__name__)
h = logging.StreamHandler()
h.setFormatter(StringFormatter())
logger.addHandler(h)


class TransactionStatsView(APIView):

    @staticmethod
    @check_account_exists
    def get(request: Request, user_id: int) -> Response:
        """
        Returns a list of transactions inside date period specified by
        start_date and end_date query params and grouped by day with total sum of the day
        If start_date is not specified, it is considered as start of the era
        If end_date is not specified, it is considered as start of the next day.
        :param request: Request object
        :param user_id: account's id
        :return: an object containing a field with a list of aggregated transactions (see above)
        """
        account = Account.objects.get(pk=user_id)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        parsed_trans = defaultdict(lambda: 0)
        for transaction in get_transactions(account, start_date, end_date):
            date_: date = transaction.date.date()
            parsed_trans[date_.isoformat()] += transaction.amount
        answer = []
        for key, value in parsed_trans.items():
            answer.append({'date': key, 'sum': value})
        return Response(data=answer)


class TransactionSetView(APIView):

    @staticmethod
    @check_account_exists
    def get(request: Request, user_id: int) -> Response:
        """
        Returns a list of transactions inside date period specified by
        start_date and end_date query params
        If start_date is not specified, it is considered as start of the era
        If end_date is not specified, it is considered as start of the day after start_date
        :param request: Request object
        :param user_id: account's id
        :return: an object containing a field with a list of transactions
        """
        account = Account.objects.get(pk=user_id)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        filter_field = request.query_params.get('filter')
        sort_by_field = request.query_params.get('sort_by')
        transactions = get_transactions(account, start_date, end_date, filter_field, sort_by_field)
        for i, tr in enumerate(transactions):
            transactions[i] = {
                'id': tr.id,
                'amount': tr.amount,
                'date': tr.date,
                'user_id': tr.user.id,
            }
        return Response(data={'transactions': transactions})

    @staticmethod
    @check_account_exists
    def post(request: Request, user_id: int) -> Response:
        user = Account.objects.get(pk=user_id)
        try:
            new_transaction = NewTransaction(**request.data)
            transactions = user.transactions.filter(idempotency_key=new_transaction.idempotency_key)
            if len(transactions) > 0:
                raise ValueError('Try to duplicate transactions with key %s', new_transaction.idempotency_key)
        except pydantic.ValidationError as e:
            logger.warning(e.json())
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            logger.warning(e)
            return Response(data={}, status=status.HTTP_409_CONFLICT)

        request.data['user'] = Account.objects.get(pk=user_id)
        new_transaction = Transaction(**request.data)
        new_transaction.save()
        return Response(data={}, status=status.HTTP_201_CREATED)


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
