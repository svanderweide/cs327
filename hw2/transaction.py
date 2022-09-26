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
            amt (string): dollar amount of transaction
            date (string, default=None): date in ISO format (YYYY-MM-DD)
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

    def is_exempt(self):
        """Check if transaction is exempt from limits"""
        return self._exempt

    def in_same_month(self, other):
        """Check if two transactions occur in same month"""
        return self._date.year == other._date.year and self._date.month == other._date.month

    def in_same_day(self, other):
        """Check if two transactions occur in the same day"""
        return self._date.day == other._date.day and self.in_same_month(self, other)

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
