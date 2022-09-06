import datetime
from decimal import ROUND_HALF_UP, Decimal
from Transaction import Transaction

class Account:

    def __init__(self, num):
        self.num = num
        self.transactions = []
        self.balance = Decimal(0)
        self._interest_rate = Decimal(0)

    def get_transactions(self):
        for transaction in self.transactions:
            print(transaction)

    def get_balance(self):
        return self.balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def add_transaction(self, amount, date, automated=False):
        if (automated or self.validate_transaction(amount, date)):
            self.__add_transaction(amount, date, automated)
    
    def __add_transaction(self, amount, date, automated):
        new_transaction = Transaction(amount, date, automated)
        self.transactions.append(new_transaction)
        self.balance += new_transaction.amount

    def validate_transaction(self, amount, date):
        return True if (self.balance + Decimal(amount) > 0) else False
    
    def add_interest(self):
        amount = self.balance * self._interest_rate
        date = datetime.date.today().isoformat()
        self.add_transaction(amount, date, True)

class Savings(Account):
    
    def __init__(self, num):
        super().__init__(num)
        self._interest_rate = Decimal('0.029')
    
    def __repr__(self):
        balance = self.get_balance()
        return f"Savings#{self.num:0>9},\tbalance: ${balance}"
    
    def validate_transaction(self, amount, date):
        
        iso_date = datetime.date.fromisoformat(date)

        same_month = 0
        same_day = 0

        for transaction in self.transactions:
            if (transaction.automated is False):
                if (transaction.date.month == iso_date.month):
                    same_month += 1
                    if (transaction.date.day == iso_date.day):
                        same_day += 1
        
        if same_day < 2 and same_month < 5:
            return super().validate_transaction(amount, date)
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
        if (self.balance < Decimal('100')):
            date = datetime.date.today().isoformat()
            self.add_transaction('-10', date, False)
