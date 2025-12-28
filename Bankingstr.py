import streamlit as st
from datetime import datetime


class Transaction:
    """Represents a single transaction"""
    def __init__(self, transaction_type, amount, balance_after):
        self.transaction_type = transaction_type
        self.amount = amount
        self.balance_after = balance_after
        self.timestamp = datetime.now()
    
    def to_dict(self):
        return {
            'Date & Time': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'Type': self.transaction_type,
            'Amount': f"${self.amount:.2f}",
            'Balance After': f"${self.balance_after:.2f}"
        }


class BankAccount:
    """Represents a bank account with transaction capabilities"""
    
    account_counter = 1000
    
    def __init__(self, account_holder, initial_deposit=0):
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1
        self.account_holder = account_holder
        self.balance = 0
        self.transaction_history = []
        self.is_active = True
        
        if initial_deposit > 0:
            self._process_deposit(initial_deposit, is_initial=True)
    
    def _process_deposit(self, amount, is_initial=False):
        """Internal method to process deposit"""
        self.balance += amount
        transaction_type = "Initial Dep" if is_initial else "Deposit"
        transaction = Transaction(transaction_type, amount, self.balance)
        self.transaction_history.append(transaction)
    
    def deposit(self, amount):
        """Deposit money into the account"""
        try:
            amount = float(amount)
            
            if amount <= 0:
                return False, "Deposit amount must be positive"
            
            self._process_deposit(amount, is_initial=False)
            return True, f"Successfully deposited ${amount:.2f}. New balance: ${self.balance:.2f}"
            
        except ValueError as e:
            return False, str(e)
    
    def withdraw(self, amount):
        """Withdraw money from the account"""
        try:
            amount = float(amount)
            
            if amount <= 0:
                return False, "Withdrawal amount must be positive"
            
            if amount > self.balance:
                return False, f"Insufficient funds! Available: ${self.balance:.2f}, Requested: ${amount:.2f}"
            
            self.balance -= amount
            transaction = Transaction("Withdrawal", amount, self.balance)
            self.transaction_history.append(transaction)
            
            message = f"Successfully withdrew ${amount:.2f}. Remaining balance: ${self.balance:.2f}"
            if self.balance < 100:
                message += f"\n⚠️ Warning: Low balance (${self.balance:.2f})"
            
            return True, message
            
        except ValueError as e:
            return False, str(e)
    
    def get_summary(self):
        """Get account summary statistics"""
        total_deposits = sum(t.amount for t in self.transaction_history 
                            if t.transaction_type in ["Deposit", "Initial Dep"])
        total_withdrawals = sum(t.amount for t in self.transaction_history 
                               if t.transaction_type == "Withdrawal")
        
        return {
            'Account Number': self.account_number,
            'Account Holder': self.account_holder,
            'Current Balance': self.balance,
            'Total Deposits': total_deposits,
            'Total Withdrawals': total_withdrawals,
            'Net Change': total_deposits - total_withdrawals,
            'Total Transactions': len(self.transaction_history)
        }


