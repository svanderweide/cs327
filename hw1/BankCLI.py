import pickle
from Account import Account
from Bank import Bank

def get_input(prompt=""):
    """
    Get user-input as a string
    
    Args:
        get_input: string to be displayed on line before '>'
    """
    if (prompt != ""):
        print(prompt)
    print(">", end="")
    return input()

def print_menu(acct):
    """Print the command menu"""

    COMMANDS = ["open account", "summary", "select account",
                "list transactions", "add transaction",
                "interest and fees", "save", "load", "quit"]
    
    print("--------------------------------")
    print("Currently selected account: ", end="")
    print("None") if acct is None else print(acct)
    [print(f"{i}: {cmd}") for i, cmd in enumerate(COMMANDS, start=1)]

if __name__ == "__main__":
    
    acct: Account = None
    bank = Bank()

    while(True):
        
        print_menu(acct)
        cmd = get_input()

        match cmd:
            case '1':
                # open new account
                type = get_input("Type of account? (checking/savings)")
                amount = get_input("Initial deposit amount?")
                bank.add_account(type, amount)
            case '2':
                # list accounts
                bank.get_accounts()
            case '3':
                # select account
                num = get_input("Enter account number")
                acct = bank.get_account_by_num(num)
            case '4':
                # list transactions for account selected
                acct.get_transactions()
            case '5':
                # add new transaction to account selected
                amount = get_input("Amount?")
                date = get_input("Date? (YYYY-MM-DD)")
                acct.add_transaction(amount, date)
            case '6':
                # add interest/fees for account selected
                acct.add_interest()
            case '7':
                # save bank with 'pickle' module
                pickle.dump(bank, 'bank.pickle')
                pass
            case '8':
                # load bank with 'pickle' module
                bank = pickle.load('bank.pickle')
                pass
            case '9':
                # quit the CLI
                break
            case _:
                print(f"ERROR: input must be integer in [1, 9]")
