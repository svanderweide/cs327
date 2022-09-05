import datetime
from decimal import ROUND_HALF_UP, Decimal
from Transaction import Transaction

class Account:

    def __init__(self, num):
        self.transactions = []
        self.balance = Decimal(0)
        self.num = num

    def get_transactions(self):
        for transaction in self.transactions:
            print(transaction)
    
    def add_transaction(self, amount, date):
        if (self.__validate_transaction(amount, date)):
            new_transaction = Transaction(amount, date)
            self.transactions.append(new_transaction)
            self.balance += new_transaction.amount

    def get_balance(self):
        return self.balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    def __validate_transaction(self, amount, date):
        if (self.balance + Decimal(amount) > 0):
            return True
        else:
            return False

class Savings(Account):
    
    def __init__(self, num):
        super().__init__(num)
        self.interest_rate = Decimal('0.029')
    
    def __repr__(self):
        balance = self.get_balance()
        return f"Savings#{self.num:0>9},\tbalance: ${balance}"
    
    def __validate_transaction(self, amount, date):
        
        iso_date = datetime.date.isoformat(date)

        same_month = 0
        same_day = 0

        for transaction in self.transactions:
            if (transaction.date.month == iso_date.month):
                same_month += 1
                if (transaction.date.day == iso_date.day):
                    same_day += 1
        
        if same_day < 2 and same_month < 5:
            return super().__validate_transaction(amount, date)
        else:
            return False

class Checking(Account):
    
    def __init__(self, num):
        super().__init__(num)
        self.interest_rate = Decimal('0.0012')
    
    def __repr__(self):
        balance = self.get_balance()
        return f"Checking#{self.num:0>9},\tbalance: ${balance}"
