"""
BankCLI module

implements CLI for Bank interface
"""

import sys
from pickle import dump, load
from account import Account
from bank import Bank

class CLI:
    """Display a CLI and respond to commands"""

    def __init__(self) -> None:
        self._account: Account = None
        self._bank: Bank = Bank()
        self._choices = {
            "1": self._add_account,
            "2": self._get_summary,
            "3": self._set_account,
            "4": self._get_transactions,
            "5": self._add_transaction,
            "6": self._interest_and_fees,
            "7": self._save,
            "8": self._load,
            "9": self._quit
        }

    def run(self) -> None:
        """Display command options and run REPL"""
        while True:
            self._print_choices()
            choice = self._input()
            action = self._choices.get(choice)
            if action:
                action()
            else:
                print(f"{choice} is not a valid choice\n")

    def _print_account(self) -> None:
        print("Currently selected account: ", end="")
        if self._account is None:
            print("None")
        else:
            print(self._account)

    def _print_choices(self) -> None:
        print("--------------------------------")
        self._print_account()
        print("Enter command")
        print("1: open account\n"
              "2: summary\n"
              "3: select account\n"
              "4: list transactions\n"
              "5: add transaction\n"
              "6: interest and fees\n"
              "7: save\n"
              "8: load\n"
              "9: quit")

    def _input(self, __prompt=None) -> str:
        if __prompt:
            print(__prompt)
        print(">", end="")
        return input()

    def _add_account(self) -> None:
        acct_type = self._input("Type of account? (checking/savings)")
        acct_amnt = self._input("Initial deposit amount?")
        acct = self._bank.add_account(acct_type)
        acct.add_transaction(acct_amnt)

    def _get_summary(self) -> None:
        accts = self._bank.accounts
        for acct in accts:
            print(acct)

    def _set_account(self) -> None:
        acct_num = self._input("Enter account number")
        self._account = self._bank.get_account(int(acct_num))

    def _get_transactions(self) -> None:
        try:
            transactions = sorted(self._account.transactions)
        except AttributeError:
            print("This command requires that you first select an account.")
        else:
            for transaction in transactions:
                print(transaction)

    def _add_transaction(self) -> None:
        trans_amnt = self._input("Amount?")
        trans_date = self._input("Date? (YYYY-MM-DD)")
        try:
            self._account.add_transaction(trans_amnt, date=trans_date)
        except AttributeError:
            print("This command requires that you first select an account.")

    def _interest_and_fees(self) -> None:
        self._account.interest_and_fees()

    def _save(self) -> None:
        with open("bank.pickle", "wb") as file:
            dump(self._bank, file)

    def _load(self) -> None:
        with open("bank.pickle", "rb") as file:
            self._bank = load(file)
        self._account = None

    def _quit(self):
        sys.exit(0)

if __name__ == "__main__":
    CLI().run()
