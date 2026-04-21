import json
import os
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from itertools import combinations
from networkx.algorithms.community import greedy_modularity_communities

DB_PATH = "connection.json"

config = {
    "show_siblings": True,
    "show_transit": False,
    "render_3d": False,
    "highlight_list": [],
    "max_transit_dist": 2
}

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
    """Detects communities and assigns colors. Highlights override communities."""
    # 1. Detect Communities (Groups)
    communities = list(greedy_modularity_communities(G))
    color_map = {}
    # Modern color palette
    palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, community in enumerate(communities):
        color = palette[i % len(palette)]
        for node in community:
            color_map[node] = color

    # 2. Apply colors, but allow 'highlight_list' (orange) to override
    final_colors = []
    for node in G.nodes():
        if node in config["highlight_list"]:
            final_colors.append('orange')
        else:
            final_colors.append(color_map.get(node, 'skyblue'))
    return final_colors

def visualize_2d(G):
    plt.figure(figsize=(12, 9))
    pos = nx.spring_layout(G, k=1.5, seed=42)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1.5, alpha=0.3)
    
    if config["show_transit"]:
        for u, v in combinations(G.nodes(), 2):
            if not G.has_edge(u, v):
                try:
                    path = nx.shortest_path(G, u, v)
                    dist = len(path) - 1
                    if 1 < dist <= config["max_transit_dist"]:
                        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color='blue', 
                                               style='--', alpha=0.15, connectionstyle="arc3,rad=0.3")
                except: continue

    colors = get_node_colors(G)
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=1600, edgecolors='black')
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    plt.title(f"Path Finder v5.8 | Colors represent detected communities")
    plt.show()

def visualize_3d(G):
    pos = nx.spring_layout(G, dim=3, seed=42)
    edge_x, edge_y, edge_z = [], [], []
    for u, v in G.edges():
        x0, y0, z0 = pos[u]; x1, y1, z1 = pos[v]
        edge_x.extend([x0, x1, None]); edge_y.extend([y0, y1, None]); edge_z.extend([z0, z1, None])

    traces = [go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', line=dict(color='black', width=1), name='Direct')]

    node_x, node_y, node_z = [], [], []
    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x); node_y.append(y); node_z.append(z)

    colors = get_node_colors(G)
    traces.append(go.Scatter3d(x=node_x, y=node_y, z=node_z, mode='markers+text', text=list(G.nodes()),
                               marker=dict(size=5, color=colors, line=dict(color='black', width=1))))
    
    fig = go.Figure(data=traces)
    fig.update_layout(title="Path Finder 3D | Community Colored")
    fig.show()

def run_network_analysis():
    G = get_graph()
    if not G: return print("[!] No data.")

    # Influential Person Logic (Degree Centrality)
    centrality = nx.degree_centrality(G)
    influencer = max(centrality, key=centrality.get)
    
    lengths = dict(nx.all_pairs_shortest_path_length(G))
    all_dists = [dist for s in lengths for e, dist in lengths[s].items() if s != e]
    
    if not all_dists: return print("[!] Not enough connections.")

    n = len(G.nodes())
    avg_dos = sum(all_dists) / len(all_dists)
    
    print(f"\n--- Path Finder: NETWORK STATS ---")
    print(f"Total People: {n}")
    print(f"Most Influential: {influencer} ({int(centrality[influencer]*(n-1))} direct links)")
    print(f"Average DoS: {avg_dos:.2f}")
    print(f"Density: {nx.density(G):.4f}")

    with open("stats_report.txt", "w") as f:
        f.write(f"Path Finder v5.8 Report\nMost Influential: {influencer}\nAvg DoS: {avg_dos:.2f}")
    print("✔ Saved to 'stats_report.txt'")

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
            print(f"✅ Path: {' -> '.join(path)}")
        except nx.NetworkXNoPath: print("❌ No path found.")
    else: print("[!] Name missing.")

def wipe_all_data():
    if input("\nType 'DELETE' to wipe all data: ") == "DELETE":
        for f in [DB_PATH, "stats_report.txt"]:
            if os.path.exists(f): os.remove(f)
        config["highlight_list"] = []
        print("✔ Wiped.")

def settings_menu():
    while True:
        print(f"\n--- Path Finder: SETTINGS ---")
        print(f"[1] Toggle Siblings: {config['show_siblings']}")
        print(f"[2] Toggle Transit: {config['show_transit']}")
        print(f"[3] Max Transit Dist: {config['max_transit_dist']}")
        print(f"[4] Toggle 3D Mode: {config['render_3d']}")
        print(f"[5] Clear Search Highlights\n[6] Back")
        
        choice = input("\nSelect: ")
        if choice == '1': config["show_siblings"] = not config["show_siblings"]
        elif choice == '2': config["show_transit"] = not config["show_transit"]
        elif choice == '3':
            try: config["max_transit_dist"] = int(input("Enter max dist (1-5): "))
            except: pass
        elif choice == '4': config["render_3d"] = not config["render_3d"]
        elif choice == '5': config["highlight_list"] = []
        elif choice == '6': break

def main():
    while True:
        print(f"\n{'='*30}\n  Path Finder v5.8\n{'='*30}")
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