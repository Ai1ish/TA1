"""
bank_system_refactored.py

A simple console banking system supporting Savings and Checking accounts.
Refactored from MP3-BankSystem-G9.py to follow PEP 8 and improve
readability, maintainability, and separation of concerns.
"""

import datetime

MENU_WIDTH = 42
SAVINGS_LATE_WITHDRAWAL_FEE = 10.0


class BankAccount:
    """Base class representing a generic bank account."""

    def __init__(self, name, initial_deposit=0):
        self.name = name
        self.balance = initial_deposit
        self.transaction_history = []
        self._record_transaction(
            f"Account created with initial balance: ${initial_deposit:.2f}"
        )

    def _record_transaction(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transaction_history.append(f"[{timestamp}] {message}")

    def deposit(self, amount):
        """Add funds to the account. Returns True on success."""
        if amount <= 0:
            print("\nDeposit amount must be positive.")
            return False

        self.balance += amount
        self._record_transaction(f"Deposited ${amount:.2f}")
        print(f"\nSuccess! Deposited ${amount:.2f}. "
              f"New balance: ${self.balance:.2f}")
        return True

    def withdraw(self, amount):
        """Remove funds from the account. Returns True on success."""
        if amount <= 0:
            print("\nWithdrawal amount must be positive.")
            return False

        if self.balance < amount:
            print("\nInsufficient funds!")
            return False

        self.balance -= amount
        self._record_transaction(f"Withdrew ${amount:.2f}")
        print(f"\nSuccess! Withdrew ${amount:.2f}. "
              f"New balance: ${self.balance:.2f}")
        return True

    def transfer(self, target_account, amount):
        """Transfer funds to another account using each account's own
        withdraw/deposit rules, so subclass limits (overdraft, minimum
        balance) are respected on both sides."""
        if amount <= 0:
            print("\nTransfer amount must be positive.")
            return False

        if not self.withdraw(amount):
            print("\nTransfer cancelled: could not withdraw funds.")
            return False

        target_account.deposit(amount)
        self._record_transaction(
            f"Transferred ${amount:.2f} to {target_account.name}"
        )
        target_account._record_transaction(
            f"Received ${amount:.2f} from {self.name}"
        )
        print(f"\nSuccess! Transferred ${amount:.2f} to "
              f"{target_account.name}.")
        return True

    def get_history(self):
        """Return the list of recorded transactions for this account."""
        return self.transaction_history


class SavingsAccount(BankAccount):
    """Bank account that earns interest and enforces a minimum balance."""

    def __init__(self, name, initial_deposit=0, interest_rate=0.03,
                 min_balance=100):
        super().__init__(name, initial_deposit)
        self.interest_rate = interest_rate
        self.min_balance = min_balance

    def withdraw(self, amount):
        if amount <= 0:
            print("\nWithdrawal amount must be positive.")
            return False

        drops_below_minimum = (self.balance - amount) < self.min_balance
        if not drops_below_minimum:
            return super().withdraw(amount)

        fee = SAVINGS_LATE_WITHDRAWAL_FEE
        print(f"\nWarning: This withdrawal drops your balance below the "
              f"minimum (${self.min_balance}). A ${fee} fee will apply.")

        if self.balance < (amount + fee):
            print("Insufficient funds to cover the withdrawal and the fee.")
            return False

        self.balance -= (amount + fee)
        self._record_transaction(
            f"Withdrew ${amount:.2f} (minimum balance fee ${fee:.2f} "
            f"applied)"
        )
        print(f"Success! Withdrew ${amount:.2f} (Fee: ${fee:.2f}). "
              f"New balance: ${self.balance:.2f}")
        return True

    def add_interest(self):
        """Apply this account's interest rate to the current balance."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        rate_pct = self.interest_rate * 100
        self._record_transaction(
            f"Interest added: ${interest:.2f} at rate {rate_pct:.1f}%"
        )
        print(f"\nInterest of ${interest:.2f} applied. "
              f"New balance: ${self.balance:.2f}")


class CheckingAccount(BankAccount):
    """Bank account that allows a limited overdraft."""

    def __init__(self, name, initial_deposit=0, overdraft_limit=50):
        super().__init__(name, initial_deposit)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= 0:
            print("\nWithdrawal amount must be positive.")
            return False

        if (self.balance + self.overdraft_limit) < amount:
            print("\nInsufficient funds, overdraft limit exceeded.")
            return False

        self.balance -= amount
        self._record_transaction(f"Withdrew ${amount:.2f}")
        if self.balance < 0:
            print(f"\nSuccess! Withdrew ${amount:.2f}. Account is "
                  f"overdrawn by ${-self.balance:.2f}")
        else:
            print(f"\nSuccess! Withdrew ${amount:.2f}. "
                  f"New balance: ${self.balance:.2f}")
        return True


def print_header(text):
    """Print a centered section header."""
    print(f"\n{text.center(57)}")
    print("_,-'\"`-._,-'\"`-._,-'\"`-._,-'\"`-._,-'\"`-._,-'\"`-._,-'\"`-._")


def prompt_positive_float(prompt_text):
    """Prompt the user for a positive float. Returns None on bad input."""
    try:
        value = float(input(prompt_text))
    except ValueError:
        print("\nInvalid amount. Please enter a valid number.")
        return None

    if value < 0:
        print("\nAmount cannot be negative.")
        return None

    return value


def get_account_from_user(accounts, prompt="\nSelect an account:"):
    """Ask the user to pick an existing account. Returns the account or
    None if the selection was invalid or no accounts exist."""
    if not accounts:
        print("\nNo accounts exist yet. Please create one first.")
        return None

    print(prompt)
    for idx, acc in enumerate(accounts):
        print(f"  {idx + 1}. {acc.name} ({type(acc).__name__})")

    try:
        choice = int(input("Enter account number: ")) - 1
    except ValueError:
        print("Please enter a valid number.")
        return None

    if 0 <= choice < len(accounts):
        return accounts[choice]

    print("Invalid selection.")
    return None


def handle_add_account(accounts):
    print_header("ADD ACCOUNT")
    name = input("Name of the user: ")
    print("\nAccount Types:")
    print("1. Savings Account")
    print("2. Checking Account")
    acc_type = input("Choose type (1-2): ")

    initial = prompt_positive_float("\nEnter initial deposit amount: $")
    if initial is None:
        return

    if acc_type == "1":
        accounts.append(SavingsAccount(name, initial))
        print(f"\nSavings Account created successfully for {name}!")
    elif acc_type == "2":
        accounts.append(CheckingAccount(name, initial))
        print(f"\nChecking Account created successfully for {name}!")
    else:
        print("\nInvalid account type selected.")


def handle_deposit_withdraw(accounts):
    print_header("DEPOSIT / WITHDRAW")
    acc = get_account_from_user(accounts)
    if acc is None:
        return

    print("\nAction:")
    print("  1. Deposit")
    print("  2. Withdraw")
    action = input("Choose action (1-2): ")

    if action not in ("1", "2"):
        print("\nInvalid action selected.")
        return

    amount = prompt_positive_float("\nEnter amount: $")
    if amount is None:
        return

    if action == "1":
        acc.deposit(amount)
    else:
        acc.withdraw(amount)


def handle_check_balance(accounts):
    print_header("CHECK BALANCE")
    acc = get_account_from_user(accounts)
    if acc:
        print(f"\nAccount Name: {acc.name}")
        print(f"Account Type: {type(acc).__name__}")
        print(f"Current Balance: ${acc.balance:.2f}")


def handle_add_interest(accounts):
    print_header("ADD SAVINGS INTEREST")
    acc = get_account_from_user(accounts)
    if not acc:
        return
    if isinstance(acc, SavingsAccount):
        acc.add_interest()
    else:
        print(f"Error: {acc.name} has a {type(acc).__name__}. "
              f"Only Savings Accounts earn interest.")


def handle_transfer(accounts):
    print_header("SEND / TRANSFER FUNDS")
    if len(accounts) < 2:
        print("\nYou need at least 2 accounts to make a transfer.")
        return

    from_acc = get_account_from_user(accounts, "\nSelect the account to "
                                                "transfer FROM:")
    if not from_acc:
        return

    to_acc = get_account_from_user(accounts, "\nSelect the account to "
                                              "transfer TO:")
    if not to_acc:
        return

    if from_acc is to_acc:
        print("Cannot transfer to the same account.")
        return

    amount = prompt_positive_float("\nEnter amount to transfer: $")
    if amount is None:
        return

    from_acc.transfer(to_acc, amount)


def handle_view_history(accounts):
    print_header("VIEW TRANSACTION HISTORY")
    acc = get_account_from_user(accounts)
    if not acc:
        return

    print(f"\nTransaction History for {acc.name}:")
    history = acc.get_history()
    if not history:
        print("No transactions yet.")
    else:
        for entry in history:
            print(entry)


def handle_exit():
    """Return True if the user confirms they want to exit."""
    exit_choice = input("\nAre you sure you want to exit? (y/n): ").lower()
    if exit_choice == "y":
        print("Thank you for using Maya Bank. Goodbye!")
        return True
    if exit_choice == "n":
        print("Returning to main menu...")
    else:
        print("Invalid choice, returning to main menu.")
    return False


MENU_ACTIONS = {
    "1": handle_add_account,
    "2": handle_deposit_withdraw,
    "3": handle_check_balance,
    "4": handle_add_interest,
    "5": handle_transfer,
    "6": handle_view_history,
}


def print_menu():
    print("\n╔────────────────────────────────────────╗")
    print("│          Welcome to Maya Bank          │")
    print("│                                        │")
    print("│  1. Add Account                        │")
    print("│  2. Deposit / Withdraw                 │")
    print("│  3. Check Balance                      │")
    print("│  4. Add Savings Interest               │")
    print("│  5. Send / Transfer Funds              │")
    print("│  6. View Transaction History           │")
    print("│  7. Exit                               │")
    print("╚────────────────────────────────────────╝")


def main():
    accounts = []

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ")

        if choice == "7":
            if handle_exit():
                break
            continue

        action = MENU_ACTIONS.get(choice)
        if action:
            action(accounts)
        else:
            print("\nInvalid Choice! Please enter a number between 1 "
                  "and 7.")


if __name__ == "__main__":
    main()
