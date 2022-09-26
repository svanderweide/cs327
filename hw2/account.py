"""
account module

implements classes for accounts (savings and checking)

classes:
    account: general account for a bank
    savings: savings account (lower interest, no fees)
    checking: checking account (higher interest, fees)
"""

from decimal import Decimal
from transaction import Transaction

class Account:
    """Abstract class for account subclasses"""

    def __init__(self, num: int) -> None:
        self._num = num
        self._transactions = []

    def add_transaction(self, amt, *, date=None, exempt=False):
        """
        Creates a pending transaction with given amount and date
        and adds transaction to the account if allowed by account rules
        
        Args:
            amt (str): amount of incoming transaction
            date (str, kw, default=None): date of incoming transaction
            exempt (bool, kw, default=False): exempt from account rules
        """
        # create transaction
        t = Transaction(amt, date, exempt)

        # check account rules
        bal_ok = self._check_balance(t)
        lim_ok = self._check_limits(t)

        if t.is_exempt() or (bal_ok and lim_ok):
            self._transactions.append(t)

    def _check_balance(self, t: Transaction) -> bool:
        """Checks whether an incoming transaction overdraws the balance
        
        Args:
            t (Transaction): incoming transaction

        Returns:
            bool: False if account is overdrawn
        """
        return t.check_balance(self.get_balance())
    
    def _check_limits(self, t: Transaction) -> bool:
        return True

    def get_balance(self):
        """Calculates the balance for an account by summing its transactions
        
        Returns:
            Decimal: current balance
        """
        return sum(x for x in self._transactions)

    def interest_and_fees(self):
        """Calculate interest and fees for the account"""
        self._interest()
        self._fees()

    def _interest(self):
        """Calculate interest for the current balance and add
        as a new transaction exempt from account limits"""
        interest: Decimal = self.get_balance() * self._interest_rate
        self.add_transaction(interest, exempt=True)
    
    def __str__(self) -> str:
        """Formats the account's number and balance
        (e.g., '#000000001,\tbalance: $100.00)'
        """
        balance = self._get_balance()
        return f"#{self._num:0>9},\tbalance: ${self.get_balance():,.2f}"

    def get_transactions(self):
        """Returns sorted list of the account's transaction"""
        return sorted(self._transactions)


class SavingsAccount(Account):
    """Account subclass for Savings account"""

    def __init__(self, num: int) -> None:
        super().__init__(num)
        self._interest_rate = Decimal('0.029')
        self._day_lim = 2
        self._month_lim = 5
    
    def _check_limits(self, t1: Transaction) -> bool:
        """Checks if incoming transaction is allowed given account limits
        
        Args:
            t1 (Transaction): incoming transaction to be checked

        Returns:
            bool: True if allowed, False if not allowed
        """
        same_day = 0
        same_month = 0
        for t2 in self._transactions:
            if not t2.is_exempt() and t2.in_same_day(t1):
                same_day += 1
            if not t2.is_exempt() and t2.in_same_month(t1):
                same_month += 1
        
        return same_day < self._day_lim and same_month < self._month_lim

    def __str__(self) -> str:
        return "Savings" + super().__str__()


class CheckingAccount(Account):
    """Account subclass for Checking account"""

    def __init__(self, num: int) -> None:
        super().__init__(num)
        self._interest_rate = Decimal('0.0012')
        self._balance_threshold = Decimal(100)
        self._low_balance_fee = Decimal(-10)

    def _fees(self):
        """Adds a low-balance fee if balance below threshold"""
        if self.get_balance() < self._balance_threshold:
            self.add_transaction(self._low_balance_fee, exempt=True)

    def __str__(self) -> str:
        return "Checking" + super().__str__()
