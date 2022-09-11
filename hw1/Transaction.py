import datetime
from decimal import ROUND_HALF_UP, Decimal

class Transaction:
    """
    Contains information about an individual transaction
    for a bank account
    
    Attributes:
        amount (Decimal): amount of the transaction
        date (date): date of the transaction as ISO date
        automated (bool): automated (True) or manual (False)
    """

    def __init__(self, amount, date, automated):
        """
        Initializes class attributes
        
        Args:
            amount (str): amount of transaction
            date (str): date of transaction
            automated (bool): automated vs. manual transaction
        """
        self._amount = Decimal(amount)
        self._date = datetime.date.fromisoformat(date)
        self._automated = automated
    
    def __str__(self):
        """Returns string representation of transaction"""
        date = self._date.isoformat()
        amount = self._amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{date}, ${amount}"
