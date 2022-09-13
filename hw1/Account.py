import datetime
from decimal import ROUND_HALF_UP, Decimal
from Transaction import Transaction

class Account:
    """Contains information related to a bank account"""

    def __init__(self, id: int) -> None:
        """Initializes class attributes"""

        self._id = id
        self._transactions = []
        self._balance = Decimal(0)
        self._interest_rate = Decimal(0)

    def id_matches(self, id: str):
        """Check if this account has the given id"""
        return self._id == int(id)

    def add_transaction(self, amnt: str, date: str):
        """
        Add a transaction to an account at a bank
        (if it is a valid transaction for the account)
        
        Args:
            amnt (str): amount of transaction
            date (str): date of transaction
        """
        if (self._validate_transaction(amnt, date)):
            self._add_transaction(amnt, date, False)
    
    def add_interest(self):
        """Add transactions for interest (and fees) on balance"""
        amnt = self._balance * self._interest_rate
        date = datetime.date.today().isoformat()
        self._add_transaction(amnt, date, True)

    def _get_transactions(self) -> list:
        """Return transactions"""
        return self._transactions
    
    transactions = property(_get_transactions)

    def _get_balance(self) -> Decimal:
        return self._balance.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    def _add_transaction(self, amnt, date, automated):
        new_transaction = Transaction(amnt, date, automated)
        self._transactions.append(new_transaction)
        self._balance += Decimal(amnt)

    def _validate_transaction(self, amnt, date):
        return True if (self._balance + Decimal(amnt) > 0) else False

class Savings(Account):
    """Account subclass for Savings account"""
    
    def __init__(self, id: int):
        super().__init__(id)
        self._interest_rate = Decimal('0.029')
    
    def __str__(self):
        """Returns string representation of savings account"""
        balance = self._get_balance()
        return f"Savings#{self._id:0>9},\tbalance: ${balance}"
    
    def _validate_transaction(self, amnt: str, date: str):

        # temporary transaction
        tmp = Transaction(amnt, date)

        # count transactions with same day and month
        same_month = 0
        same_day = 0
        for transaction in self._transactions:
            if not transaction.automated:
                if tmp.same_month(transaction):
                    same_month += 1
                    if tmp.same_day(transaction):
                        same_day += 1
        
        # savings account-specific validation
        return same_day < 2 and same_month < 5 and super()._validate_transaction(amnt, date)


class Checking(Account):
    """Account subclass for Checking account"""
    
    def __init__(self, id: int):
        super().__init__(id)
        self._interest_rate = Decimal('0.0012')
    
    def __str__(self):
        """Returns string representation of checking account"""
        balance = self._get_balance()
        return f"Checking#{self._id:0>9},\tbalance: ${balance}"

    def add_interest(self):
        """Add transactions for interest (and fees) on balance"""
        super().add_interest()
        if (self._balance < Decimal('100')):
            date = datetime.date.today().isoformat()
            self._add_transaction('-10', date, False)
