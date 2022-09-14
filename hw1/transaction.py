"""
transaction module

implements Transaction class to store transaction information
"""

import datetime
from decimal import ROUND_HALF_UP, Decimal

class Transaction:
    """Represents an individual transaction"""

    def __init__(self, amnt: str, date: str, automated=False) -> None:
        self._amnt = Decimal(amnt)
        self._date = datetime.date.fromisoformat(date)
        self._automated = automated

    def __str__(self) -> str:
        date = self._date.isoformat()
        amnt = self._amnt.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{date}, ${amnt}"

    def same_month(self, other) -> bool:
        """Return True if transactions in same month"""
        return self._date.month == other._date.month

    def same_day(self, other) -> bool:
        """Return True if transaction on same day in same month"""
        return self._date.day == other._date.day and self.same_month(other)

    def _get_automated(self) -> bool:
        return self._automated

    def __lt__(self, other) -> bool:
        return self._date < other._date

    automated = property(_get_automated)
