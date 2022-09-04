import datetime
from Account import Account, Savings, Checking

class Bank:

    def __init__(self):
        self.accounts: Account = []
        self.max_account = 1
    
    def add_account(self, type, initial_amt):
        
        if type == "savings":
            acct = Savings(self.max_account)
        else:
            acct = Checking(self.max_account)
        self.max_account += 1
        
        date = datetime.date.today().isoformat()
        acct.add_transaction(initial_amt, date)

        self.accounts.append(acct)

    def get_accounts(self):
        for acct in self.accounts:
            print(acct)

    def get_account_by_num(self, num):
        for acct in self.accounts:
            if acct.num == int(num):
                print(acct)
                return acct
        return None
