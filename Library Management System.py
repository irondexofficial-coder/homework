from datetime import datetime, timedelta


class Book:
    """Represents a book in the library"""
    
    book_id_counter = 1
    
    def __init__(self, title, author, isbn, copies=1):
        self.book_id = Book.book_id_counter
        Book.book_id_counter += 1
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = copies
        self.available_copies = copies
        self.issued_to = {}  # member_id: issue_record
    
    def is_available(self):
        """Check if book is available for borrowing"""
        return self.available_copies > 0
    
    def issue_book(self, member_id, member_name):
        """Issue book to a member"""
        if not self.is_available():
            return False, "No copies available"
        
        if member_id in self.issued_to:
            return False, "Member already has this book"
        
        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=14)  # 14 days borrowing period
        
        issue_record = {
            'member_id': member_id,
            'member_name': member_name,
            'issue_date': issue_date,
            'due_date': due_date
        }
        
        self.issued_to[member_id] = issue_record
        self.available_copies -= 1
        
        return True, issue_record
    
    def return_book(self, member_id):
        """Return book from a member"""
        if member_id not in self.issued_to:
            return False, "Book not issued to this member", None
        
        issue_record = self.issued_to.pop(member_id)
        self.available_copies += 1
        
        return_date = datetime.now()
        days_borrowed = (return_date - issue_record['issue_date']).days
        
        # Check if overdue
        is_overdue = return_date > issue_record['due_date']
        overdue_days = (return_date - issue_record['due_date']).days if is_overdue else 0
        
        return_info = {
            'days_borrowed': days_borrowed,
            'is_overdue': is_overdue,
            'overdue_days': overdue_days,
            'fine': overdue_days * 1.0 if is_overdue else 0  # $1 per day fine
        }
        
        return True, "Book returned successfully", return_info
    
    def __str__(self):
        status = f"({self.available_copies}/{self.total_copies} available)"
        return f"[ID: {self.book_id}] {self.title} by {self.author} {status}"


class Member:
    """Represents a library member"""
    
    member_id_counter = 100
    
    def __init__(self, name, email):
        self.member_id = Member.member_id_counter
        Member.member_id_counter += 1
        self.name = name
        self.email = email
        self.borrowed_books = []  # List of book_ids
        self.total_fines = 0
    
    def borrow_book(self, book_id):
        """Add book to member's borrowed list"""
        self.borrowed_books.append(book_id)
    
    def return_book(self, book_id):
        """Remove book from member's borrowed list"""
        if book_id in self.borrowed_books:
            self.borrowed_books.remove(book_id)
            return True
        return False
    
    def add_fine(self, amount):
        """Add fine to member's account"""
        self.total_fines += amount
    
    def __str__(self):
        return f"[ID: {self.member_id}] {self.name} ({self.email}) - Books: {len(self.borrowed_books)}"


