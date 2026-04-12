import json
import os
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt


DB_PATH = "connection.json"

def find_distance(start, target):
    try:
        with open(DB_PATH, 'r') as D:
            graph = json.load(D)
    except FileNotFoundError:
        print("\n[!] Error: connection.json not found! Add some data first.")
        return -1

    queue = deque([(start.capitalize(), 0)])
    visited = {start.capitalize()}

    print(f"\n--- Searching: {start} -> {target} ---")

    while queue:
        current, dist = queue.popleft()
        if current.lower() == target.lower():
            return dist

        neighbors = graph.get(current, [])
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1 

def update_data_interactive():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r') as D:
            data = json.load(D)
    else:
        data = {}

    print("\n--- Data Builder (Type 'exit' to stop) ---")
    while True:
        name = input("Enter Main Name: ").strip().capitalize()
        if name.lower() == 'exit': break
        
        related = input(f"Enter names related to {name} (comma-separated): ")
        if related.lower() == 'exit': break
        
        clean_related = [r.strip().capitalize() for r in related.split(",") if r.strip()]
        data[name] = clean_related

        with open(DB_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"✔ Link Created: {name} -> {', '.join(clean_related)}")

def visualize_bold(highlight_list):
    try:
        with open(DB_PATH, 'r') as J:
            data = json.load(J)
    except FileNotFoundError:
        return print("No data to visualize.")

    G = nx.DiGraph()
    for parent, children in data.items():
        for child in children:
            G.add_edge(parent, child)

    highlights = [n.capitalize() for n in highlight_list if n]
    
    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if u in highlights or v in highlights:
            edge_colors.append('red') 
            edge_widths.append(4.0)     
        else:
            edge_colors.append('#E0E0E0') 
            edge_widths.append(1.0)

    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, k=1.5, seed=42) 

    nx.draw(G, pos, with_labels=True, 
            node_color='white', edgecolors='black', node_size=2500,
            edge_color=edge_colors, width=edge_widths,
            arrowsize=30, arrowstyle='-|>', 
            font_size=9, font_weight='bold')

    plt.title(f"Connection Map Focus: {', '.join(highlights)}")
    plt.gcf().canvas.manager.set_window_title('Connection Map')
    plt.show()

def main_menu():
    while True:
        print("\n" + "="*30)
        print("  CONNECTION NETWORK MANAGER")
        print("="*30)
        print("1. Add/Update Name Data")
        print("2. Search Relationship Distance")
        print("3. Visualize Full Map")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ")

        if choice == '1':
            update_data_interactive()
        elif choice == '2':
            s = input("Start Name: ")
            e = input("Target Name: ")
            d = find_distance(s, e)
            if d != -1:
                print(f"\nResult: {s} and {e} are {d} steps apart.")
                visualize_bold([s, e])
            else:
                print("\nNo connection found.")
        elif choice == '3':
            visualize_bold([])
        elif choice == '4':
            print("Shutting down...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()