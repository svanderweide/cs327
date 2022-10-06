"""
BankCLI module

implements GUI for Bank
"""

# library modules
from decimal import InvalidOperation
import sys
import logging
from pickle import dump, load

# GUI modules
import tkinter as tk
from tkinter import messagebox

# custom modules
from bank import Bank
from account import Account, OverdrawError, TransactionLimitError, TransactionSequenceError

# configure the logging module
logging.basicConfig(filename="bank.log",
                    level=logging.DEBUG,
                    format="%(asctime)s|%(levelname)s|%(message)s",
                    datefmt="%Y-%m-%d %I:%M:%S")


class GUI:
    """Display a GUI and respond to user inputs"""

    def __init__(self):

        self._account: Account = None
        self._bank: Bank = Bank()

        # main tkinter window with title
        self._window = tk.Tk()
        self._window.title("Bank")

        # dictionary of associated frames
        self._frames: dict = {}

        # frame for account selected
        self._frames["selected"] = tk.Frame(self._window)
        self._frames["selected"].grid(row=0, pady=10)

        # StringVar for selected account (named for later updating)
        self._selected_label = tk.StringVar(self._frames["selected"], "Selected Account: None")

        tk.Label(self._frames["selected"], textvariable=self._selected_label).pack()

        # frame for command buttons
        self._frames["commands"] = tk.LabelFrame(self._window, text="Commands")
        self._frames["commands"].grid(row=1, sticky="news", padx=10)
        
        tk.Button(self._frames["commands"],
                  text="open account",
                  command=self._open_account).grid(row=0, column=0)

        tk.Button(self._frames["commands"],
                  text="add transaction",
                  command=self._add_transaction).grid(row=0, column=1)
        
        tk.Button(self._frames["commands"],
                  text="interest and fees",
                  command=self._interest_and_fees).grid(row=0, column=2)
        
        tk.Button(self._frames["commands"],
                  text="save",
                  command=self._save).grid(row=0, column=3)
        
        tk.Button(self._frames["commands"],
                  text="load",
                  command=self._load).grid(row=0, column=4)

        # frame for user-input entries
        self._frames["input"] = tk.LabelFrame(self._window)
        self._frames["input"].grid(row=2, pady=10)
        
        # frame for holding accounts and transaction frames
        self._frames["contents"] = tk.Frame(self._window)
        self._frames["contents"].grid(row=3)

        # frame for holding accounts
        self._frames["accounts"] = tk.LabelFrame(self._frames["contents"], text="Accounts")
        self._frames["accounts"].grid(row=0, column=0, sticky="news", padx=10, pady=10)

        # listbox for holding accounts (inside accounts frame)
        self._accounts_listbox = tk.Listbox(self._frames["accounts"])
        self._accounts_listbox.pack()

        # frame for holding transactions
        self._frames["transactions"] = tk.LabelFrame(self._frames["contents"], text="Transactions")
        self._frames["transactions"].grid(row=0, column=1, columnspan=3, sticky="news", padx=10, pady=10)
        
        # listbox for holding transactions (inside transactions frame)
        self._transactions_listbox = tk.Listbox(self._frames["transactions"])
        self._transactions_listbox.pack()

        self._window.mainloop()


    def _update_selected_account(self) -> None:
        self._selected_label.set(f"Selected Account: {str(self._account)}")


    def _open_account(self) -> None:

        def open_callback() -> None:

            # adding an account cannot raise an exception
            acct = self._bank.add_account(options.get())

            # adding a transaction can raise exceptions
            try:
                acct.add_transaction(amt_sel.get())
            except InvalidOperation:
                err_msg = "Please try again with a valid dollar amount."
                messagebox.showwarning("ERROR", err_msg)
            except AttributeError:
                err_msg = "New account could not be created."
                messagebox.showwarning("ERROR", err_msg)
            except OverdrawError:
                err_msg = "New account cannot have negative initial balance."
                messagebox.showwarning("ERROR", err_msg)
            finally:
                # clean up the input frame
                for widget in self._frames["input"].winfo_children():
                    widget.destroy()
                self._show_accounts()

        acct_types = ["savings", "checking"]
        options = tk.StringVar(self._frames["input"])
        options.set(acct_types[0])

        amt_label = tk.Label(self._frames["input"], text="Initial Deposit:")
        amt_label.grid(row=0, column=0)

        amt_sel = tk.Entry(self._frames["input"])
        amt_sel.grid(row=0, column=1)

        type_sel = tk.OptionMenu(self._frames["input"], options, *acct_types)
        type_sel.grid(row=0, column=2, padx=10)

        button = tk.Button(self._frames["input"],
                           text="Create",
                           command=open_callback)
        button.grid(row=0, column=3)

    class SelectAccountHandler:

        def __init__(self, gui, acct) -> None:
            self._gui = gui
            self._acct = acct
        
        def __call__(self) -> None:
            self._gui._account = self._acct
            self._gui._update_selected_account()
            self._gui._show_transactions()

    def _show_accounts(self) -> None:

        self._update_selected_account()

        for acct in self._accounts_listbox.winfo_children():
            acct.destroy()

        for acct in self._bank.accounts:
            tk.Button(self._accounts_listbox,
                      text=str(acct),
                      command=GUI.SelectAccountHandler(self, acct),
                      bg="white").grid(column=0, sticky="nesw")
        
        if self._account is not None: 
            self._show_transactions()

    def _show_transactions(self) -> None:
        
        for trans in self._transactions_listbox.winfo_children():
            trans.destroy()

        for trans in sorted(self._account.transactions):
            trans_str = str(trans)
            col = "red" if "$-" in trans_str else "green"
            tk.Label(self._transactions_listbox,
                     text=trans_str,
                     fg=col,
                     bg="white").grid(sticky="nws")

    def _add_transaction(self) -> None:
        
        def add_callback() -> None:

            # adding a transaction can raise exceptions
            try:
                self._account.add_transaction(amt_sel.get(), date=date_sel.get())
            except InvalidOperation:
                err_msg = "Please try again with a valid dollar amount."
                messagebox.showwarning("ERROR", err_msg)
            except AttributeError:
                err_msg = "This utility requires that you first select an account."
                messagebox.showwarning("ERROR", err_msg)
            except OverdrawError:
                err_msg = "This transaction could not be completed due to an insufficient account balance."
                messagebox.showwarning("ERROR", err_msg)
            except TransactionLimitError:
                err_msg = "This transaction could not be completed because the account has reached a transaction limit."
                messagebox.showwarning("ERROR", err_msg)
            except TransactionSequenceError as e:
                err_msg = f"New transactions must be from {e.latest_date} onward"
                messagebox.showwarning("ERROR", err_msg)
            else:
                # clean up the input frame
                for widget in self._frames["input"].winfo_children():
                    widget.destroy()
            finally:
                self._show_accounts()

        amt_label = tk.Label(self._frames["input"], text="Amount:")
        amt_label.grid(row=0, column=0)

        amt_sel = tk.Entry(self._frames["input"])
        amt_sel.grid(row=0, column=1)

        date_label = tk.Label(self._frames["input"], text="Date:")
        date_label.grid(row=1, column=0)

        date_sel = tk.Entry(self._frames["input"])
        date_sel.grid(row=1, column=1)

        button = tk.Button(self._frames["input"],
                           text="Create",
                           command=add_callback)
        button.grid(row=2, columnspan=2)


    def _interest_and_fees(self) -> None:
        
        def open_callback() -> None:

            # adding an account cannot raise an exception
            acct = self._bank.add_account(options.get())

            # adding a transaction can raise exceptions
            try:
                acct.add_transaction(amt_sel.get())
            except AttributeError:
                err_msg = "New account could not be created"
                messagebox.showwarning("ERROR", err_msg)
            except OverdrawError:
                err_msg = "New account cannot have negative initial balance"
                messagebox.showwarning("ERROR", err_msg)
            finally:
                # clean up the input frame
                for widget in self._frames["input"].winfo_children():
                    widget.destroy()
                self._show_accounts()

        acct_types = ["savings", "checking"]
        options = tk.StringVar(self._frames["input"])
        options.set(acct_types[0])

        amt_label = tk.Label(self._frames["input"], text="Initial Deposit:")
        amt_label.grid(row=0, column=0)

        amt_sel = tk.Entry(self._frames["input"])
        amt_sel.grid(row=0, column=1)

        type_sel = tk.OptionMenu(self._frames["input"], options, *acct_types)
        type_sel.grid(row=0, column=2, padx=10)

        button = tk.Button(self._frames["input"],
                           text="Create",
                           command=open_callback)
        button.grid(row=0, column=3)


    def _save(self) -> None:
        with open("bank.pickle", "wb") as file:
            dump(self._bank, file)
        logging.debug("Saved to bank.pickle")


    def _load(self) -> None:
        try:
            with open("bank.pickle", "rb") as file:
                self._bank = load(file)
        except FileNotFoundError:
            print("This command requires you to save the bank before loading.")
        else:
            self._account = None
            logging.debug("Loaded from bank.pickle")
        self._show_accounts()

if __name__ == "__main__":
    GUI()
