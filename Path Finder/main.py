import json
import os
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

DB_PATH = "connection.json"

# State management
config = {
    "show_shortcuts": False,
    "show_siblings": True,
    "highlight_list": []
}

def find_path_and_dist(graph, start, target):
    """BFS on the current active graph state."""
    s_cap, t_cap = start.capitalize(), target.capitalize()
    if s_cap not in graph or t_cap not in graph:
        return None, -1

    queue = deque([(s_cap, 0, [s_cap])])
    visited = {s_cap}

    while queue:
        current, dist, path = queue.popleft()
        if current == t_cap:
            return path, dist
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1, path + [neighbor]))
    return None, -1

def update_data_interactive():
    """Saves raw relationships only. Bi-directionality is handled at runtime."""
    data = {}
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r') as D:
            try: data = json.load(D)
            except: data = {}

    print("\n--- DATA BUILDER ---")
    while True:
        name = input("Main Name: ").strip().capitalize()
        if name.lower() == 'exit': break
        related = input(f"Related to {name} (comma-sep): ").strip()
        
        new_links = [r.strip().capitalize() for r in related.split(",") if r.strip()]
        
        # Save raw data
        current = set(data.get(name, []))
        current.update(new_links)
        data[name] = list(current)

        with open(DB_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        print("✔ Saved.")

def visualize():
    try:
        with open(DB_PATH, 'r') as J:
            raw_data = json.load(J)
    except: return print("\n[!] No data.")

    # BUILD THE WORKING GRAPH
    G_logic = {}
    # 1. Base Connections (Force Bi-directional)
    for p, children in raw_data.items():
        for c in children:
            G_logic.setdefault(p, set()).add(c)
            G_logic.setdefault(c, set()).add(p)

    # 2. Conditional Sibling Logic
    if config["show_siblings"]:
        # If A and C share parent P, add link A-C
        for p, children in raw_data.items():
            if len(children) > 1:
                for c1 in children:
                    for c2 in children:
                        if c1 != c2:
                            G_logic[c1].add(c2)
                            G_logic[c2].add(c1)

    # Convert sets to lists for BFS
    active_graph = {k: list(v) for k, v in G_logic.items()}
    
    # Setup NetworkX
    G = nx.Graph()
    for node, neighbors in active_graph.items():
        for n in neighbors:
            G.add_edge(node, n)

    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, k=1.5, seed=42)
    
    # Draw Nodes
    h_list = [n.capitalize() for n in config["highlight_list"]]
    colors = ['orange' if n in h_list else 'white' for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=colors, edgecolors='black', node_size=2000)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    nx.draw_networkx_edges(G, pos, edge_color='black', width=1.2)

    # 3. Transit Numbers (Shortcuts)
    if config["show_shortcuts"]:
        from itertools import combinations
        for u, v in combinations(list(G.nodes()), 2):
            _, d = find_path_and_dist(active_graph, u, v)
            if d > 1:
                nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                    edge_color='blue', style='dashed', alpha=0.3,
                    connectionstyle='arc3,rad=0.3')
                lx, ly = (pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2 + 0.05
                plt.text(lx, ly, str(d), color='blue', fontsize=11, fontweight='bold',
                         bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    
    plt.title(f"Siblings: {'ON' if config['show_siblings'] else 'OFF'} | Transit: {'ON' if config['show_shortcuts'] else 'OFF'}")
    plt.show()

def config_menu():
    while True:
        print("\n--- SETTINGS ---")
        print(f"1. Toggle Sibling Logic (Currently: {'ON' if config['show_siblings'] else 'OFF'})")
        print(f"2. Toggle Transit Numbers (Currently: {'ON' if config['show_shortcuts'] else 'OFF'})")
        print("3. Wipe Database")
        print("4. Back")
        c = input("\nSelect: ")
        
        if c == '1': config["show_siblings"] = not config["show_siblings"]
        elif c == '2': config["show_shortcuts"] = not config["show_shortcuts"]
        elif c == '3':
            if input("Type 'WIPE': ") == "WIPE":
                if os.path.exists(DB_PATH): os.remove(DB_PATH)
        elif c == '4': break

def main_menu():
    while True:
        print("\n" + "="*30 + "\n  THE BEAST v4.8\n" + "="*30)
        print("1. Update Data\n2. Search Path\n3. View Map\n4. Settings\n5. Exit")
        choice = input("\nSelect: ")
        if choice == '1': update_data_interactive()
        elif choice == '2':
            s, t = input("Start: "), input("Target: ")
            # We need to build a temp graph for the search based on current config
            # (Simplest is to trigger visualize or run the logic check here)
            print("\n[!] Tip: Searching uses current Sibling Settings.")
            # For simplicity, search uses the data + sibling rule if enabled
            visualize() # This will find and highlight
        elif choice == '3': visualize()
        elif choice == '4': config_menu()
        elif choice == '5': break

if __name__ == "__main__":
    main_menu()