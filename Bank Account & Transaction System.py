from datetime import datetime


class Transaction:
    """Represents a single transaction"""
    def __init__(self, transaction_type, amount, balance_after):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = datetime.now()
    
    def __str__(self):
        date_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"{date_str} | {self.transaction_type:<12} | ${self.amount:>10.2f} | Balance: ${self.balance_after:>10.2f}"


class BankAccount:
    """Represents a bank account with transaction capabilities"""
    
    account_counter = 1000  # Class variable for generating account numbers
    
    def __init__(self, account_holder, initial_deposit=0):
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1
        self.account_holder = account_holder
        self.balance = 0
        self.transaction_history = []
        self.is_active = True
        
        # Add initial deposit if provided
        if initial_deposit > 0:
            self.deposit(initial_deposit, is_initial=True)
    
    def deposit(self, amount, is_initial=False):
        """Deposit money into the account"""
        try:
            amount = float(amount)
            
            if amount <= 0:
                raise ValueError("Deposit amount must be positive")
            
            self.balance += amount
            transaction_type = "Initial Dep" if is_initial else "Deposit"
            transaction = Transaction(transaction_type, amount, self.balance)
            self.transaction_history.append(transaction)
            
            print(f"\n✓ Deposit successful!")
            print(f"  Amount deposited: ${amount:.2f}")
            print(f"  New balance: ${self.balance:.2f}")
            return True
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
            return False
    
    def withdraw(self, amount):
        """Withdraw money from the account with overdraft prevention"""
        try:
            amount = float(amount)
            
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive")
            
            # Overdraft prevention
            if amount > self.balance:
                print(f"\n✗ Insufficient funds!")
                print(f"  Requested: ${amount:.2f}")
                print(f"  Available: ${self.balance:.2f}")
                print(f"  Shortfall: ${amount - self.balance:.2f}")
                return False
            
            self.balance -= amount
            transaction = Transaction("Withdrawal", amount, self.balance)
            self.transaction_history.append(transaction)
            
            print(f"\n✓ Withdrawal successful!")
            print(f"  Amount withdrawn: ${amount:.2f}")
            print(f"  Remaining balance: ${self.balance:.2f}")
            
            # Low balance warning
            if self.balance < 100:
                print(f"  ⚠️  Warning: Low balance (${self.balance:.2f})")
            
            return True
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
            return False
    
    def show_balance(self):
        """Display current account balance"""
        print("\n" + "="*60)
        print("ACCOUNT BALANCE".center(60))
        print("="*60)
        print(f"Account Number : {self.account_number}")
        print(f"Account Holder : {self.account_holder}")
        print(f"Current Balance: ${self.balance:.2f}")
        print("="*60)
        
        if self.balance < 100:
            print("⚠️  Low Balance Warning")
        elif self.balance >= 10000:
            print("🌟 Premium Account Status")
    
    def show_transaction_history(self, limit=None):
        """Display transaction history"""
        if not self.transaction_history:
            print("\nNo transactions yet.")
            return
        
        print("\n" + "="*80)
        print("TRANSACTION HISTORY".center(80))
        print("="*80)
        print(f"Account: {self.account_number} | Holder: {self.account_holder}")
        print("-"*80)
        print(f"{'Date & Time':<20} | {'Type':<12} | {'Amount':<12} | {'Balance After'}")
        print("-"*80)
        
        # Show limited transactions if specified
        transactions = self.transaction_history[-limit:] if limit else self.transaction_history
        
        for transaction in transactions:
            print(transaction)
        
        print("-"*80)
        print(f"Total Transactions: {len(self.transaction_history)}")
        print(f"Current Balance: ${self.balance:.2f}")
        print("="*80)
    
    def get_account_summary(self):
        """Get summary statistics of the account"""
        if not self.transaction_history:
            print("\nNo transaction data available.")
            return
        
        total_deposits = sum(t.amount for t in self.transaction_history 
                            if t.transaction_type in ["Deposit", "Initial Dep"])
        total_withdrawals = sum(t.amount for t in self.transaction_history 
                               if t.transaction_type == "Withdrawal")
        
        print("\n" + "="*60)
        print("ACCOUNT SUMMARY".center(60))
        print("="*60)
        print(f"Account Number    : {self.account_number}")
        print(f"Account Holder    : {self.account_holder}")
        print(f"Current Balance   : ${self.balance:.2f}")
        print("-"*60)
        print(f"Total Deposits    : ${total_deposits:.2f}")
        print(f"Total Withdrawals : ${total_withdrawals:.2f}")
        print(f"Net Change        : ${total_deposits - total_withdrawals:.2f}")
        print(f"Total Transactions: {len(self.transaction_history)}")
        print("="*60)
    
    def __str__(self):
        return f"Account #{self.account_number} - {self.account_holder} (Balance: ${self.balance:.2f})"


