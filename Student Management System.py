class Student:
    """Represents a student with their details and marks"""
    def __init__(self, student_id, name, age):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.marks = {}  # subject: marks dictionary
    
    def add_marks(self, subject, marks):
        """Add marks for a specific subject"""
        if 0 <= marks <= 100:
            self.marks[subject] = marks
            return True
        return False
    
    def calculate_average(self):
        """Calculate average marks across all subjects"""
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)
    
    def calculate_grade(self):
        """Calculate grade based on average marks"""
        avg = self.calculate_average()
        if avg >= 90:
            return 'A+'
        elif avg >= 80:
            return 'A'
        elif avg >= 70:
            return 'B'
        elif avg >= 60:
            return 'C'
        elif avg >= 50:
            return 'D'
        else:
            return 'F'
    
    def __str__(self):
        return f"ID: {self.student_id} | Name: {self.name} | Age: {self.age}"


class StudentManagementSystem:
    """Main system to manage all students"""
    def __init__(self):
        self.students = {}  # student_id: Student object
    
    def add_student(self, student_id, name, age):
        """Add a new student to the system"""
        try:
            if student_id in self.students:
                print(f"\n✗ Error: Student ID '{student_id}' already exists!")
                return False
            
            age = int(age)
            if age < 5 or age > 100:
                raise ValueError("Age must be between 5 and 100")
            
            student = Student(student_id, name.strip().title(), age)
            self.students[student_id] = student
            print(f"\n✓ Student added successfully!")
            print(f"   {student}")
            return True
            
        except ValueError as e:
            print(f"\n✗ Error: Invalid age. {e}")
            return False
    
    def add_student_marks(self, student_id, subject, marks):
        """Add marks for a student in a specific subject"""
        try:
            if student_id not in self.students:
                print(f"\n✗ Error: Student ID '{student_id}' not found!")
                return False
            
            marks = float(marks)
            student = self.students[student_id]
            
            if student.add_marks(subject.strip().title(), marks):
                print(f"\n✓ Marks added successfully!")
                print(f"   {student.name} - {subject.title()}: {marks}")
                return True
            else:
                print(f"\n✗ Error: Marks must be between 0 and 100")
                return False
                
        except ValueError:
            print(f"\n✗ Error: Invalid marks value")
            return False
    
    def search_student(self, student_id):
        """Search and display student by ID"""
        if student_id not in self.students:
            print(f"\n✗ Student ID '{student_id}' not found!")
            return None
        
        student = self.students[student_id]
        self._display_student_details(student)
        return student
    
    def display_student_report(self, student_id):
        """Display detailed report for a student"""
        if student_id not in self.students:
            print(f"\n✗ Student ID '{student_id}' not found!")
            return
        
        student = self.students[student_id]
        
        print("\n" + "="*70)
        print("STUDENT REPORT".center(70))
        print("="*70)
        print(f"Student ID    : {student.student_id}")
        print(f"Name          : {student.name}")
        print(f"Age           : {student.age}")
        print("-"*70)
        
        if student.marks:
            print("SUBJECT-WISE MARKS:")
            print("-"*70)
            print(f"{'Subject':<30} {'Marks':<10} {'Grade'}")
            print("-"*70)
            
            for subject, marks in sorted(student.marks.items()):
                grade = self._get_grade_for_marks(marks)
                print(f"{subject:<30} {marks:<10.1f} {grade}")
            
            print("-"*70)
            avg = student.calculate_average()
            overall_grade = student.calculate_grade()
            print(f"{'AVERAGE':<30} {avg:<10.2f} {overall_grade}")
            print("="*70)
        else:
            print("No marks recorded yet.")
            print("="*70)
    
    def _get_grade_for_marks(self, marks):
        """Helper function to get grade for specific marks"""
        if marks >= 90:
            return 'A+'
        elif marks >= 80:
            return 'A'
        elif marks >= 70:
            return 'B'
        elif marks >= 60:
            return 'C'
        elif marks >= 50:
            return 'D'
        else:
            return 'F'
    
    def _display_student_details(self, student):
        """Helper function to display student details"""
        print("\n" + "="*70)
        print(student)
        if student.marks:
            print(f"Subjects: {', '.join(student.marks.keys())}")
            print(f"Average Marks: {student.calculate_average():.2f}")
            print(f"Grade: {student.calculate_grade()}")
        else:
            print("No marks recorded yet.")
        print("="*70)
    
    def display_all_students(self):
        """Display all students in the system"""
        if not self.students:
            print("\nNo students in the system yet.")
            return
        
        print("\n" + "="*70)
        print("ALL STUDENTS".center(70))
        print("="*70)
        print(f"{'ID':<10} {'Name':<25} {'Age':<8} {'Avg Marks':<12} {'Grade'}")
        print("-"*70)
        
        for student_id, student in self.students.items():
            avg = student.calculate_average()
            grade = student.calculate_grade() if student.marks else 'N/A'
            avg_str = f"{avg:.2f}" if student.marks else "N/A"
            
            print(f"{student_id:<10} {student.name:<25} {student.age:<8} {avg_str:<12} {grade}")
        
        print("="*70)
    
    def sort_students_by_average(self):
        """Display students sorted by average marks (highest first)"""
        if not self.students:
            print("\nNo students in the system yet.")
            return
        
        # Filter students who have marks and sort by average
        students_with_marks = [(s, s.calculate_average()) 
                               for s in self.students.values() 
                               if s.marks]
        
        if not students_with_marks:
            print("\nNo students have marks recorded yet.")
            return
        
        sorted_students = sorted(students_with_marks, 
                                key=lambda x: x[1], 
                                reverse=True)
        
        print("\n" + "="*70)
        print("STUDENTS RANKED BY PERFORMANCE".center(70))
        print("="*70)
        print(f"{'Rank':<6} {'ID':<10} {'Name':<25} {'Avg Marks':<12} {'Grade'}")
        print("-"*70)
        
        for rank, (student, avg) in enumerate(sorted_students, 1):
            grade = student.calculate_grade()
            
            # Add medal emoji for top 3
            rank_display = f"{rank}."
            if rank == 1:
                rank_display = "🥇 1."
            elif rank == 2:
                rank_display = "🥈 2."
            elif rank == 3:
                rank_display = "🥉 3."
            
            print(f"{rank_display:<6} {student.student_id:<10} {student.name:<25} {avg:<12.2f} {grade}")
        
        print("="*70)


