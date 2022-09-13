import datetime
from Account import Account, Savings, Checking

class Bank:
    """Contains information about accounts at a bank"""    

    def __init__(self) -> None:
        self._accounts: list = []
        self._max_id: int = 1
    
    def add_account(self, type: str, init_bal: str) -> None:
        """Creates and adds an account to the bank"""
        
        # savings account if 'savings'
        if type == "savings":
            acct = Savings(self._max_id)
        # checking account if 'checking'
        elif type == "checking":
            acct = Checking(self._max_id)
        # otherwise, invalid type
        else: return

        self._max_id += 1
        
        # create account's initial transaction
        date = datetime.date.today().isoformat()
        acct.add_transaction(init_bal, date)

        # add account to bank's tracked accounts
        self._accounts.append(acct)

    def get_account_by_id(self, id: str) -> Account:
        """Returns the account with the given id"""
        for acct in self._accounts:
            if acct.id_matches(id):
                return acct
        return None

    def _get_accounts(self):
        """Return the accounts stored in the bank"""
        return self._accounts
    
    accounts = property(_get_accounts)
