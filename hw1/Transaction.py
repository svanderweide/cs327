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
            manual (bool): automated vs. manual transaction
        """
        self.amount = Decimal(amount)
        self.date = datetime.date.fromisoformat(date)
        self.automated = automated
    
    def __repr__(self):
        """Creates string representation"""
        date = self.date.isoformat()
        amount = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{date}, ${amount}"
