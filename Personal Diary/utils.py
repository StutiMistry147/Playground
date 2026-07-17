import json
import os
from datetime import datetime

def load_entries():
    """Read entries.json and return list of entries"""
    try:
        with open('entries.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return empty list if file doesn't exist
    except json.JSONDecodeError:
        # If file is corrupted, backup and start fresh
        if os.path.exists('entries.json'):
            backup_name = f"entries_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            os.rename('entries.json', backup_name)
            print(f"Corrupted entries.json backed up as {backup_name}")
        return []

def save_entries(entries):
    """Write list back to entries.json with atomic write"""
    # Write to temp file first, then rename to avoid corruption
    temp_file = 'entries_temp.json'
    try:
        with open(temp_file, 'w') as file:
            json.dump(entries, file, indent=2)
        # Atomic rename (works on most filesystems)
        os.replace(temp_file, 'entries.json')
    except Exception as e:
        print(f"Error saving entries: {e}")
        if os.path.exists(temp_file):
            os.remove(temp_file)

def add_entry():
    """Take user input, attach timestamp, save"""
    print("\n--- Add New Entry ---")
    
    # Optional: Add title
    title = input("Enter a title for your entry (optional): ").strip()
    content = input("Write your diary entry: ").strip()
    
    if not content:
        print("Entry content cannot be empty.")
        return
    
    # Create new entry with timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = {
        "date": current_time,
        "title": title if title else "Untitled",
        "content": content
    }
    
    # Load existing entries, append new one, save
    entries = load_entries()
    entries.append(new_entry)
    save_entries(entries)
    
    print("Entry saved successfully!")

def view_all():
    """Print all entries with dates"""
    print("\n--- All Entries ---")
    entries = load_entries()
    
    if not entries:
        print("No entries found. Write your first entry!")
        return
    
    print(f"Total entries: {len(entries)}\n")
    for i, entry in enumerate(entries, 1):
        print(f"{i}. Date: {entry['date']}")
        print(f"   Title: {entry.get('title', 'Untitled')}")
        # Smart truncation for content
        content = entry['content']
        if len(content) > 50:
            print(f"   Content: {content[:50]}...")
        else:
            print(f"   Content: {content}")
        print()

def view_by_date():
    """Filter entries by a date the user types"""
    print("\n--- View Entries by Date ---")
    search_date = input("Enter date (YYYY-MM-DD): ").strip()
    
    if not search_date:
        print("Please enter a valid date.")
        return
    
    entries = load_entries()
    
    # Filter entries where date starts with the search date
    filtered = [entry for entry in entries if entry['date'].startswith(search_date)]
    
    if not filtered:
        print(f"No entries found for {search_date}")
        return
    
    print(f"Found {len(filtered)} entries for {search_date}:\n")
    for entry in filtered:
        print(f"Date: {entry['date']}")
        print(f"Title: {entry.get('title', 'Untitled')}")
        print(f"Content: {entry['content']}")
        print()

def search_by_keyword():
    """Search entries by keyword in content or title"""
    print("\n--- Search Entries ---")
    keyword = input("Enter keyword to search for: ").strip().lower()
    
    if not keyword:
        print("Please enter a keyword.")
        return
    
    entries = load_entries()
    
    # Search in title and content
    matches = []
    for entry in entries:
        title_match = keyword in entry.get('title', '').lower()
        content_match = keyword in entry['content'].lower()
        if title_match or content_match:
            matches.append(entry)
    
    if not matches:
        print(f"No entries found containing '{keyword}'")
        return
    
    print(f"Found {len(matches)} entries containing '{keyword}':\n")
    for i, entry in enumerate(matches, 1):
        print(f"{i}. Date: {entry['date']}")
        print(f"   Title: {entry.get('title', 'Untitled')}")
        # Show matching context
        content = entry['content']
        if len(content) > 60:
            print(f"   Content: {content[:60]}...")
        else:
            print(f"   Content: {content}")
        print()

def delete_entry():
    """Show entries, user picks one to delete"""
    print("\n--- Delete Entry ---")
    entries = load_entries()
    
    if not entries:
        print("No entries to delete.")
        return
    
    # Display entries with numbers
    print("Select an entry to delete:\n")
    for i, entry in enumerate(entries, 1):
        content_preview = entry['content'][:50]
        if len(entry['content']) > 50:
            content_preview += "..."
        print(f"{i}. {entry['date']} - {entry.get('title', 'Untitled')}")
        print(f"   {content_preview}")
        print()
    
    try:
        choice = int(input("\nEnter the number of the entry to delete (or 0 to cancel): "))
        if choice == 0:
            print("Deletion cancelled.")
            return
        elif 1 <= choice <= len(entries):
            deleted_entry = entries.pop(choice - 1)
            save_entries(entries)
            print(f"Deleted entry from {deleted_entry['date']}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def edit_entry():
    """Edit an existing entry"""
    print("\n--- Edit Entry ---")
    entries = load_entries()
    
    if not entries:
        print("No entries to edit.")
        return
    
    # Display entries with numbers
    print("Select an entry to edit:\n")
    for i, entry in enumerate(entries, 1):
        content_preview = entry['content'][:50]
        if len(entry['content']) > 50:
            content_preview += "..."
        print(f"{i}. {entry['date']} - {entry.get('title', 'Untitled')}")
        print(f"   {content_preview}")
        print()
    
    try:
        choice = int(input("\nEnter the number of the entry to edit (or 0 to cancel): "))
        if choice == 0:
            print("Edit cancelled.")
            return
        elif 1 <= choice <= len(entries):
            entry_to_edit = entries[choice - 1]
            print(f"\nCurrent title: {entry_to_edit.get('title', 'Untitled')}")
            new_title = input("Enter new title (press Enter to keep current): ").strip()
            if new_title:
                entry_to_edit['title'] = new_title
            
            print(f"\nCurrent content: {entry_to_edit['content']}")
            new_content = input("Enter new content (press Enter to keep current): ").strip()
            if new_content:
                entry_to_edit['content'] = new_content
            
            # Update timestamp to show when edited
            entry_to_edit['last_edited'] = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            save_entries(entries)
            print("Entry updated successfully!")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def show_menu():
    """Print options, return user choice"""
    print("\n" + "="*40)
    print("        PYTHON DIARY CLI")
    print("="*40)
    print("1. Write a new entry")
    print("2. View all past entries")
    print("3. View entries by date")
    print("4. Search by keyword")
    print("5. Edit an entry")
    print("6. Delete an entry")
    print("7. Exit")
    print("="*40)
    
    return input("Choose an option (1-7): ").strip()
