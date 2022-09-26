"""
transaction module

implements Transaction class to store transaction information
"""

from datetime import datetime
from decimal import setcontext, BasicContext, Decimal

# set Decimal context for rounding
setcontext(BasicContext)

class Transaction:
    """Represents an individual transaction"""

    def __init__(self, amt, date=None, exempt=False) -> None:
        """
        Args:
            amt (str): dollar amount of transaction
            date (str, default=None): date in ISO format (YYYY-MM-DD)
            exempt (bool, default=False): exempt from account limits
        """
        self._amt = Decimal(amt)
        if date is None:
            self._date = datetime.now().date()
        else:
            self._date = datetime.strptime(date, "%Y-%m-%d").date()
        self._exempt = exempt

    def __str__(self) -> str:
        return f"{self._date}, ${self._amt:,.2f}"

    def is_exempt(self) -> bool:
        """Check if transaction is exempt from limits"""
        return self._exempt

    def _get_day(self) -> int:
        """Getter for day of a transaction"""
        return self._date.day

    def _get_month(self) -> int:
        """Getter for month of a transaction"""
        return self._date.month

    def _get_year(self) -> int:
        """Getter for year of a transaction"""
        return self._date.year

    day = property(_get_day)
    month = property(_get_month)
    year = property(_get_year)

    def in_same_month(self, other):
        """Check if two transactions occur in same month"""
        return self.year == other.year and self.month == other.month

    def in_same_day(self, other):
        """Check if two transactions occur in the same day"""
        return self.day == other.day and self.in_same_month(other)

    def __radd__(self, other):
        """Required for sum() with Transaction instances"""
        return other + self._amt

    def check_balance(self, balance):
        """Checks if the Transaction would overdraw the balance given

        Args:
            balance (Decimal): current balance
        """
        return self._amt >= 0 or balance > abs(self._amt)

    def __lt__(self, other):
        """Compares Transactions by date"""
        return self._date < other._date
