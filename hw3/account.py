"""
account module

implements classes for accounts (savings and checking)

classes:
    account: general account for a bank
    savings: savings account (lower interest, no fees)
    checking: checking account (higher interest, fees)
"""

# library modules
import logging
from decimal import Decimal
from datetime import date
from calendar import monthrange

# SQL modules
from sqlalchemy.orm import relationship, backref
from sqlalchemy import ForeignKey, Column, Integer, Float, String

# custom modules
from db import Base
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

class Account(Base):
    """Abstract class for account subclasses"""

    __tablename__ = "account"

    _num = Column(Integer, primary_key=True)
    _transactions = relationship("Transaction", backref=backref("account"))
    _interest_rate = Column(Float)
    _interest_triggered = Column(Integer)
    _bank_id = Column(Integer, ForeignKey("bank._id"))
    _type = Column(String(10))

    __mapper_args__ = {
        "polymorphic_identity": "account",
        "polymorphic_on": _type,
    }

    def __init__(self, num: int) -> None:
        self._num = num
        self._interest_rate = 0
        self._interest_triggered = False

    def __str__(self) -> str:
        """Formats the account's number and balance"""
        return f"#{self._num:0>9},\tbalance: ${self.balance:,.2f}"

    def _get_balance(self) -> Decimal:
        """Calculates the balance for an account by summing its transactions

        Returns:
            Decimal: current balance
        """
        return Decimal(sum(x for x in self._transactions))

    balance = property(_get_balance)

    def _get_transactions(self) -> list:
        """Returns sorted list of the account's transaction"""
        return sorted(self._transactions)

    transactions = property(_get_transactions)

    def add_transaction(self, amt, session, *, date=None, exempt=False) -> None:
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
        if trans.is_exempt() and not seq_ok:
            raise TransactionSequenceError(newest.date)
        else:
            # non-exempt transactions care about all errors
            if not bal_ok:
                raise OverdrawError
            if not lim_ok:
                raise TransactionLimitError
            if not seq_ok:
                raise TransactionSequenceError(newest.date)

            # if non-exempt transaction enters new month, enable interest/fees
            if newest is not None and trans.date > self._newest_end_of_month():
                self._interest_triggered = False
                session.add(self)

        # add pending transaction
        self._transactions.append(trans)
        session.add(trans)
        logging.debug(f"Created transaction, {self._num}, {amt}")

        # commit pending transaction
        session.commit()
        logging.debug("Saved to bank.db")


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
        # check if triggering is allowed for exempt transactions
        return newest <= trans and not self._interest_triggered

    def _newest_date(self) -> date:
        """Returns date of most recent transaction on the account
        or today's date if account has no transactions (negative initial amt)
        """
        newest = self._newest_trans()
        return newest.date if newest else date.today()

    newest_date = property(_newest_date)

    def _newest_trans(self) -> Transaction:
        """Returns most recent transaction on the account"""
        return max(self.transactions, default=None)

    def _newest_end_of_month(self) -> date:
        """Returns date for end of month"""
        # get newest transaction
        newest_date = self._newest_date()

        # calculate date attributes
        year = newest_date.year
        month = newest_date.month
        day = monthrange(year, month)[1]

        return date(year, month, day)

    def interest_and_fees(self, session) -> None:
        """Calculate interest and fees for the account"""
        self._interest(session)
        self._fees(session)
        self._interest_triggered = True
        session.add(self)
        session.commit()

    def _interest(self, session) -> None:
        """Calculate interest for the current balance and add
        as a new transaction exempt from account limits"""
        interest = self._get_balance() * Decimal(self._interest_rate)
        interest_date = self._newest_end_of_month().isoformat()
        self.add_transaction(interest,
                             session,
                             date=interest_date,
                             exempt=True)

    def _fees(self, session) -> None:
        pass

    def _get_num(self) -> None:
        return self._num

    num = property(_get_num)


class SavingsAccount(Account):
    """Account subclass for Savings account"""

    __tablename__ = "savingsaccount"

    _num = Column(Integer, ForeignKey("account._num"), primary_key=True)
    _day_lim = Column(Integer)
    _month_lim = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "savingsaccount"
    }

    def __init__(self, num: int) -> None:
        super().__init__(num)
        self._interest_rate = 0.029
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

    __tablename__ = "checkingaccount"

    _num = Column(Integer, ForeignKey("account._num"), primary_key=True)
    _balance_threshold = Column(Integer)
    _low_balance_fee = Column(Integer)

    __mapper_args__ = {
        "polymorphic_identity": "checkingaccount"
    }

    def __init__(self, num: int) -> None:
        super().__init__(num)
        self._interest_rate = 0.0012
        self._balance_threshold = 100
        self._low_balance_fee = -10

    def __str__(self) -> str:
        return "Checking" + super().__str__()

    def _fees(self, session) -> None:
        """Adds a low-balance fee if balance below threshold"""
        if self._get_balance() < Decimal(self._balance_threshold):
            fees_date = self._newest_end_of_month().isoformat()
            self.add_transaction(Decimal(self._low_balance_fee),
                                 session,
                                 date=fees_date,
                                 exempt=True)
