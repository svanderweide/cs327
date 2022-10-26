"""
bank module

implements Bank class to aggregate Accounts
"""

# library modules
import logging

# SQL modules
from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, backref

# custom modules
from db import Base
from account import Account, SavingsAccount, CheckingAccount

# constants for pattern matching
SAVINGS = "savings"
CHECKING = "checking"

class Bank(Base):
    """Contains information about accounts at a bank"""

    __tablename__ = "bank"

    _id = Column(Integer, primary_key=True)
    _accounts = relationship("Account", backref=backref("bank"))

    def add_account(self, acct_type, session) -> Account:
        """Creates and adds an account to the bank

        Args:
            type (str): "savings" or "checking" to indicate accont type

        Returns:
            Account: Account object created or None if type not matched
        """
        acct_num = self._generate_account_number()

        if acct_type == SAVINGS:
            acct = SavingsAccount(acct_num)
        elif acct_type == CHECKING:
            acct = CheckingAccount(acct_num)
        else:
            return None

        logging.debug(f"Created account: {acct_num}")

        self._accounts.append(acct)
        session.add(acct)
        session.commit()
        return acct

    def _generate_account_number(self) -> int:
        return len(self._accounts) + 1

    def _get_accounts(self) -> list:
        """Getter method for accounts"""
        return self._accounts

    accounts = property(_get_accounts)

    def get_account(self, num: str) -> Account:
        """Returns the account with the given account num

        Args:
            num (str): account number to check

        Returns:
            Account: Account with given number or None
        """
        for acct in self._accounts:
            if acct.num == int(num):
                return acct
        return None
