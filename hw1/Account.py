import datetime
from decimal import ROUND_HALF_UP, Decimal
from Transaction import Transaction

class Account:
    """Contains information related to an account"""

    def __init__(self, num):
        """
        Initializes class attributes
        
        Args:
            num (numeric):  account number at the bank
        """
        self._num = num
        self._transactions = []
        self._balance = Decimal(0)
        self._interest_rate = Decimal(0)

    def get_transactions(self):
        """Print all of an account's transactions"""
        for transaction in self._transactions:
            print(transaction)

    def get_balance(self):
        """Return the balance of an account rounded to cents"""
        return self._balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def get_num(self):
        """Return the account number at the bank"""
        return self._num

    def add_transaction(self, amount, date):
        """
        Add a transaction to an account at a bank
        (if it is a valid transaction for the account)
        
        Args:
            amount (str): amount of transaction
            date (str): date of transaction
        """
        if (self._validate_transaction(amount, date)):
            self._add_transaction(amount, date, False)
    
    def add_interest(self):
        """Add transactions for interest on balance"""
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
    """Account subclass for Savings account"""
    
    def __init__(self, num):
        """
        Initializes class attributes
        
        Args:
            num (numeric):  account number at the bank
        """
        super().__init__(num)
        self._interest_rate = Decimal('0.029')
    
    def __str__(self):
        """Returns string representation of savings account"""
        balance = self.get_balance()
        return f"Savings#{self.num:0>9},\tbalance: ${balance}"
    
    def _validate_transaction(self, amount, date):

        # converts date string to ISO date
        iso_date = datetime.date.fromisoformat(date)

        # finds number of transactions in same day and same month
        same_month = 0
        same_day = 0
        for transaction in self._transactions:
            if (transaction.automated is False):
                if (transaction.date.month == iso_date.month):
                    same_month += 1
                    if (transaction.date.day == iso_date.day):
                        same_day += 1
        
        # savings account-specific validation
        if same_day < 2 and same_month < 5:
            # general account validation
            return super()._validate_transaction(amount, date)
        else:
            return False


class Checking(Account):
    """Account subclass for Checking account"""
    
    def __init__(self, num):
        """
        Initializes class attributes
        
        Args:
            num (numeric):  account number at the bank
        """
        super().__init__(num)
        self._interest_rate = Decimal('0.0012')
    
    def __str__(self):
        """Returns string representation of checking account"""
        balance = self.get_balance()
        return f"Checking#{self.num:0>9},\tbalance: ${balance}"

    def add_interest(self):
        """Adds transactions for interest and $10 fee if balance < $100"""
        super().add_interest()
        if (self._balance < Decimal('100')):
            date = datetime.date.today().isoformat()
            self.add_transaction('-10', date, False)
