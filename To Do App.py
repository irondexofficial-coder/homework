import json
from datetime import datetime
from pathlib import Path


class Task:
    """Represents a single task"""
    
    task_id_counter = 1
    
    def __init__(self, title, description="", priority="Medium", task_id=None):
        self.task_id = task_id if task_id else Task.task_id_counter
        if not task_id:
            Task.task_id_counter += 1
        
        self.title = title
        self.description = description
        self.priority = priority  # High, Medium, Low
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at = None
    
    def mark_completed(self):
        """Mark task as completed"""
        self.completed = True
        self.completed_at = datetime.now()
    
    def mark_pending(self):
        """Mark task as pending"""
        self.completed = False
        self.completed_at = None
    
    def get_priority_value(self):
        """Get numeric value for priority (for sorting)"""
        priority_map = {'High': 3, 'Medium': 2, 'Low': 1}
        return priority_map.get(self.priority, 2)
    
    def to_dict(self):
        """Convert task to dictionary for saving"""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create task from dictionary"""
        task = cls(
            title=data['title'],
            description=data['description'],
            priority=data['priority'],
            task_id=data['task_id']
        )
        task.completed = data['completed']
        task.created_at = datetime.fromisoformat(data['created_at'])
        if data['completed_at']:
            task.completed_at = datetime.fromisoformat(data['completed_at'])
        
        # Update counter if needed
        if task.task_id >= Task.task_id_counter:
            Task.task_id_counter = task.task_id + 1
        
        return task
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        priority_icon = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        icon = priority_icon.get(self.priority, "⚪")
        
        return f"{status} [{self.task_id}] {icon} {self.title}"


class TaskManager:
    """Main task management system"""
    
    def __init__(self, save_file="tasks.json"):
        self.tasks = []
        self.save_file = Path(save_file)
        self.load_tasks()
    
    def add_task(self, title, description="", priority="Medium"):
        """Add a new task"""
        try:
            title = title.strip()
            if not title:
                raise ValueError("Task title cannot be empty")
            
            priority = priority.strip().title()
            if priority not in ['High', 'Medium', 'Low']:
                print(f"⚠️  Invalid priority '{priority}'. Using 'Medium' instead.")
                priority = 'Medium'
            
            task = Task(title, description.strip(), priority)
            self.tasks.append(task)
            
            print(f"\n✓ Task added successfully!")
            print(f"  {task}")
            print(f"  Priority: {priority}")
            
            self.save_tasks()
            return task.task_id
            
        except ValueError as e:
            print(f"\n✗ Error: {e}")
            return None
    
    def mark_completed(self, task_id):
        """Mark a task as completed"""
        try:
            task_id = int(task_id)
            task = self._find_task(task_id)
            
            if not task:
                print(f"\n✗ Task ID {task_id} not found!")
                return False
            
            if task.completed:
                print(f"\n⚠️  Task is already completed!")
                return False
            
            task.mark_completed()
            print(f"\n✓ Task marked as completed!")
            print(f"  {task}")
            
            self.save_tasks()
            return True
            
        except ValueError:
            print(f"\n✗ Invalid task ID format!")
            return False
    
    def mark_pending(self, task_id):
        """Mark a task as pending"""
        try:
            task_id = int(task_id)
            task = self._find_task(task_id)
            
            if not task:
                print(f"\n✗ Task ID {task_id} not found!")
                return False
            
            if not task.completed:
                print(f"\n⚠️  Task is already pending!")
                return False
            
            task.mark_pending()
            print(f"\n✓ Task marked as pending!")
            print(f"  {task}")
            
            self.save_tasks()
            return True
            
        except ValueError:
            print(f"\n✗ Invalid task ID format!")
            return False
    
    def delete_task(self, task_id):
        """Delete a task"""
        try:
            task_id = int(task_id)
            task = self._find_task(task_id)
            
            if not task:
                print(f"\n✗ Task ID {task_id} not found!")
                return False
            
            confirm = input(f"\n⚠️  Delete task '{task.title}'? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                self.tasks.remove(task)
                print(f"\n✓ Task deleted successfully!")
                self.save_tasks()
                return True
            else:
                print(f"\n✗ Deletion cancelled.")
                return False
            
        except ValueError:
            print(f"\n✗ Invalid task ID format!")
            return False
    
    def view_pending_tasks(self, sort_by_priority=False):
        """View all pending tasks"""
        pending = [task for task in self.tasks if not task.completed]
        
        if not pending:
            print("\n🎉 No pending tasks! You're all caught up!")
            return
        
        if sort_by_priority:
            pending.sort(key=lambda t: t.get_priority_value(), reverse=True)
        
        print("\n" + "="*80)
        print("PENDING TASKS".center(80))
        print("="*80)
        
        for task in pending:
            created = task.created_at.strftime("%Y-%m-%d %H:%M")
            print(f"{task}")
            if task.description:
                print(f"     Description: {task.description}")
            print(f"     Created: {created}")
            print("-"*80)
        
        print(f"Total Pending: {len(pending)} tasks")
        print("="*80)
    
    def view_completed_tasks(self):
        """View all completed tasks"""
        completed = [task for task in self.tasks if task.completed]
        
        if not completed:
            print("\n📝 No completed tasks yet.")
            return
        
        print("\n" + "="*80)
        print("COMPLETED TASKS".center(80))
        print("="*80)
        
        for task in completed:
            completed_date = task.completed_at.strftime("%Y-%m-%d %H:%M")
            print(f"{task}")
            if task.description:
                print(f"     Description: {task.description}")
            print(f"     Completed: {completed_date}")
            print("-"*80)
        
        print(f"Total Completed: {len(completed)} tasks")
        print("="*80)
    
    def view_all_tasks(self, sort_by_priority=False):
        """View all tasks"""
        if not self.tasks:
            print("\n📝 No tasks yet. Add your first task to get started!")
            return
        
        tasks_to_show = self.tasks.copy()
        
        if sort_by_priority:
            # Sort by priority (high first), then by completion status (pending first)
            tasks_to_show.sort(key=lambda t: (t.completed, -t.get_priority_value()))
        
        print("\n" + "="*80)
        print("ALL TASKS".center(80))
        print("="*80)
        
        for task in tasks_to_show:
            created = task.created_at.strftime("%Y-%m-%d")
            status = "Completed" if task.completed else "Pending"
            
            print(f"{task} | {status}")
            if task.description:
                print(f"     Description: {task.description}")
            print(f"     Created: {created}")
            print("-"*80)
        
        pending_count = sum(1 for t in self.tasks if not t.completed)
        completed_count = len(self.tasks) - pending_count
        
        print(f"Total: {len(self.tasks)} | Pending: {pending_count} | Completed: {completed_count}")
        print("="*80)
    
    def view_tasks_by_priority(self, priority):
        """View tasks filtered by priority"""
        priority = priority.strip().title()
        
        if priority not in ['High', 'Medium', 'Low']:
            print(f"\n✗ Invalid priority. Use: High, Medium, or Low")
            return
        
        filtered = [task for task in self.tasks if task.priority == priority and not task.completed]
        
        if not filtered:
            print(f"\n📝 No pending {priority} priority tasks.")
            return
        
        print("\n" + "="*80)
        print(f"{priority.upper()} PRIORITY TASKS".center(80))
        print("="*80)
        
        for task in filtered:
            created = task.created_at.strftime("%Y-%m-%d")
            print(f"{task}")
            if task.description:
                print(f"     Description: {task.description}")
            print(f"     Created: {created}")
            print("-"*80)
        
        print(f"Total {priority} Priority Tasks: {len(filtered)}")
        print("="*80)
    
    def get_statistics(self):
        """Display task statistics"""
        if not self.tasks:
            print("\n📊 No tasks to analyze yet.")
            return
        
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.completed)
        pending = total - completed
        
        high = sum(1 for t in self.tasks if t.priority == 'High' and not t.completed)
        medium = sum(1 for t in self.tasks if t.priority == 'Medium' and not t.completed)
        low = sum(1 for t in self.tasks if t.priority == 'Low' and not t.completed)
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        print("\n" + "="*60)
        print("TASK STATISTICS".center(60))
        print("="*60)
        print(f"Total Tasks      : {total}")
        print(f"Completed        : {completed} ({completion_rate:.1f}%)")
        print(f"Pending          : {pending}")
        print("-"*60)
        print("Pending by Priority:")
        print(f"  🔴 High Priority  : {high}")
        print(f"  🟡 Medium Priority: {medium}")
        print(f"  🟢 Low Priority   : {low}")
        print("="*60)
    
    def _find_task(self, task_id):
        """Find task by ID"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            data = {
                'tasks': [task.to_dict() for task in self.tasks]
            }
            
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=2)
            
        except Exception as e:
            print(f"\n⚠️  Warning: Could not save tasks to file: {e}")
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        try:
            if self.save_file.exists():
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                
                self.tasks = [Task.from_dict(task_data) for task_data in data['tasks']]
                print(f"\n✓ Loaded {len(self.tasks)} tasks from {self.save_file}")
            
        except Exception as e:
            print(f"\n⚠️  Warning: Could not load tasks from file: {e}")
            self.tasks = []


