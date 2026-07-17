# Python Diary CLI

A simple command-line diary application.

## Features

- Write entries with timestamps
- View all entries
- Filter by date
- Search by keyword
- Edit entries
- Delete entries
- JSON storage

## Quick Start

```bash
# Clone and enter directory
cd diary

# Run
python diary.py
```

## Menu Options

```
1. Write a new entry
2. View all entries
3. View by date
4. Search by keyword
5. Edit entry
6. Delete entry
7. Exit
```

## File Structure

```
diary/
├── diary.py      # Main program
├── utils.py      # Functions
└── entries.json  # Data storage
```

## Example

```
--- Add New Entry ---
Title: My Day
Content: Had a great day coding!
Entry saved!

--- View All ---
1. 2026-07-16 14:35 - My Day
   Content: Had a great day coding!
```

## Requirements

- Python 3.6+
- No external packages needed

## Data Format

```json
[
  {
    "date": "2026-07-16 14:35",
    "title": "My Day",
    "content": "Had a great day coding!"
  }
]
```
