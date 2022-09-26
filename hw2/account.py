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

class OverdrawError(Exception):
    """Custom exception to handle overdrawn balance errors"""

class TransactionLimitError(Exception):
    """Custom exception to handle invalid transactions on Savings accounts"""

class Account:
    """Abstract class for account subclasses"""

    def __init__(self, num: int) -> None:
        self._num = num
        self._transactions = []
        self._interest_rate = Decimal(0)

    def __str__(self) -> str:
        """Formats the account's number and balance"""
        return f"#{self._num:0>9},\tbalance: ${self.balance:,.2f}"

    def _get_balance(self) -> Decimal:
        """Calculates the balance for an account by summing its transactions

        Returns:
            Decimal: current balance
        """
        return sum(x for x in self._transactions)

    balance = property(_get_balance)

    def _get_transactions(self) -> list[Transaction]:
        """Returns sorted list of the account's transaction"""
        return sorted(self._transactions)

    transactions = property(_get_transactions)

    def add_transaction(self, amt, *, date=None, exempt=False) -> None:
        """
        Creates a pending transaction with given amount and date
        and adds transaction to the account if allowed by account rules

        Args:
            amt (str): amount of incoming transaction
            date (str, kw, default=None): date of incoming transaction
            exempt (bool, kw, default=False): exempt from account rules
        """
        # create transaction
        trans = Transaction(amt, date, exempt)

        # check account rules
        bal_ok = self._check_balance(trans)
        lim_ok = self._check_limits(trans)

        if trans.is_exempt():
            self._transactions.append(trans)
        elif not bal_ok:
            raise OverdrawError
        elif not lim_ok:
            raise TransactionLimitError
        else:
            self._transactions.append(trans)

    def _check_balance(self, trans: Transaction) -> bool:
        """Checks whether an incoming transaction overdraws the balance

        Args:
            t (Transaction): incoming transaction

        Returns:
            bool: False if account is overdrawn
        """
        return trans.check_balance(self._get_balance())

    def _check_limits(self, trans1: Transaction) -> bool:
        return trans1 is not None

    def interest_and_fees(self) -> None:
        """Calculate interest and fees for the account"""
        self._interest()
        self._fees()

    def _interest(self) -> None:
        """Calculate interest for the current balance and add
        as a new transaction exempt from account limits"""
        interest: Decimal = self._get_balance() * self._interest_rate
        self.add_transaction(interest, exempt=True)

    def _fees(self) -> None:
        pass


class SavingsAccount(Account):
    """Account subclass for Savings account"""

    def __init__(self, num: int) -> None:
        super().__init__(num)
        self._interest_rate = Decimal('0.029')
        self._day_lim = 2
        self._month_lim = 5

    def __str__(self) -> str:
        return "Savings" + super().__str__()

    def _check_limits(self, trans1: Transaction) -> bool:
        """Checks if incoming transaction is allowed given account limits

        Args:
            trans (Transaction): incoming transaction to be checked

        Returns:
            bool: True if allowed, False if not allowed
        """
        same_day = 0
        same_month = 0
        for trans2 in self._transactions:
            if not trans2.is_exempt() and trans2.in_same_day(trans1):
                same_day += 1
            if not trans2.is_exempt() and trans2.in_same_month(trans1):
                same_month += 1

        return same_day < self._day_lim and same_month < self._month_lim


class CheckingAccount(Account):
    """Account subclass for Checking account"""

    def __init__(self, num: int) -> None:
        super().__init__(num)
        self._interest_rate = Decimal('0.0012')
        self._balance_threshold = Decimal(100)
        self._low_balance_fee = Decimal(-10)

    def __str__(self) -> str:
        return "Checking" + super().__str__()

    def _fees(self) -> None:
        """Adds a low-balance fee if balance below threshold"""
        if self._get_balance() < self._balance_threshold:
            self.add_transaction(self._low_balance_fee, exempt=True)