def display_menu():
    """Display the main menu"""
    print("\n" + "="*70)
    print("SMART TASK MANAGER".center(70))
    print("="*70)
    print("Task Management:")
    print("  1. Add Task")
    print("  2. View All Tasks")
    print("  3. View Pending Tasks")
    print("  4. View Completed Tasks")
    print("  5. View Tasks by Priority")
    print("\nTask Actions:")
    print("  6. Mark Task as Completed")
    print("  7. Mark Task as Pending")
    print("  8. Delete Task")
    print("\nAnalytics:")
    print("  9. View Statistics")
    print("  10. View Pending Tasks (Sorted by Priority)")
    print("\n  11. Exit")
    print("="*70)


def main():
    """Main program loop"""
    manager = TaskManager()
    
    print("\n" + "="*70)
    print("📋 Welcome to Smart Task Manager!".center(70))
    print("Stay Organized, Stay Productive".center(70))
    print("="*70)
    
    while True:
        display_menu()
        
        try:
            choice = input("\nEnter your choice (1-11): ").strip()
            
            if choice == '1':
                print("\n--- Add New Task ---")
                title = input("Enter task title: ")
                description = input("Enter description (optional): ")
                print("\nPriority levels: High, Medium, Low")
                priority = input("Enter priority (default: Medium): ").strip() or "Medium"
                manager.add_task(title, description, priority)
            
            elif choice == '2':
                sort = input("\nSort by priority? (yes/no): ").strip().lower()
                manager.view_all_tasks(sort_by_priority=(sort == 'yes'))
            
            elif choice == '3':
                manager.view_pending_tasks()
            
            elif choice == '4':
                manager.view_completed_tasks()
            
            elif choice == '5':
                print("\n--- Filter by Priority ---")
                print("Available: High, Medium, Low")
                priority = input("Enter priority: ")
                manager.view_tasks_by_priority(priority)
            
            elif choice == '6':
                task_id = input("\nEnter task ID to mark as completed: ")
                manager.mark_completed(task_id)
            
            elif choice == '7':
                task_id = input("\nEnter task ID to mark as pending: ")
                manager.mark_pending(task_id)
            
            elif choice == '8':
                task_id = input("\nEnter task ID to delete: ")
                manager.delete_task(task_id)
            
            elif choice == '9':
                manager.get_statistics()
            
            elif choice == '10':
                manager.view_pending_tasks(sort_by_priority=True)
            
            elif choice == '11':
                print("\n" + "="*70)
                print("Thank you for using Smart Task Manager!".center(70))
                print("Stay productive! 🚀".center(70))
                print("="*70 + "\n")
                break
            
            else:
                print("\n✗ Invalid choice. Please enter a number between 1 and 11.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Exiting... Stay productive!")
            break
        except Exception as e:
            print(f"\n✗ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()