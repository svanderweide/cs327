"""
BankCLI module

implements CLI for Bank interface
"""

# library modules
import sys
import logging
from decimal import Decimal, InvalidOperation
from datetime import datetime

# SQL modules
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

# custom modules
from db import Base, DATABASE
from bank import Bank
from account import Account, OverdrawError, TransactionLimitError, TransactionSequenceError

# configure the logging module
logging.basicConfig(filename="bank.log",
                    level=logging.DEBUG,
                    format="%(asctime)s|%(levelname)s|%(message)s",
                    datefmt="%Y-%m-%d %I:%M:%S")


class CLI:
    """Display a CLI and respond to commands"""

    def __init__(self) -> None:

        self._session = Session()

        self._bank: Bank = self._session.query(Bank).first()
        if self._bank is None:
            self._bank = Bank()
            self._session.add(self._bank)
            self._session.commit()
            logging.debug("Saved to bank.db")
        else:
            logging.debug("Loaded from bank.db")

        self._account: Account = None

        self._choices = {
            "1": self._add_account,
            "2": self._get_summary,
            "3": self._set_account,
            "4": self._get_transactions,
            "5": self._add_transaction,
            "6": self._interest_and_fees,
            "7": self._quit
        }

        self._run()

    def _run(self) -> None:
        """Display command options and run REPL"""
        try:
            while True:
                self._print_choices()
                choice = self._parse_input()
                action = self._choices.get(choice)
                action()
        except Exception as err:
            print("Sorry! Something unexpected happened. "
                  "If this problem persists please contact "
                  "our support team for assistance.")
            logging.error(f"{type(err).__name__}: {repr(str(err))}")

    def _print_choices(self) -> None:
        print("--------------------------------")
        print(f"Currently selected account: {self._account}")
        print("Enter command")
        print("1: open account\n"
              "2: summary\n"
              "3: select account\n"
              "4: list transactions\n"
              "5: add transaction\n"
              "6: interest and fees\n"
              "7: quit")

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

        acct = self._bank.add_account(acct_type, self._session)

        try:
            acct.add_transaction(acct_amnt, self._session)
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
                                       ("Please try again with a valid date "
                                        "in the format YYYY-MM-DD."))
        # add transaction to account (check for exceptions)
        try:
            self._account.add_transaction(trans_amt, self._session, date=trans_date)
        except AttributeError:
            print("This command requires that you first select an account.")
        except OverdrawError:
            print("This transaction could not be completed "
                  "due to an insufficient account balance.")
        except TransactionLimitError:
            print("This transaction could not be completed "
                  "because the account has reached a transaction limit.")
        except TransactionSequenceError as err:
            print(f"New transactions must be from {err.latest_date} onward.")


    def _interest_and_fees(self) -> None:
        try:
            self._account.interest_and_fees(self._session)
        except AttributeError:
            print("This command requires that you first select an account.")
        except TransactionSequenceError as err:
            print(f"Cannot apply interest and fees again "
                  f"in the month of {err.latest_date.strftime('%B')}.")
        else:
            logging.debug("Triggered fees and interest")

    def _quit(self):
        sys.exit(0)

if __name__ == "__main__":
    engine = create_engine(DATABASE)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    CLI()
