import pickle
from Account import Account
from Bank import Bank

def get_input():
    print(">", end='')
    return input()

def print_menu(acct):
    
    COMMANDS = ["open account", "summary", "select account",
                "list transactions", "add transaction",
                "interest and fees", "save", "load", "quit"]
    
    print("--------------------------------")
    print("Currently selected account: ", end="")
    print("None") if acct is None else print(acct)
    [print(f"{i}: {cmd}") for i, cmd in zip(range(1,10), COMMANDS)]

if __name__ == "__main__":
    
    acct: Account = None
    bank = Bank()

    while(True):
        
        print_menu(acct)
        cmd = get_input()

        match cmd:
            case '1':
                print("Type of account? (checking/savings)")
                type = get_input()
                print("Initial deposit amount?")
                amount = get_input()
                bank.add_account(type, amount)
            case '2':
                bank.get_accounts()
            case '3':
                print("Enter account number")
                num = get_input()
                acct = bank.get_account_by_num(num)
            case '4':
                acct.get_transactions()
            case '5':
                print("Amount?")
                amount = get_input()
                print("Date? (YYYY-MM-DD)")
                date = get_input()
                acct.add_transaction(amount, date)
            case '6':
                pass
            case '7':
                pass
            case '8':
                pass
            case '9':
                break
            case _:
                print(f"ERROR: input must be integer in [1, 9]")
