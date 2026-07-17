# Explicit imports instead of "from utils import *"
from utils import (
    add_entry, 
    view_all, 
    view_by_date, 
    search_by_keyword,
    edit_entry,
    delete_entry, 
    show_menu
)

def main():
    """Main loop that ties everything together"""
    print("Welcome to your Python Diary!")
    
    while True:
        choice = show_menu()
        
        # Handle each option
        if choice == '1':
            add_entry()
        
        elif choice == '2':
            view_all()
        
        elif choice == '3':
            view_by_date()
        
        elif choice == '4':
            search_by_keyword()
        
        elif choice == '5':
            edit_entry()
        
        elif choice == '6':
            delete_entry()
        
        elif choice == '7':
            print("\nThank you for using the Python Diary. Goodbye!")
            break
        
        else:
            print("Invalid input. Please choose a number between 1 and 7.")
        
        # Pause before showing menu again
        input("\nPress Enter to continue...")

# Run the diary application
if __name__ == "__main__":
    main()
