"""
bank module

implements Bank class to aggregate Accounts
"""

import logging
from account import Account, SavingsAccount, CheckingAccount

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship, backref

from db import Base

# constants for pattern matching
SAVINGS = "savings"
CHECKING = "checking"

class Bank(Base):
    """Contains information about accounts at a bank"""

    __tablename__ = "bank"

    _id = Column(Integer, primary_key=True)
    _accounts = relationship("Account", backref=backref("bank"))

    # def __init__(self) -> None:
    #     self._accounts: dict = {}

    def add_account(self, acct_type: str) -> Account:
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

        self._accounts[acct_num] = acct
        return self._accounts.get(acct_num)

    def _generate_account_number(self) -> int:
        return len(self._accounts) + 1

    def _get_accounts(self) -> list:
        """Getter method for accounts"""
        return list(self._accounts.values())

    accounts = property(_get_accounts)

    def get_account(self, num: str) -> Account:
        """Returns the account with the given account num

        Args:
            num (str): account number to check

        Returns:
            Account: Account with given number or None
        """
        return self._accounts.get(int(num))

    accounts = property(_get_accounts)