class BankingSystem:
    """Main banking system to manage multiple accounts"""
    def __init__(self):
        self.accounts = {}
        self.accounts_by_name = {}
    
    def create_account(self, account_holder, initial_deposit=0):
        """Create a new bank account"""
        try:
            account_holder = account_holder.strip()
            
            if not account_holder:
                return None, "Account holder name cannot be empty"
            
            account_holder = " ".join(word.capitalize() for word in account_holder.split())
            initial_deposit = float(initial_deposit)
            
            if initial_deposit < 0:
                return None, "Initial deposit cannot be negative"
            
            account = BankAccount(account_holder, initial_deposit)
            self.accounts[account.account_number] = account
            
            name_key = account_holder.lower()
            if name_key not in self.accounts_by_name:
                self.accounts_by_name[name_key] = []
            self.accounts_by_name[name_key].append(account)
            
            return account, f"Account created successfully! Account Number: {account.account_number}"
            
        except ValueError as e:
            return None, str(e)
    
    def get_account(self, identifier):
        """Retrieve account by number or name"""
        if not identifier or not str(identifier).strip():
            return None, "Please enter an account number or name"
        
        identifier = str(identifier).strip()
        
        # Try account number first
        try:
            account_number = int(identifier)
            if account_number in self.accounts:
                return self.accounts[account_number], None
        except ValueError:
            pass
        
        # Search by name
        name_key = identifier.lower()
        
        # Exact match
        if name_key in self.accounts_by_name:
            accounts = self.accounts_by_name[name_key]
            if len(accounts) == 1:
                return accounts[0], None
            else:
                return None, f"Multiple accounts found for '{identifier}'. Please use account number."
        
        # Partial match
        matching_accounts = []
        for stored_name, accounts in self.accounts_by_name.items():
            if name_key in stored_name or stored_name in name_key:
                matching_accounts.extend(accounts)
        
        if matching_accounts:
            if len(matching_accounts) == 1:
                return matching_accounts[0], None
            else:
                return None, f"Multiple accounts found matching '{identifier}'. Please use account number."
        
        return None, f"No account found for '{identifier}'"
    
    def get_all_accounts(self):
        """Return all accounts as a list"""
        return sorted(self.accounts.values(), key=lambda x: x.account_number)


# Initialize session state
if 'bank' not in st.session_state:
    st.session_state.bank = BankingSystem()

# Page configuration
st.set_page_config(
    page_title="Bank Account System",
    page_icon="🏦",
    layout="wide"
)

