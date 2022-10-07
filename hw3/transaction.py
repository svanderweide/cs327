"""
transaction module

implements Transaction class to store transaction information
"""

from datetime import datetime, date
from decimal import setcontext, BasicContext, Decimal

from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, Float, Boolean, Date

from db import Base

# set Decimal context for rounding
setcontext(BasicContext)

class Transaction(Base):
    """Represents an individual transaction"""

    __tablename__ = "transaction"

    _id = Column(Integer, primary_key=True)
    _amt = Column(Float)
    _date = Column(Date)
    _exempt = Column(Boolean)
    _account_num = Column(Integer, ForeignKey("account._num"))

    def __init__(self, amt, date=None, exempt=False) -> None:
        """
        Args:
            amt (str): dollar amount of transaction
            date (str, default=None): date in ISO format (YYYY-MM-DD)
            exempt (bool, default=False): exempt from account limits
        """
        self._amt = Decimal(amt)
        if date is None:
            self._date = datetime.now().date()
        else:
            self._date = datetime.strptime(date, "%Y-%m-%d").date()
        self._exempt = exempt

    def __str__(self) -> str:
        return f"{self._date}, ${self._amt:,.2f}"

    def is_exempt(self) -> bool:
        """Check if transaction is exempt from limits"""
        return self._exempt

    def _get_date(self) -> date:
        """Getter for date of a transaction"""
        return self._date

    date = property(_get_date)

    def same_year(self, other):
        """Check if two transactions occur in same year"""
        return self.date.year == other.date.year

    def same_month(self, other):
        """Check if two transactions occur in same month"""
        return self.date.month == other.date.month and self.same_year(other)

    def same_day(self, other):
        """Check if two transactions occur in the same day"""
        return self.date.day == other.date.day and self.same_month(other)

    def __radd__(self, other):
        """Required for sum() with Transaction instances"""
        return other + self._amt

    def check_balance(self, balance):
        """Checks if the Transaction would overdraw the balance given

        Args:
            balance (Decimal): current balance
        """
        return self._amt >= 0 or balance >= abs(self._amt)

    def __lt__(self, other):
        return self._date < other._date

    def __le__(self, other):
        return self._date <= other._date
