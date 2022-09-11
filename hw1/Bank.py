import datetime
from Account import Account, Savings, Checking

class Bank:
    """Contains information about accounts at a bank"""    

    def __init__(self):
        self._accounts: Account = []
        self._max_account = 1
    
    def add_account(self, type, initial_amt):
        """
        Creates and adds an account to the bank

        Args:
            type (str):         'savings' for Savings; else, Checking
            initial_amt (str):  initial bank account balance
        """
        
        # create savings/checking account based on 'type'
        if type == "savings":
            acct = Savings(self._max_account)
        else:
            acct = Checking(self._max_account)
        self._max_account += 1
        
        # create account's initial transaction
        date = datetime.date.today().isoformat()
        acct.add_transaction(initial_amt, date)

        # add account to bank's tracked accounts
        self._accounts.append(acct)

    def get_accounts(self):
        """Print the accounts stored in the bank"""
        for acct in self._accounts:
            print(acct)

    def get_account_by_num(self, num):
        """Returns the account with the given number or None"""
        for acct in self._accounts:
            if acct.num == int(num):
                print(acct)
                return acct
        return None
