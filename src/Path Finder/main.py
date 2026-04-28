import json
import os
import glob  # For finding all timestamped reports
import networkx as nx
import matplotlib
matplotlib.use("TkAgg") # for linux(maybe macos) in vscode in running
import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt #--> for windows users/linux(maybe mac) in terminal running
import plotly.graph_objects as go
from datetime import datetime
from itertools import combinations
from networkx.algorithms.community import greedy_modularity_communities

DB_PATH = "connection.json"
CONFIG_PATH = "config.json"

# Default configuration
config = {
    "show_siblings": True,
    "show_transit": False,
    "render_3d": False,
    "highlight_list": [],
    "max_transit_dist": 2
}

# --- PERSISTENCE LOGIC ---

def load_config():
    """Loads settings from JSON on startup."""
    global config
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            try:
                saved_config = json.load(f)
                config.update(saved_config)
            except:
                print("[!] Config file corrupted, using defaults.")

def save_config():
    """Saves current settings to JSON."""
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

# --- GRAPH ENGINE ---

def get_graph():
    if not os.path.exists(DB_PATH): return None
    with open(DB_PATH, 'r') as f:
        try: data = json.load(f)
        except: return None
    G = nx.Graph()
    for parent, children in data.items():
        p_cap = parent.capitalize()
        for child in children:
            c_cap = child.capitalize()
            G.add_edge(p_cap, c_cap)
            if config["show_siblings"]:
                for other_child in children:
                    oc_cap = other_child.capitalize()
                    if c_cap != oc_cap: G.add_edge(c_cap, oc_cap)
    return G

def get_node_colors(G):
    communities = list(greedy_modularity_communities(G))
    color_map = {}
    palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    for i, comm in enumerate(communities):
        color = palette[i % len(palette)]
        for node in comm: color_map[node] = color
    return ['orange' if n in config["highlight_list"] else color_map.get(n, 'skyblue') for n in G.nodes()]

# --- VISUALIZATION ---

def visualize_2d(G):
    plt.figure("Path Finder", figsize=(12, 9))
    pos = nx.spring_layout(G, k=1.5, seed=42)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.5, alpha=0.3)
    
    if config["show_transit"]:
        for u, v in combinations(G.nodes(), 2):
            if not G.has_edge(u, v):
                try:
                    dist = nx.shortest_path_length(G, u, v)
                    if 1 < dist <= config["max_transit_dist"]:
                        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='blue', 
                                               style='--', alpha=0.15, connectionstyle="arc3,rad=0.3")
                except: continue

    nx.draw_networkx_nodes(G, pos, node_color=get_node_colors(G), node_size=1600, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    plt.title("Path Finder | Colors = Communities")
    plt.show()

def visualize_3d(G):
    pos = nx.spring_layout(G, dim=3, seed=42)
    edge_x, edge_y, edge_z = [], [], []
    for u, v in G.edges():
        x0, y0, z0 = pos[u]; x1, y1, z1 = pos[v]
        edge_x.extend([x0, x1, None]); edge_y.extend([y0, y1, None]); edge_z.extend([z0, z1, None])
    
    traces = [go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', 
                           line=dict(color='black', width=1.5), name='Direct')]

    if config["show_transit"]:
        t_x, t_y, t_z = [], [], []
        for u, v in combinations(G.nodes(), 2):
            if not G.has_edge(u, v):
                try:
                    dist = nx.shortest_path_length(G, u, v)
                    if 1 < dist <= config["max_transit_dist"]:
                        x0, y0, z0 = pos[u]; x1, y1, z1 = pos[v]
                        t_x.extend([x0, x1, None]); t_y.extend([y0, y1, None]); t_z.extend([z0, z1, None])
                except: continue
        if t_x:
            traces.append(go.Scatter3d(x=t_x, y=t_y, z=t_z, mode='lines', 
                                       line=dict(color='blue', width=1, dash='dash'), 
                                       opacity=0.3, name='Transit'))

    node_x, node_y, node_z = [], [], []
    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x); node_y.append(y); node_z.append(z)

    traces.append(go.Scatter3d(x=node_x, y=node_y, z=node_z, mode='markers+text', 
                               text=list(G.nodes()), textposition="top center",
                               marker=dict(size=6, color=get_node_colors(G), 
                               line=dict(color='black', width=1))))
    
    fig = go.Figure(data=traces)
    fig.update_layout(title="Path Finder 3D Engine")
    fig.show()

