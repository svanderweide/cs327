"""
BankCLI module

implements GUI for Bank
"""

# library modules
import sys
import logging
from re import fullmatch
from decimal import InvalidOperation

# GUI modules
import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

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


class GUI:
    """Display a GUI and respond to user inputs"""

    def __init__(self):

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

        # main tkinter window with title
        self._window = tk.Tk()
        self._window.title("Bank")
        self._window.report_callback_exception = self._handle_exception

        # dictionary of associated frames
        self._frames: dict = {}

        # main frame
        self._frames["main"] = tk.Frame(self._window)
        self._frames["main"].grid()

        # frame for account selected
        self._frames["selected"] = tk.Frame(self._frames["main"])
        self._frames["selected"].grid(row=0, pady=10, sticky="news")

        # StringVar for selected account (named for later updating)
        self._selected_label = tk.StringVar(self._frames["selected"])
        self._selected_label.set("Selected Account: None")

        tk.Label(self._frames["selected"],
                 textvariable=self._selected_label).pack()

        # frame for command buttons
        self._frames["commands"] = tk.LabelFrame(self._frames["main"],
                                                 text="Commands")
        self._frames["commands"].grid(row=1, sticky="news",
                                      padx=10, pady=(0, 10))

        tk.Button(self._frames["commands"],
                  text="open account",
                  command=self._open_account).grid(row=0, column=0)

        tk.Button(self._frames["commands"],
                  text="add transaction",
                  command=self._add_transaction).grid(row=0, column=1)

        tk.Button(self._frames["commands"],
                  text="interest and fees",
                  command=self._interest_and_fees).grid(row=0, column=2)

        # frame for user-input entries
        self._frames["input"] = tk.LabelFrame(self._frames["main"])
        self._frames["input"].grid(row=2, pady=10)

        # frame for holding accounts and transaction frames
        self._frames["contents"] = tk.Frame(self._frames["main"])
        self._frames["contents"].grid(row=3)

        # frame for holding accounts
        self._frames["accounts"] = tk.LabelFrame(self._frames["contents"],
                                                 text="Accounts")
        self._frames["accounts"].grid(row=0, column=0, sticky="news",
                                      padx=10, pady=10)

        # listbox for holding accounts (inside accounts frame)
        self._accounts_listbox = tk.Listbox(self._frames["accounts"])
        self._accounts_listbox.pack()

        # frame for holding transactions
        self._frames["transactions"] = tk.LabelFrame(self._frames["contents"],
                                                     text="Transactions")
        self._frames["transactions"].grid(row=0, column=1, columnspan=3,
                                          sticky="news", padx=10, pady=10)

        # listbox for holding transactions (inside transactions frame)
        self._transactions_listbox = tk.Listbox(self._frames["transactions"])
        self._transactions_listbox.pack()

        self._show_accounts()

        self._window.mainloop()

    def _handle_exception(self, exception, value, traceback):
        err_msg = ("Sorry! Something unexpected happened. "
                   "If this problem persists, please contact "
                   "our support team for assistance.")
        messagebox.showerror("ERROR", err_msg)
        logging.error(f"{exception.__name__}: {repr(value)}")
        sys.exit(1)

    def _clean_input_frame(self) -> None:
        for widget in self._frames["input"].winfo_children():
            widget.destroy()

    def _update_selected_account(self) -> None:
        self._selected_label.set(f"Selected Account: {str(self._account)}")

    class ValidatingEntry(tk.Frame):
        """Entry with highlighting for validation

        constructor args:
            parent (tk Widget): container for widget
            regexp (str): regexp string for pattern matching
        """

        def __init__(self, parent, regexp, button, *args, **kwargs):

            tk.Frame.__init__(self, parent, *args, **kwargs)

            self._regexp = regexp

            self._entry = tk.Entry(self)
            self._entry.pack()
            self._entry.bind("<KeyPress>", self._validate)
            self._entry.bind("<KeyRelease>", self._validate)

            self._button: tk.Button = button

        def _validate(self, event):

            data = self._entry.get()
            if fullmatch(self._regexp, data):
                self._entry.configure(bg="lightgreen")
                self._button.configure(state="normal")
            else:
                self._entry.configure(bg="pink")
                self._button.configure(state="disabled")

        def get(self):
            """Returns value of contained tk.Entry()"""
            return self._entry.get()

    def _open_account(self) -> None:

        def open_callback() -> None:

            # adding an account cannot raise an exception
            acct = self._bank.add_account(options.get(), self._session)

            # adding a transaction can raise exceptions
            try:
                acct.add_transaction(amt_sel.get(), self._session)
            except InvalidOperation:
                err_msg = "Please try again with a valid dollar amount."
                messagebox.showwarning("WARNING", err_msg)
            except AttributeError:
                err_msg = "New account could not be created."
                messagebox.showwarning("WARNING", err_msg)
                self._clean_input_frame()
            except OverdrawError:
                err_msg = "New account cannot have negative initial balance."
                messagebox.showwarning("WARNING", err_msg)
                self._clean_input_frame()
            finally:
                self._show_accounts()

        self._clean_input_frame()

        acct_types = ["savings", "checking"]
        options = tk.StringVar(self._frames["input"])
        options.set(acct_types[0])

        button = tk.Button(self._frames["input"],
                           text="Create",
                           command=open_callback)
        button.grid(row=0, column=3)

        amt_label = tk.Label(self._frames["input"], text="Initial Deposit:")
        amt_label.grid(row=0, column=0)

        amt_sel = GUI.ValidatingEntry(self._frames["input"],
                                      r"^\d+(\.\d*)?$",
                                      button)
        amt_sel.grid(row=0, column=1)

        type_sel = tk.OptionMenu(self._frames["input"], options, *acct_types)
        type_sel.grid(row=0, column=2, padx=10)

    class SelectAccountHandler:
        """Event handler for select account buttons"""

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
                self._account.add_transaction(amt_sel.get(),
                                              self._session,
                                              date=date_sel.get_date())
            except InvalidOperation:
                err_msg = "Please try again with a valid dollar amount."
                messagebox.showwarning("WARNING", err_msg)
            except OverdrawError:
                err_msg = ("This transaction could not be completed "
                           "due to an insufficient account balance.")
                messagebox.showwarning("WARNING", err_msg)
            except TransactionLimitError:
                err_msg = ("This transaction could not be completed "
                           "because the account has reached a transaction limit.")
                messagebox.showwarning("WARNING", err_msg)
            except TransactionSequenceError as err:
                err_msg = f"New transactions must be from {err.latest_date} onward"
                messagebox.showwarning("WARNING", err_msg)
            else:
                self._clean_input_frame()
            finally:
                self._show_accounts()

        if self._account is None:
            messagebox.showwarning("WARNING", ("You must select an account"
                                               "before adding a transaction"))
        else:
            self._clean_input_frame()

            button = tk.Button(self._frames["input"],
                            text="Create",
                            command=add_callback)
            button.grid(row=2, columnspan=2, pady=(0, 10))

            amt_label = tk.Label(self._frames["input"], text="Amount:")
            amt_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))

            amt_sel = GUI.ValidatingEntry(self._frames["input"],
                                          r"^(-)?\d+(\.\d*)?$",
                                          button)
            amt_sel.grid(row=0, column=1, sticky="news", padx=(0, 10), pady=(10,0))

            date_label = tk.Label(self._frames["input"], text="Date:")
            date_label.grid(row=1, column=0, padx=(10, 0))

            date_sel = Calendar(self._frames["input"],
                                mindate=self._account.newest_date,
                                date_pattern="yyyy-mm-dd",
                                selectbackground="green",
                                showweeknumers=False,
                                firstweekday="sunday")
            date_sel.grid(row=1, column=1, pady=(10, 10), padx=(0,10))

    def _interest_and_fees(self) -> None:
        try:
            self._account.interest_and_fees(self._session)
        except AttributeError:
            err_msg = "This command requires that you first select an account."
            messagebox.showwarning("WARNING", err_msg)
        except TransactionSequenceError as err:
            err_msg = (f"Cannot apply interest and fees again "
                       f"in the month of {err.latest_date.strftime('%B')}.")
            messagebox.showwarning("WARNING", err_msg)
        else:
            logging.debug("Triggered fees and interest")
        finally:
            self._show_accounts()

if __name__ == "__main__":
    engine = create_engine(DATABASE)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    GUI()
