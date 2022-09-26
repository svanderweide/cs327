"""
bank module

implements Bank class to aggregate Accounts
"""

import datetime
from account import Account, Savings, Checking

class Bank:
    """Contains information about accounts at a bank"""

    def __init__(self) -> None:
        self._accounts: list = []
        self._max_num: int = 1

    def add_account(self, acct_type: str, init_bal: str) -> None:
        """Creates and adds an account to the bank"""

        # savings account if 'savings'
        if acct_type == "savings":
            acct = Savings(self._max_num)
        # checking account if 'checking'
        elif acct_type == "checking":
            acct = Checking(self._max_num)
        # otherwise, invalid type
        else: return

        self._max_num += 1

        # create account's initial transaction
        date = datetime.date.today().isoformat()
        acct.add_transaction(init_bal, date)

        # add account to bank's tracked accounts
        self._accounts.append(acct)

    def get_account_by_num(self, num: str) -> Account:
        """Returns the account with the given num"""
        for acct in self._accounts:
            if acct.num_matches(num):
                return acct
        return None

    def _get_accounts(self) -> list:
        """Return the accounts stored in the bank"""
        return self._accounts

    accounts = property(_get_accounts)