class Library:
    """Main library management system"""
    
    def __init__(self, name):
        self.name = name
        self.books = {}  # book_id: Book object
        self.members = {}  # member_id: Member object
        self.isbn_index = {}  # isbn: book_id (for quick lookup)
    
    def add_book(self, title, author, isbn, copies=1):
        """Add a new book to the library"""
        try:
            title = title.strip().title()
            author = author.strip().title()
            isbn = isbn.strip()
            copies = int(copies)
            
            if copies <= 0:
                raise ValueError("Number of copies must be positive")
            
            # Check if book already exists by ISBN
            if isbn in self.isbn_index:
                existing_book_id = self.isbn_index[isbn]
                existing_book = self.books[existing_book_id]
                existing_book.total_copies += copies
                existing_book.available_copies += copies
                
                print(f"\n✓ Added {copies} more copies to existing book!")
                print(f"  {existing_book}")
                return existing_book_id
            
            book = Book(title, author, isbn, copies)
            self.books[book.book_id] = book
            self.isbn_index[isbn] = book.book_id
            
            print(f"\n✓ Book added successfully!")
            print(f"  {book}")
            return book.book_id
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
            return None
    
    def register_member(self, name, email):
        """Register a new library member"""
        try:
            name = name.strip().title()
            email = email.strip().lower()
            
            if not name or not email:
                raise ValueError("Name and email cannot be empty")
            
            member = Member(name, email)
            self.members[member.member_id] = member
            
            print(f"\n✓ Member registered successfully!")
            print(f"  {member}")
            print(f"\n💡 Member ID: {member.member_id} - Please save this for future transactions.")
            return member.member_id
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
            return None
    
    def view_available_books(self):
        """Display all available books"""
        available_books = [book for book in self.books.values() if book.is_available()]
        
        if not available_books:
            print("\n📚 No books available for borrowing at the moment.")
            return
        
        print("\n" + "="*90)
        print("AVAILABLE BOOKS".center(90))
        print("="*90)
        print(f"{'ID':<6} {'Title':<35} {'Author':<25} {'Available':<10} {'ISBN'}")
        print("-"*90)
        
        for book in sorted(available_books, key=lambda b: b.title):
            avail = f"{book.available_copies}/{book.total_copies}"
            print(f"{book.book_id:<6} {book.title:<35} {book.author:<25} {avail:<10} {book.isbn}")
        
        print("="*90)
        print(f"Total Available Books: {len(available_books)}")
    
    def view_all_books(self):
        """Display all books in the library"""
        if not self.books:
            print("\n📚 No books in the library yet.")
            return
        
        print("\n" + "="*90)
        print("ALL BOOKS IN LIBRARY".center(90))
        print("="*90)
        print(f"{'ID':<6} {'Title':<35} {'Author':<25} {'Status':<15} {'ISBN'}")
        print("-"*90)
        
        for book in sorted(self.books.values(), key=lambda b: b.title):
            status = f"{book.available_copies}/{book.total_copies} available"
            print(f"{book.book_id:<6} {book.title:<35} {book.author:<25} {status:<15} {book.isbn}")
        
        print("="*90)
        print(f"Total Books: {len(self.books)} | Total Copies: {sum(b.total_copies for b in self.books.values())}")
    
    def issue_book(self, book_id, member_id):
        """Issue a book to a member"""
        try:
            book_id = int(book_id)
            member_id = int(member_id)
            
            if book_id not in self.books:
                print(f"\n✗ Book ID {book_id} not found!")
                return False
            
            if member_id not in self.members:
                print(f"\n✗ Member ID {member_id} not found!")
                return False
            
            book = self.books[book_id]
            member = self.members[member_id]
            
            success, result = book.issue_book(member_id, member.name)
            
            if not success:
                print(f"\n✗ Cannot issue book: {result}")
                return False
            
            member.borrow_book(book_id)
            
            print("\n" + "="*70)
            print("✓ BOOK ISSUED SUCCESSFULLY!".center(70))
            print("="*70)
            print(f"Book         : {book.title}")
            print(f"Borrowed by  : {member.name} (ID: {member.member_id})")
            print(f"Issue Date   : {result['issue_date'].strftime('%Y-%m-%d %H:%M')}")
            print(f"Due Date     : {result['due_date'].strftime('%Y-%m-%d')}")
            print(f"Borrow Period: 14 days")
            print("="*70)
            print("⚠️  Please return the book on or before the due date to avoid fines.")
            
            return True
            
        except ValueError:
            print(f"\n✗ Invalid ID format!")
            return False
    
    def return_book(self, book_id, member_id):
        """Return a book from a member"""
        try:
            book_id = int(book_id)
            member_id = int(member_id)
            
            if book_id not in self.books:
                print(f"\n✗ Book ID {book_id} not found!")
                return False
            
            if member_id not in self.members:
                print(f"\n✗ Member ID {member_id} not found!")
                return False
            
            book = self.books[book_id]
            member = self.members[member_id]
            
            success, message, return_info = book.return_book(member_id)
            
            if not success:
                print(f"\n✗ Cannot return book: {message}")
                return False
            
            member.return_book(book_id)
            
            print("\n" + "="*70)
            print("✓ BOOK RETURNED SUCCESSFULLY!".center(70))
            print("="*70)
            print(f"Book         : {book.title}")
            print(f"Returned by  : {member.name} (ID: {member.member_id})")
            print(f"Days Borrowed: {return_info['days_borrowed']}")
            
            if return_info['is_overdue']:
                print(f"Status       : OVERDUE by {return_info['overdue_days']} days")
                print(f"Fine         : ${return_info['fine']:.2f}")
                member.add_fine(return_info['fine'])
                print("⚠️  Fine has been added to your account.")
            else:
                print(f"Status       : Returned on time ✓")
            
            print("="*70)
            
            return True
            
        except ValueError:
            print(f"\n✗ Invalid ID format!")
            return False
    
    def view_issued_books(self):
        """Display all currently issued books"""
        issued_books = []
        
        for book in self.books.values():
            if book.issued_to:
                for member_id, record in book.issued_to.items():
                    days_remaining = (record['due_date'] - datetime.now()).days
                    is_overdue = days_remaining < 0
                    
                    issued_books.append({
                        'book': book,
                        'member_id': member_id,
                        'member_name': record['member_name'],
                        'issue_date': record['issue_date'],
                        'due_date': record['due_date'],
                        'days_remaining': days_remaining,
                        'is_overdue': is_overdue
                    })
        
        if not issued_books:
            print("\n📚 No books are currently issued.")
            return
        
        print("\n" + "="*100)
        print("ISSUED BOOKS".center(100))
        print("="*100)
        print(f"{'Book Title':<30} {'Member':<20} {'Issue Date':<12} {'Due Date':<12} {'Status'}")
        print("-"*100)
        
        for record in sorted(issued_books, key=lambda x: x['due_date']):
            issue_str = record['issue_date'].strftime('%Y-%m-%d')
            due_str = record['due_date'].strftime('%Y-%m-%d')
            
            if record['is_overdue']:
                status = f"OVERDUE ({abs(record['days_remaining'])} days)"
            else:
                status = f"Due in {record['days_remaining']} days"
            
            print(f"{record['book'].title[:29]:<30} {record['member_name'][:19]:<20} {issue_str:<12} {due_str:<12} {status}")
        
        print("="*100)
        print(f"Total Issued Books: {len(issued_books)}")
    
    def view_member_info(self, member_id):
        """Display detailed member information"""
        try:
            member_id = int(member_id)
            
            if member_id not in self.members:
                print(f"\n✗ Member ID {member_id} not found!")
                return
            
            member = self.members[member_id]
            
            print("\n" + "="*70)
            print("MEMBER INFORMATION".center(70))
            print("="*70)
            print(f"Member ID    : {member.member_id}")
            print(f"Name         : {member.name}")
            print(f"Email        : {member.email}")
            print(f"Books Issued : {len(member.borrowed_books)}")
            print(f"Total Fines  : ${member.total_fines:.2f}")
            print("-"*70)
            
            if member.borrowed_books:
                print("CURRENTLY BORROWED BOOKS:")
                for book_id in member.borrowed_books:
                    book = self.books[book_id]
                    record = book.issued_to[member_id]
                    due_date = record['due_date'].strftime('%Y-%m-%d')
                    days_remaining = (record['due_date'] - datetime.now()).days
                    
                    status = "OVERDUE" if days_remaining < 0 else f"Due in {days_remaining} days"
                    print(f"  • {book.title} (Due: {due_date}) - {status}")
            else:
                print("No books currently borrowed.")
            
            print("="*70)
            
        except ValueError:
            print(f"\n✗ Invalid member ID format!")