# --- CORE FEATURES ---

def update_data():
    data = {}
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r') as f:
            try: data = json.load(f)
            except: data = {}
    name = input("Main Name: ").strip().capitalize()
    if name.lower() == 'exit': return
    related = input(f"Related to {name} (comma separated): ").strip()
    new_links = [r.strip().capitalize() for r in related.split(",") if r.strip()]
    current = set(data.get(name, []))
    current.update(new_links)
    data[name] = list(current)
    with open(DB_PATH, 'w') as f:
        json.dump(data, f, indent=4)
    print("✔ Saved.")

def search_path():
    G = get_graph()
    if not G: return print("[!] No data.")
    s, t = input("Start: ").strip().capitalize(), input("Target: ").strip().capitalize()
    if s in G and t in G:
        try:
            path = nx.shortest_path(G, s, t)
            config["highlight_list"] = path
            save_config()
            print(f"✅ Path found: {' -> '.join(path)}")
            print(f"📍 Distance: {len(path) - 1} Degrees of Separation")
        except nx.NetworkXNoPath: print("❌ No path found.")
    else: print("[!] Name missing.")

def run_network_analysis():
    G = get_graph()
    if not G: return print("[!] No data.")
    centrality = nx.degree_centrality(G)
    influencer = max(centrality, key=centrality.get)
    lengths = dict(nx.all_pairs_shortest_path_length(G))
    all_dists = [d for s in lengths for e, d in lengths[s].items() if s != e]
    if not all_dists: return print("[!] Not enough connections.")
    
    n, avg_dos = len(G.nodes()), sum(all_dists) / len(all_dists)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n--- Path Finder: NETWORK STATS ---")
    print(f"Total People: {n}\nMost Influential: {influencer}")
    print(f"Average Separation: {avg_dos:.2f}\nDensity: {nx.density(G):.4f}")

    filename = f"report_{file_timestamp}.txt"
    with open(filename, "w") as f:
        f.write(f"Path Finder Report\nGenerated: {now}\nInfluencer: {influencer}\nDoS: {avg_dos:.2f}")
    print(f"✔ Report saved as '{filename}'")

def settings_menu():
    while True:
        print(f"\n--- Path Finder: SETTINGS ---")
        print(f"[1] Toggle Siblings: {'ON' if config['show_siblings'] else 'OFF'}")
        print(f"[2] Toggle Transit:  {'ON' if config['show_transit'] else 'OFF'}")
        print(f"[3] Max Transit Distance: {config['max_transit_dist']}")
        print(f"[4] Toggle 3D Mode:  {'3D' if config['render_3d'] else '2D'}")
        print(f"[5] Clear Search Highlights\n[6] Back")
        
        choice = input("\nSelect: ")
        if choice == '1': config["show_siblings"] = not config["show_siblings"]
        elif choice == '2': config["show_transit"] = not config["show_transit"]
        elif choice == '3':
            try: config["max_transit_dist"] = int(input("Max dist (1-5): "))
            except: pass
        elif choice == '4': config["render_3d"] = not config["render_3d"]
        elif choice == '5': config["highlight_list"] = []
        elif choice == '6': break
        save_config()

def wipe_all_data():
    if input("\nType 'DELETE' to wipe ALL data and reports: ") == "DELETE":
        # Delete static files
        for f in [DB_PATH, CONFIG_PATH, "stats_report.txt"]:
            if os.path.exists(f): os.remove(f)
        
        # Delete all timestamped reports
        reports = glob.glob("report_*.txt")
        for r in reports:
            os.remove(r)
        
        config["highlight_list"] = []
        print("✔ All data and reports wiped.")

def main():
    load_config()
    while True:
        print(f"\n{'='*30}\n  Path Finder v5.8.4\n{'='*30}")
        print("1. Update Data\n2. Search Path\n3. View Map\n4. Network Analysis\n5. Settings\n6. WIPE DATA\n7. Exit")
        c = input("\nSelect: ")
        if c == '1': update_data()
        elif c == '2': search_path()
        elif c == '3':
            G = get_graph()
            if G: visualize_3d(G) if config["render_3d"] else visualize_2d(G)
        elif c == '4': run_network_analysis()
        elif c == '5': settings_menu()
        elif c == '6': wipe_all_data()
        elif c == '7': break

if __name__ == "__main__": main()