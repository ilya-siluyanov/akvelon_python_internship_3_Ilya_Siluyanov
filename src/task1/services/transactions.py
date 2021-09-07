from datetime import datetime as dt, timedelta
from typing import List

from ..models import Account, Transaction


def get_transactions(account: Account,
                     start_date: str = None,
                     end_date: str = None) -> List[Transaction]:
    if start_date is None:
        start_date = dt.fromtimestamp(0)
    if end_date is None:
        end_date = dt.now()
    start_date: dt = dt.fromisoformat(start_date)
    end_date: dt = dt.fromisoformat(end_date) + timedelta(days=1)
    return account.transactions.all().filter(date__lt=end_date).filter(start_date__gte=start_date)
