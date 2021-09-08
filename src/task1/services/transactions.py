from datetime import datetime as dt, timedelta
from typing import List

from ..models import Account, Transaction


def get_transactions(account: Account,
                     start_date: str = None,
                     end_date: str = None,
                     filter_field: str = None,
                     sort_by_field: str = None
                     ) -> List[Transaction]:
    """
    :param sort_by_field: a field name which is used to sort an array of transactions
    :param filter_field: a filter value which is used for filtering. Now allowed values are ('income', 'outcome')
    :param account: An account
    :param start_date: a date (without time) - the start of the period
    :param end_date: a date (without time) - the end of the period (including the date)
    :return: a list of transactions inside the specified period
    """
    transactions = account.transactions.all()

    # configure date period
    if start_date is None:
        start_date = dt.fromtimestamp(0).isoformat()
    if end_date is None:
        end_date = dt.now().isoformat()
    start_date: dt = dt.fromisoformat(start_date)
    end_date: dt = dt.fromisoformat(end_date) + timedelta(days=1)

    transactions = transactions.filter(date__lt=end_date).filter(date__gte=start_date)

    # configure filter field
    filter_to_mapping = {
        'income': {'amount__gt': 0},
        'outcome': {'amount__lt': 0}
    }
    condition = filter_to_mapping.get(filter_field, {})
    transactions = transactions.filter(**condition)

    # sort query set
    if sort_by_field in ('date', 'amount'):
        transactions = transactions.order_by(sort_by_field)

    return list(transactions)
