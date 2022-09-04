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
        new_transaction = Transaction(amount, date)
        self.transactions.append(new_transaction)
        self.balance += new_transaction.amount
    
    def get_balance(self):
        return self.balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

class Savings(Account):
    
    def __init__(self, num):
        Account.__init__(self, num)
        self.interest_rate = Decimal('0.029')
    
    def __repr__(self):
        balance = self.get_balance()
        return f"Savings#{self.num:0>9},\tbalance: ${balance}"
        

class Checking(Account):
    
    def __init__(self, num):
        Account.__init__(self, num)
        self.interest_rate = Decimal('0.0012')
    
    def __repr__(self):
        balance = self.get_balance()
        return f"Checking#{self.num:0>9},\tbalance: ${balance}"
