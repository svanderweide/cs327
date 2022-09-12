from cmd import PROMPT
from sys import stderr
import pickle
from Account import Account
from Bank import Bank

class CLI:
    """Display a CLI and respond to commands"""

    def __init__(self) -> None:
        """Initialize CLI variables"""

        self._account: Account = None
        self._bank: Bank = Bank()
        self._choices = {
            '1': 'open account',
            '2': 'summary',
            '3': 'select account',
            '4': 'list transactions',
            '5': 'add transaction',
            '6': 'interest and fees',
            '7': 'save',
            '8': 'load',
            '9': 'quit'
        }

    def _print_account(self) -> None:
        print("Currently selected account: ", end="")
        if self._account is None:
            print("None")
        else:
            print(self._account)

    def _print_choices(self) -> None:
        print("--------------------------------")
        self._print_account()
        [print(f"{idx}: {cmd}") for idx, cmd in self._choices.items()]
    
    def _input(self, __prompt=None) -> str:
        if __prompt:
            print(__prompt)
        print(">", end="")
        return input()

    def run(self) -> None:
        """Display command options and run REPL"""
        while(True):
            self._print_choices()
            cmd = self._input()
            if cmd == '1':
                self._add_account()
            elif cmd == '2':
                self._get_summary()
            elif cmd == '3':
                self._set_account()
            elif cmd == '4':
                self._get_transactions()
            elif cmd == '5':
                self._add_transaction()
            elif cmd == '6':
                self._add_interest()
            elif cmd == '7':
                self._save()
            elif cmd == '8':
                self._load()
            elif cmd == '9':
                self._quit()
            else:
                print("ERROR: insert a value between 1 and 9\n", file=stderr)

    def _add_account(self) -> None:
        acct_type = input("Type of account? (checking/savings)")
        acct_amnt = input("Initial deposit amount?")
        self._bank.add_account(acct_type, acct_amnt)

    def _get_summary(self) -> None:
        self._bank.get_accounts()

    def _set_account(self) -> None:
        acct_id = input("Enter account number")
        self._bank.get_account_by_id(acct_id)

    def _get_transactions(self) -> None:
        self._account.print_transactions()

    def _add_transaction(self) -> None:
        trans_amnt = input("Amount?")
        trans_date = input("Date? (YYYY-MM-DD)")
        self._account.add_transaction(trans_amnt, trans_date)

    def _add_interest(self) -> None:
        self._account.add_interest()

    def _save(self) -> None:
        with open('bank.pickle', 'wb') as file:
            pickle.dump(self._bank, file)

    def _load(self) -> None:
        with open('bank.pickle', 'rb') as file:
            self._bank = pickle.load(file)
            self._account = None

    def _quit(self) -> None:
        exit(0)

if __name__ == "__main__":

    CLI().run()
