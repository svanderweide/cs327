import datetime
from Account import Account, Savings, Checking

class Bank:

    def __init__(self):
        self._accounts: Account = []
        self._max_account = 1
    
    def add_account(self, type, initial_amt):
        
        if type == "savings":
            acct = Savings(self._max_account)
        else:
            acct = Checking(self._max_account)
        self._max_account += 1
        
        date = datetime.date.today().isoformat()
        acct.add_transaction(initial_amt, date)

        self._accounts.append(acct)

    def get_accounts(self):
        for acct in self._accounts:
            print(acct)

    def get_account_by_num(self, num):
        for acct in self._accounts:
            if acct.num == int(num):
                print(acct)
                return acct
        return None
