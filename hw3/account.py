"""
account module

implements classes for accounts (savings and checking)

classes:
    account: general account for a bank
    savings: savings account (lower interest, no fees)
    checking: checking account (higher interest, fees)
"""

import logging
from decimal import Decimal
from datetime import date
from calendar import monthrange
from transaction import Transaction

class OverdrawError(Exception):
    """Custom exception to handle overdrawn balance errors"""

class TransactionLimitError(Exception):
    """Custom exception to handle invalid transactions on Savings accounts"""

class TransactionSequenceError(Exception):
    """Custom exception to enforce chronological ordering of transactions"""

    def __init__(self, latest_date):
        super().__init__()
        self.latest_date = latest_date

class Account:
    """Abstract class for account subclasses"""

    def __init__(self, num: int) -> None:
        self._num = num
        self._transactions = []
        self._interest_rate = Decimal(0)
        self._interest_triggered = False

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

    def _get_transactions(self) -> list:
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
        seq_ok = self._check_sequence(trans)

        # get newest transaction
        newest = self._newest_trans()

        # exempt transactions only care about sequence errors
        if trans.is_exempt():
            if seq_ok:
                self._transactions.append(trans)
            else:
                raise TransactionSequenceError(newest.date)
        # non-exempt transactions care about all errors
        elif not bal_ok:
            raise OverdrawError
        elif not lim_ok:
            raise TransactionLimitError
        elif not seq_ok:
            raise TransactionSequenceError(newest._date)
        else:
            # if transaction enters new month, enable interest/fees
            if newest is not None and trans.date > self._newest_end_of_month():
                self._interest_triggered = False
            # include transaction
            self._transactions.append(trans)

        logging.debug(f"Created transaction, {self._num}, {amt}")
        

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
    
    def _check_sequence(self, trans: Transaction) -> bool:
        """Checks whether incoming transaction satisfies
        chronological (partial/total) ordering of transactions
        """
        newest = self._newest_trans()
        if newest is None:
            return True
        if not trans.is_exempt():
            return newest <= trans
        else:
            # check if triggering is allowed for exempt transactions
            return newest <= trans and not self._interest_triggered
    
    def _newest_date(self) -> date:
        """Returns date of most recent transaction on the account"""
        return self._newest_trans().date
    
    newest_date = property(_newest_date)

    def _newest_trans(self) -> Transaction:
        """Returns most recent transaction on the account"""
        return max(self.transactions, default=None)
    
    def _newest_end_of_month(self) -> date:
        """Returns date for end of month"""
        # get newest transaction
        newest = self._newest_trans()

        # calculate date attributes
        year = newest.date.year
        month = newest.date.month
        day = monthrange(year, month)[1]

        return date(year, month, day)

    def interest_and_fees(self) -> None:
        """Calculate interest and fees for the account"""
        self._interest()
        self._fees()
        self._interest_triggered = True

    def _interest(self) -> None:
        """Calculate interest for the current balance and add
        as a new transaction exempt from account limits"""
        interest = self._get_balance() * self._interest_rate
        date = self._newest_end_of_month().isoformat()
        self.add_transaction(interest, date=date, exempt=True)

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
        non_exempts = [t for t in self._transactions if not t.is_exempt()]
        same_day = len([t2 for t2 in non_exempts if trans1.same_day(t2)])
        same_month = len([t2 for t2 in non_exempts if trans1.same_month(t2)])
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
            date = self._newest_end_of_month().isoformat()
            self.add_transaction(self._low_balance_fee, date=date, exempt=True)
