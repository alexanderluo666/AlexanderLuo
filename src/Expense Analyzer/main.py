import json
import os

DATA_FILE = "expenses.json"

def load_data():
    """Reads the JSON file from your Fedora disk into a Python dictionary."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {} # If file is corrupted, start fresh
    return {}

def save_data(data):
    """Writes your dictionary back to the JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def delete_data():
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    else:
        print("No data to wipe")

def add_expense(data):
    category = input("Category (e.g. Food, Games): ").strip().capitalize()
    
    # Validation: Ensure the user actually enters a number
    try:
        amount = float(input(f"Amount for {category}: $"))
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")
        return

    if category not in data:
        data[category] = []
    
    data[category].append(amount)
    save_data(data)
    print(f"✅ Added ${amount:.2f} to {category}.")

def show_stats(data):
    if not data:
        print("\n[!] No data recorded yet.")
        return

    total_all = sum(sum(amounts) for amounts in data.values())
    print(f"\n{'='*30}\n FINANCIAL SUMMARY \n{'='*30}")
    
    for cat, amounts in data.items():
        cat_total = sum(amounts)
        avg = cat_total / len(amounts)
        print(f"{cat:10} | Total: ${cat_total:7.2f} | Avg: ${avg:5.2f}")
    
    print("-" * 30)
    print(f"NET TOTAL: ${total_all:.2f}")

def find_expensive_items(data, threshold):
    try:
        limit = float(threshold)
    except ValueError:
        print("❌ Threshold must be a number.")
        return

    print(f"\n--- Items over ${limit:.2f} ---")
    found = False

    # Outer loop: looks at each category (e.g., 'Food')
    for category, amounts in data.items():
        # Inner loop: looks at each individual price in that category
        for price in amounts:
            if price >= limit:
                print(f"[{category}] ${price:.2f}")
                found = True
    
    if not found:
        print("No items found above that amount.")

def menu():
    """The heartbeat of the program."""
    # We load it ONCE at the start
    my_expenses = load_data()
    
    while True:
        print("\n1. Add Expense | 2. Show Stats | 3. Wipe Data | 4. Find Items | 5. Exit")
        choice = input("Select: ")
        if choice == "1":
            add_expense(my_expenses)
        elif choice == "2":
            show_stats(my_expenses)
        elif choice == "3":
            confirm = input("Type 'WIPE' to confirm: ")
            if confirm == "WIPE":
                delete_data()
                my_expenses = {}  # Clear the live dictionary in RAM!
                print("✔ RAM and Disk cleared.")
        elif choice == "4":
            find_expensive_items(my_expenses,input("Threshold:"))
        elif choice == "5":
            print("Goodbye!!!")
            break
        else:
            print("Unknown command.")

if __name__ == "__main__":
    menu()