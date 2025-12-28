class Expense:
    """Represents a single expense entry"""
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description
    
    def __str__(self):
        return f"{self.category}: ${self.amount:.2f} - {self.description}"


class ExpenseTracker:
    """Main expense tracker and budget manager"""
    def __init__(self):
        self.expenses = []
        self.monthly_budget = 0
        self.categories = set()
    
    def add_expense(self, amount, category, description):
        """Add a new expense to the tracker"""
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            expense = Expense(amount, category.strip().title(), description.strip())
            self.expenses.append(expense)
            self.categories.add(expense.category)
            
            print(f"\n✓ Expense added successfully: {expense}")
            self._check_budget_alert()
            
        except ValueError as e:
            print(f"\n✗ Error: Invalid amount. {e}")
    
    def view_expenses(self):
        """Display all expenses"""
        if not self.expenses:
            print("\nNo expenses recorded yet.")
            return
        
        print("\n" + "="*60)
        print("ALL EXPENSES".center(60))
        print("="*60)
        
        for i, expense in enumerate(self.expenses, 1):
            print(f"{i}. {expense}")
        
        print("="*60)
    
    def calculate_total(self):
        """Calculate and display total spending"""
        total = sum(expense.amount for expense in self.expenses)
        print(f"\n💰 Total Spending: ${total:.2f}")
        
        if self.monthly_budget > 0:
            remaining = self.monthly_budget - total
            percentage = (total / self.monthly_budget) * 100
            
            print(f"📊 Budget: ${self.monthly_budget:.2f}")
            print(f"📈 Budget Used: {percentage:.1f}%")
            
            if remaining >= 0:
                print(f"✓ Remaining: ${remaining:.2f}")
            else:
                print(f"⚠ Over Budget by: ${abs(remaining):.2f}")
        
        return total
    
    def set_budget(self, amount):
        """Set monthly budget"""
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Budget must be positive")
            
            self.monthly_budget = amount
            print(f"\n✓ Monthly budget set to: ${self.monthly_budget:.2f}")
            self._check_budget_alert()
            
        except ValueError as e:
            print(f"\n✗ Error: Invalid budget amount. {e}")
    
    def _check_budget_alert(self):
        """Check if budget is exceeded and alert user"""
        if self.monthly_budget > 0:
            total = sum(expense.amount for expense in self.expenses)
            
            if total > self.monthly_budget:
                overspend = total - self.monthly_budget
                print(f"\n⚠️  BUDGET ALERT: You've exceeded your budget by ${overspend:.2f}!")
            elif total >= self.monthly_budget * 0.9:
                percentage = (total / self.monthly_budget) * 100
                print(f"\n⚠️  Warning: You've used {percentage:.1f}% of your budget.")
    
    def category_summary(self):
        """Display spending summary by category"""
        if not self.expenses:
            print("\nNo expenses to summarize.")
            return
        
        category_totals = {}
        for expense in self.expenses:
            category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
        
        total_spending = sum(category_totals.values())
        
        print("\n" + "="*60)
        print("CATEGORY-WISE SUMMARY".center(60))
        print("="*60)
        
        # Sort categories by spending (highest first)
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        for category, amount in sorted_categories:
            percentage = (amount / total_spending) * 100
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            
            print(f"{category:20s} ${amount:8.2f} ({percentage:5.1f}%) {bar}")
        
        print("="*60)
        print(f"{'TOTAL':20s} ${total_spending:8.2f} (100.0%)")
        print("="*60)


def display_menu():
    """Display the main menu"""
    print("\n" + "="*60)
    print("SMART EXPENSE TRACKER & BUDGET MANAGER".center(60))
    print("="*60)
    print("1. Add Expense")
    print("2. View All Expenses")
    print("3. Calculate Total Spending")
    print("4. Set Monthly Budget")
    print("5. Category-wise Summary")
    print("6. Exit")
    print("="*60)


def main():
    """Main program loop"""
    tracker = ExpenseTracker()
    
    print("\n🎯 Welcome to Smart Expense Tracker!")
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                print("\n--- Add New Expense ---")
                amount = input("Enter amount: $")
                category = input("Enter category (e.g., Food, Transport, Entertainment): ")
                description = input("Enter description: ")
                tracker.add_expense(amount, category, description)
            
            elif choice == '2':
                tracker.view_expenses()
            
            elif choice == '3':
                tracker.calculate_total()
            
            elif choice == '4':
                budget = input("\nEnter monthly budget: $")
                tracker.set_budget(budget)
            
            elif choice == '5':
                tracker.category_summary()
            
            elif choice == '6':
                print("\n👋 Thank you for using Smart Expense Tracker!")
                print("💡 Stay on budget and track your expenses wisely!\n")
                break
            
            else:
                print("\n✗ Invalid choice. Please enter a number between 1 and 6.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Exiting... Goodbye!")
            break
        except Exception as e:
            print(f"\n✗ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()