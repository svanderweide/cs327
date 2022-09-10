import datetime
from decimal import ROUND_HALF_UP, Decimal
from Transaction import Transaction

class Account:

    def __init__(self, num):
        self.num = num
        self._transactions = []
        self._balance = Decimal(0)
        self._interest_rate = Decimal(0)

    def get_transactions(self):
        for transaction in self._transactions:
            print(transaction)

    def get_balance(self):
        return self._balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def add_transaction(self, amount, date, automated=False):
        if (automated or self._validate_transaction(amount, date)):
            self._add_transaction(amount, date, automated)
    
    def add_interest(self):
        amount = self._balance * self._interest_rate
        date = datetime.date.today().isoformat()
        self.add_transaction(amount, date, True)
    
    def _add_transaction(self, amount, date, automated):
        new_transaction = Transaction(amount, date, automated)
        self._transactions.append(new_transaction)
        self._balance += Decimal(amount)

    def _validate_transaction(self, amount, date):
        return True if (self._balance + Decimal(amount) > 0) else False

class Savings(Account):
    
    def __init__(self, num):
        super().__init__(num)
        self._interest_rate = Decimal('0.029')
    
    def __str__(self):
        balance = self.get_balance()
        return f"Savings#{self.num:0>9},\tbalance: ${balance}"
    
    def _validate_transaction(self, amount, date):
        
        iso_date = datetime.date.fromisoformat(date)

        same_month = 0
        same_day = 0

        for transaction in self._transactions:
            if (transaction.automated is False):
                if (transaction.date.month == iso_date.month):
                    same_month += 1
                    if (transaction.date.day == iso_date.day):
                        same_day += 1
        
        if same_day < 2 and same_month < 5:
            return super()._validate_transaction(amount, date)
        else:
            return False
    
    def add_interest(self):
        super().add_interest()

class Checking(Account):
    
    def __init__(self, num):
        super().__init__(num)
        self._interest_rate = Decimal('0.0012')
    
    def __repr__(self):
        balance = self.get_balance()
        return f"Checking#{self.num:0>9},\tbalance: ${balance}"

    def add_interest(self):
        super().add_interest()
        if (self._balance < Decimal('100')):
            date = datetime.date.today().isoformat()
            self.add_transaction('-10', date, False)
