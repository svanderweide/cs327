import datetime
from decimal import ROUND_HALF_UP, Decimal

class Transaction:

    def __init__(self, amount, date):
        self.amount = Decimal(amount)
        self.date = datetime.date.fromisoformat(date)
    
    def __repr__(self):
        date = self.date.isoformat()
        amount = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{date}, ${amount}"