def display_menu():
    """Display the main menu"""
    print("\n" + "="*70)
    print("STUDENT MANAGEMENT SYSTEM".center(70))
    print("="*70)
    print("1. Add Student")
    print("2. Add Marks for Student")
    print("3. Search Student by ID")
    print("4. Display Student Report")
    print("5. Display All Students")
    print("6. Sort Students by Average Marks")
    print("7. Exit")
    print("="*70)


def main():
    """Main program loop"""
    sms = StudentManagementSystem()
    
    print("\n📚 Welcome to Student Management System!")
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                print("\n--- Add New Student ---")
                student_id = input("Enter Student ID: ").strip()
                name = input("Enter Student Name: ")
                age = input("Enter Student Age: ")
                sms.add_student(student_id, name, age)
            
            elif choice == '2':
                print("\n--- Add Student Marks ---")
                student_id = input("Enter Student ID: ").strip()
                subject = input("Enter Subject: ")
                marks = input("Enter Marks (0-100): ")
                sms.add_student_marks(student_id, subject, marks)
            
            elif choice == '3':
                print("\n--- Search Student ---")
                student_id = input("Enter Student ID: ").strip()
                sms.search_student(student_id)
            
            elif choice == '4':
                print("\n--- Student Report ---")
                student_id = input("Enter Student ID: ").strip()
                sms.display_student_report(student_id)
            
            elif choice == '5':
                sms.display_all_students()
            
            elif choice == '6':
                sms.sort_students_by_average()
            
            elif choice == '7':
                print("\n👋 Thank you for using Student Management System!")
                print("📖 Keep learning and growing!\n")
                break
            
            else:
                print("\n✗ Invalid choice. Please enter a number between 1 and 7.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Exiting... Goodbye!")
            break
        except Exception as e:
            print(f"\n✗ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()