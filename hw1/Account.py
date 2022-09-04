from decimal import ROUND_UP, Decimal
from Transaction import Transaction

class Account:

    account_max = 1

    def __init__(self):
        self.transactions = []
        self.balance = Decimal(0)
        self.num = Account.account_max
        Account.account_max += 1

    def __repr__(self):
        balance = self.balance.quantize(Decimal('0.01'), rounding=ROUND_UP)
        return f"#{self.num:0>9},\tbalance: ${balance}"

    def get_transactions(self):
        for transaction in self.transactions:
            print(transaction)
    
    def add_transaction(self, amount, date):
        new_transaction = Transaction(amount, date)
        self.transactions.append(new_transaction)
        self.balance += new_transaction.amount