def display_menu():
    """Display the main menu"""
    print("\n" + "="*70)
    print("LIBRARY MANAGEMENT SYSTEM".center(70))
    print("="*70)
    print("Book Management:")
    print("  1. Add Book")
    print("  2. View Available Books")
    print("  3. View All Books")
    print("\nMember Management:")
    print("  4. Register Member")
    print("  5. View Member Info")
    print("\nTransactions:")
    print("  6. Issue Book")
    print("  7. Return Book")
    print("  8. View Issued Books")
    print("\n  9. Exit")
    print("="*70)


def main():
    """Main program loop"""
    library = Library("Central City Library")
    
    print("\n" + "="*70)
    print(f"📚 Welcome to {library.name}!".center(70))
    print("Your Gateway to Knowledge and Learning".center(70))
    print("="*70)
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-9): ").strip()
            
            if choice == '1':
                print("\n--- Add New Book ---")
                title = input("Enter book title: ")
                author = input("Enter author name: ")
                isbn = input("Enter ISBN: ")
                copies = input("Enter number of copies: ")
                library.add_book(title, author, isbn, copies)
            
            elif choice == '2':
                library.view_available_books()
            
            elif choice == '3':
                library.view_all_books()
            
            elif choice == '4':
                print("\n--- Register New Member ---")
                name = input("Enter member name: ")
                email = input("Enter email address: ")
                library.register_member(name, email)
            
            elif choice == '5':
                print("\n--- View Member Info ---")
                member_id = input("Enter member ID: ")
                library.view_member_info(member_id)
            
            elif choice == '6':
                print("\n--- Issue Book ---")
                book_id = input("Enter book ID: ")
                member_id = input("Enter member ID: ")
                library.issue_book(book_id, member_id)
            
            elif choice == '7':
                print("\n--- Return Book ---")
                book_id = input("Enter book ID: ")
                member_id = input("Enter member ID: ")
                library.return_book(book_id, member_id)
            
            elif choice == '8':
                library.view_issued_books()
            
            elif choice == '9':
                print("\n" + "="*70)
                print("Thank you for using the Library Management System!".center(70))
                print("Happy Reading! 📚".center(70))
                print("="*70 + "\n")
                break
            
            else:
                print("\n✗ Invalid choice. Please enter a number between 1 and 9.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Exiting... Happy Reading!")
            break
        except Exception as e:
            print(f"\n✗ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()