from rest_framework import status
from rest_framework.response import Response

from .models import Account, Transaction


def fibonacci(n: int) -> int:
    """
    calculates n-th Fibonacci sequence number
    using O(n) time and O(1) memory
    >>> fibonacci(0)
    0
    >>> fibonacci(1)
    1
    >>> fibonacci(10)
    55
    :param n:
    :return: n-th Fibonacci sequence number
    """
    if n < 0:
        # FIXME: raise an exception
        return 0
    a = 1
    if n == 1:
        return a
    b = 1
    if n == 2:
        return b
    for i in range(3, n + 1):
        c = a + b
        a, b = b, c
    return b


def check_account_exists(func):
    def wrapper(*args, **kwargs):
        user_id = kwargs['user_id']
        try:
            Account.objects.get(pk=user_id)
        except Account.DoesNotExist as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        return func(*args, **kwargs)

    return wrapper


def check_transaction_exists(func):
    def wrapper(*args, **kwargs):
        user_id = kwargs['user_id']
        transaction_id = kwargs['transaction_id']
        try:
            user = Account.objects.get(pk=user_id)
            user.transactions.get(pk=transaction_id)
        except (Account.DoesNotExist, Transaction.DoesNotExist) as e:
            return Response(data={}, status=status.HTTP_404_NOT_FOUND)
        return func(*args, **kwargs)

    return wrapper