class BankingSystem:
    """Main banking system to manage multiple accounts"""
    def __init__(self):
        self.accounts = {}
    
    def create_account(self, account_holder, initial_deposit=0):
        """Create a new bank account"""
        try:
            account_holder = account_holder.strip().title()
            
            if not account_holder:
                raise ValueError("Account holder name cannot be empty")
            
            if initial_deposit < 0:
                raise ValueError("Initial deposit cannot be negative")
            
            account = BankAccount(account_holder, initial_deposit)
            self.accounts[account.account_number] = account
            
            print("\n" + "="*60)
            print("✓ ACCOUNT CREATED SUCCESSFULLY!".center(60))
            print("="*60)
            print(f"Account Number: {account.account_number}")
            print(f"Account Holder: {account.account_holder}")
            print(f"Initial Balance: ${account.balance:.2f}")
            print("="*60)
            print("\n💡 Please save your account number for future transactions.")
            
            return account.account_number
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
            return None
    
    def get_account(self, account_number):
        """Retrieve account by account number"""
        try:
            account_number = int(account_number)
            
            if account_number not in self.accounts:
                print(f"\n✗ Account number {account_number} not found!")
                return None
            
            return self.accounts[account_number]
            
        except ValueError:
            print(f"\n✗ Invalid account number format!")
            return None
    
    def list_all_accounts(self):
        """Display all accounts in the system"""
        if not self.accounts:
            print("\nNo accounts in the system yet.")
            return
        
        print("\n" + "="*80)
        print("ALL BANK ACCOUNTS".center(80))
        print("="*80)
        print(f"{'Account #':<12} {'Account Holder':<30} {'Balance':<15} {'Transactions'}")
        print("-"*80)
        
        for account_number, account in sorted(self.accounts.items()):
            trans_count = len(account.transaction_history)
            print(f"{account_number:<12} {account.account_holder:<30} ${account.balance:<14.2f} {trans_count}")
        
        print("="*80)
        print(f"Total Accounts: {len(self.accounts)}")


def display_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("BANK ACCOUNT & TRANSACTION SYSTEM".center(60))
    print("="*60)
    print("1. Create New Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. View Transaction History")
    print("6. Account Summary")
    print("7. List All Accounts")
    print("8. Exit")
    print("="*60)


def main():
    """Main program loop"""
    bank = BankingSystem()
    
    print("\n🏦 Welcome to the Bank Account & Transaction System!")
    print("   Secure, Simple, and Reliable Banking")
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                print("\n--- Create New Account ---")
                holder_name = input("Enter account holder name: ")
                initial = input("Enter initial deposit amount (0 if none): $")
                
                try:
                    initial_amount = float(initial) if initial else 0
                    bank.create_account(holder_name, initial_amount)
                except ValueError:
                    print("\n✗ Invalid deposit amount!")
            
            elif choice == '2':
                print("\n--- Deposit Money ---")
                acc_num = input("Enter account number: ")
                account = bank.get_account(acc_num)
                
                if account:
                    amount = input("Enter amount to deposit: $")
                    account.deposit(amount)
            
            elif choice == '3':
                print("\n--- Withdraw Money ---")
                acc_num = input("Enter account number: ")
                account = bank.get_account(acc_num)
                
                if account:
                    amount = input("Enter amount to withdraw: $")
                    account.withdraw(amount)
            
            elif choice == '4':
                print("\n--- Check Balance ---")
                acc_num = input("Enter account number: ")
                account = bank.get_account(acc_num)
                
                if account:
                    account.show_balance()
            
            elif choice == '5':
                print("\n--- Transaction History ---")
                acc_num = input("Enter account number: ")
                account = bank.get_account(acc_num)
                
                if account:
                    limit_input = input("Show last N transactions (press Enter for all): ").strip()
                    limit = int(limit_input) if limit_input else None
                    account.show_transaction_history(limit)
            
            elif choice == '6':
                print("\n--- Account Summary ---")
                acc_num = input("Enter account number: ")
                account = bank.get_account(acc_num)
                
                if account:
                    account.get_account_summary()
            
            elif choice == '7':
                bank.list_all_accounts()
            
            elif choice == '8':
                print("\n" + "="*60)
                print("Thank you for using our Banking System!".center(60))
                print("Your money is safe with us. Have a great day!".center(60))
                print("="*60 + "\n")
                break
            
            else:
                print("\n✗ Invalid choice. Please enter a number between 1 and 8.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Exiting... Thank you for banking with us!")
            break
        except Exception as e:
            print(f"\n✗ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()