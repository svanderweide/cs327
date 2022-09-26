"""
BankCLI module

implements CLI for Bank interface
"""

# general
import sys
from pickle import dump, load

# required for parsing
from datetime import datetime
from decimal import Decimal, InvalidOperation

# required for BankCLI
from bank import Bank
from account import Account, OverdrawError, TransactionLimitError, TransactionSequenceError

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
        try:
            while True:
                self._print_choices()
                choice = self._parse_input()
                action = self._choices.get(choice)
                action()
        except Exception as e:
            print("Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")


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

    def _parse_input(self, prompt=None, parse=str, exception=None, reprompt=None) -> str:
        
        # get user input with input()
        if prompt:
            print(prompt)
        val = input(">")

        # check for exception in parsing
        if exception:
            try:
                # parse input string as instance of class cls
                parse(val)
            except exception:
                # print secondary prompt if unable to parse
                if reprompt:
                    print(reprompt)
                return self._parse_input(prompt, parse, exception, reprompt)
        
        return val

    def _add_account(self) -> None:
        acct_type = self._parse_input("Type of account? (checking/savings)")
        acct_amnt = self._parse_input("Initial deposit amount?",
                                      Decimal,
                                      InvalidOperation,
                                      "Please try again with a valid dollar amount.")

        acct = self._bank.add_account(acct_type)

        try:
            acct.add_transaction(acct_amnt)
        except AttributeError:
            print("Account could not be created.")
        except OverdrawError:
            print("Account cannot be created with a negative initial balance.")
            

    def _get_summary(self) -> None:
        accts = self._bank.accounts
        for acct in accts:
            print(acct)

    def _set_account(self) -> None:
        acct_num = self._parse_input("Enter account number",
                                     int,
                                     ValueError,
                                     "Please try again with a valid number.")
        self._account = self._bank.get_account(acct_num)

    def _get_transactions(self) -> None:
        try:
            transactions = sorted(self._account.transactions)
        except AttributeError:
            print("This command requires that you first select an account.")
        else:
            for transaction in transactions:
                print(transaction)

    def _add_transaction(self) -> None:
        # get amount for transaction
        trans_amt = self._parse_input("Amount?",
                                      Decimal,
                                      InvalidOperation,
                                      "Please try again with a valid dollar amount.")
        # get date for transaction
        trans_date = self._parse_input("Date? (YYYY-MM-DD)",
                                       datetime.fromisoformat,
                                       ValueError,
                                       "Please try again with a valid date in the format YYYY-MM-DD.")
        # add transaction to account (check for exceptions)
        try:
            self._account.add_transaction(trans_amt, date=trans_date)
        except AttributeError:
            print("This command requires that you first select an account.")
        except OverdrawError:
            print("This transaction could not be completed due to an insufficient account balance.")
        except TransactionLimitError:
            print("This transaction could not be completed because the account has reached a transaction limit.")
        except TransactionSequenceError as e:
            print(f"New transactions must be from {e.latest_date} onward.")


    def _interest_and_fees(self) -> None:
        try:
            self._account.interest_and_fees()
        except AttributeError:
            print("This command requires that you first select an account.")
        except TransactionSequenceError as e:
            print(f"Cannot apply interest and fees again in the month of {e.latest_date.strftime('%B')}.")


    def _save(self) -> None:
        with open("bank.pickle", "wb") as file:
            dump(self._bank, file)


    def _load(self) -> None:
        try:
            with open("bank.pickle", "rb") as file:
                self._bank = load(file)
        except FileNotFoundError:
            print("This command requires you to save the bank before loading.")
        else:
            self._account = None

    def _quit(self):
        sys.exit(0)

if __name__ == "__main__":
    CLI().run()