# Title
st.title("🏦 Bank Account & Transaction System")
st.markdown("### Secure, Simple, and Reliable Banking")
st.divider()

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select Operation:",
        ["Create Account", "Deposit Money", "Withdraw Money", 
         "Check Balance", "Transaction History", "Account Summary", "All Accounts"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown("### 💡 Tips")
    st.info("You can use either account number or account holder name for transactions!")

# Main content area
if page == "Create Account":
    st.header("Create New Account")
    
    with st.form("create_account_form"):
        holder_name = st.text_input("Account Holder Name", placeholder="e.g., John Smith")
        initial_deposit = st.number_input("Initial Deposit ($)", min_value=0.0, step=10.0, format="%.2f")
        
        submitted = st.form_submit_button("Create Account", type="primary")
        
        if submitted:
            if not holder_name:
                st.error("❌ Account holder name cannot be empty!")
            else:
                account, message = st.session_state.bank.create_account(holder_name, initial_deposit)
                if account:
                    st.success(f"✅ {message}")
                    st.info(f"**Account Holder:** {account.account_holder}\n\n**Initial Balance:** ${account.balance:.2f}")
                else:
                    st.error(f"❌ {message}")

elif page == "Deposit Money":
    st.header("Deposit Money")
    
    with st.form("deposit_form"):
        identifier = st.text_input("Account Number or Name", placeholder="e.g., 1000 or John Smith")
        amount = st.number_input("Amount to Deposit ($)", min_value=0.01, step=10.0, format="%.2f")
        
        submitted = st.form_submit_button("Deposit", type="primary")
        
        if submitted:
            account, error = st.session_state.bank.get_account(identifier)
            if account:
                success, message = account.deposit(amount)
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
            else:
                st.error(f"❌ {error}")

elif page == "Withdraw Money":
    st.header("Withdraw Money")
    
    with st.form("withdraw_form"):
        identifier = st.text_input("Account Number or Name", placeholder="e.g., 1000 or John Smith")
        amount = st.number_input("Amount to Withdraw ($)", min_value=0.01, step=10.0, format="%.2f")
        
        submitted = st.form_submit_button("Withdraw", type="primary")
        
        if submitted:
            account, error = st.session_state.bank.get_account(identifier)
            if account:
                success, message = account.withdraw(amount)
                if success:
                    st.success(f"✅ {message}")
                else:
                    st.error(f"❌ {message}")
            else:
                st.error(f"❌ {error}")

elif page == "Check Balance":
    st.header("Check Balance")
    
    identifier = st.text_input("Account Number or Name", placeholder="e.g., 1000 or John Smith", key="balance_check")
    
    if st.button("Check Balance", type="primary"):
        if identifier:
            account, error = st.session_state.bank.get_account(identifier)
            if account:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Account Number", account.account_number)
                with col2:
                    st.metric("Account Holder", account.account_holder)
                with col3:
                    st.metric("Current Balance", f"${account.balance:.2f}")
                
                if account.balance < 100 and account.balance > 0:
                    st.warning("⚠️ Low Balance Warning")
                elif account.balance >= 10000:
                    st.success("🌟 Premium Account Status")
                elif account.balance == 0:
                    st.info("💡 Account has zero balance")
            else:
                st.error(f"❌ {error}")
        else:
            st.warning("Please enter an account number or name")

elif page == "Transaction History":
    st.header("Transaction History")
    
    identifier = st.text_input("Account Number or Name", placeholder="e.g., 1000 or John Smith", key="transaction_history")
    limit = st.number_input("Show last N transactions (0 for all)", min_value=0, value=0, step=1)
    
    if st.button("View History", type="primary"):
        if identifier:
            account, error = st.session_state.bank.get_account(identifier)
            if account:
                st.subheader(f"Account: {account.account_number} | Holder: {account.account_holder}")
                
                if not account.transaction_history:
                    st.info("📝 No transactions yet")
                else:
                    transactions = account.transaction_history[-limit:] if limit > 0 else account.transaction_history
                    
                    # Display as dataframe
                    import pandas as pd
                    df = pd.DataFrame([t.to_dict() for t in transactions])
                    st.dataframe(df, use_container_width=True)
                    
                    st.divider()
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Transactions", len(account.transaction_history))
                    with col2:
                        st.metric("Current Balance", f"${account.balance:.2f}")
            else:
                st.error(f"❌ {error}")
        else:
            st.warning("Please enter an account number or name")

elif page == "Account Summary":
    st.header("Account Summary")
    
    identifier = st.text_input("Account Number or Name", placeholder="e.g., 1000 or John Smith", key="account_summary")
    
    if st.button("View Summary", type="primary"):
        if identifier:
            account, error = st.session_state.bank.get_account(identifier)
            if account:
                if not account.transaction_history:
                    st.info("📝 No transaction data available")
                else:
                    summary = account.get_summary()
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Account Number", summary['Account Number'])
                        st.metric("Account Holder", summary['Account Holder'])
                        st.metric("Current Balance", f"${summary['Current Balance']:.2f}")
                    
                    with col2:
                        st.metric("Total Deposits", f"${summary['Total Deposits']:.2f}")
                        st.metric("Total Withdrawals", f"${summary['Total Withdrawals']:.2f}")
                        st.metric("Net Change", f"${summary['Net Change']:.2f}")
                    
                    st.divider()
                    st.metric("Total Transactions", summary['Total Transactions'])
            else:
                st.error(f"❌ {error}")
        else:
            st.warning("Please enter an account number or name")

elif page == "All Accounts":
    st.header("All Bank Accounts")
    
    accounts = st.session_state.bank.get_all_accounts()
    
    if not accounts:
        st.info("📝 No accounts in the system yet. Create an account to get started!")
    else:
        import pandas as pd
        
        data = []
        for account in accounts:
            data.append({
                'Account #': account.account_number,
                'Account Holder': account.account_holder,
                'Balance': f"${account.balance:.2f}",
                'Transactions': len(account.transaction_history)
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Accounts", len(accounts))
        with col2:
            total_balance = sum(acc.balance for acc in accounts)
            st.metric("Total System Balance", f"${total_balance:.2f}")

# Footer
st.divider()
st.markdown("---")
st.markdown("**🏦 Bank Account & Transaction System** | Secure, Simple, and Reliable Banking")