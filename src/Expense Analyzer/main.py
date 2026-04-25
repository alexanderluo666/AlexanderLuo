import json
import os

# The 'Database' file on your Fedora system
DATA_FILE = "expenses.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_expense(data):
    category = input("Enter category (e.g., Food, Games, School): ").capitalize()
    amount = float(input("Enter amount ($): "))
    
    if category not in data:
        data[category] = []
    
    data[category].append(amount)
    save_data(data)
    print(f"✔ Added ${amount} to {category}")

def show_stats(data):
    if not data:
        print("No data yet!")
        return

    total = sum(sum(amounts) for amounts in data.values())
    print(f"\n--- Financial Summary ---")
    print(f"Total Spent: ${total:.2f}")
    
    for category, amounts in data.items():
        cat_total = sum(amounts)
        percentage = (cat_total / total) * 100
        print(f"{category}: ${cat_total:.2f} ({percentage:.1f}%)")

if __name__ == "__main__":
    load_data()