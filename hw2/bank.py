"""
bank module

implements Bank class to aggregate Accounts
"""

from account import Account, SavingsAccount, CheckingAccount

# constants for pattern matching
SAVINGS = "savings"
CHECKING = "checking"

class Bank:
    """Contains information about accounts at a bank"""

    def __init__(self) -> None:
        self._accounts: dict = {}

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
