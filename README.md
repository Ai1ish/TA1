# Maya Bank

A simple console-based banking system written in Python. The program demonstrates object-oriented programming through a generic bank account class and specialized Savings and Checking account types.

## Features

- Create Savings and Checking accounts
- Make deposits and withdrawals
- View account balances
- Transfer money between accounts
- View transaction history with timestamps
- Add interest to Savings accounts
- Apply a minimum-balance fee to certain Savings withdrawals
- Allow Checking accounts to use a limited overdraft
- Validate invalid amounts, account selections, and menu choices

## Account Types

### Savings Account

- Default interest rate: 3%
- Default minimum balance: `$100`
- A `$10` fee is applied when a withdrawal lowers the balance below the minimum and the account can cover the fee

### Checking Account

- Default overdraft limit: `$50`
- Withdrawals are allowed while the account remains within the overdraft limit

## Requirements

- Python 3.8 or newer

No external packages are required.

## Running the Program

Open a terminal in this project folder and run:

```bash
python bank_system.py
```

The program displays a menu with options for creating accounts, managing money, transferring funds, checking balances, viewing transaction history, and exiting.

## Project Files

- `bank_system.py` - Current console banking application.
- `bank_system_refactored.py` - Refactored version with improved formatting, constants, documentation, and return values for account operations.
- `TA1.py` - Original project file.

## Example Workflow

1. Choose **Add Account** from the menu.
2. Enter an account holder name and select Savings or Checking.
3. Enter an initial deposit.
4. Use the menu to deposit, withdraw, transfer funds, add Savings interest, or view the transaction history.

## Notes

Account data is stored in memory only. Closing the program clears all accounts and transaction history; no database or permanent file storage is currently used.
