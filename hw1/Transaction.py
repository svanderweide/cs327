import datetime
from decimal import ROUND_HALF_UP, Decimal

class Transaction:
    """
    Contains information about an individual transaction
    for a bank account
    
    Attributes:
        amount (Decimal): stores the amount of the transaction
        date (date): stores the date of the transaction as ISO date
    """

    def __init__(self, amount, date):
        """
        Initializes class attributes
        
        Args:
            amount (str): amount of transaction
            date (str): date of transaction
        """
        self.amount = Decimal(amount)
        self.date = datetime.date.fromisoformat(date)
    
    def __repr__(self):
        """Creates string representation"""
        date = self.date.isoformat()
        amount = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{date}, ${amount}"
