import json
from collections import deque
#data is stored inside data.json; uses Breadth First Search

def find_distance(start, target, data_file = r"C:\Users\alexa\OneDrive\Desktop\Github\data.json"):

    try:
        with open(data_file, 'r') as d:
            graph = json.load(d)
    except FileNotFoundError:
        print("Error: data.json not found!")
        return -1

    queue = deque([(start, 0)])
    visited = {start}

    print(f"--- Searching for relationship: {start} -> {target} ---")

    while queue:
        current, dist = queue.popleft()


        if current.lower() == target.lower():
            return dist


        neighbors = graph.get(current, [])
        
        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
                print(f"  Checked {neighbor} (Distance: {dist + 1})")

    return -1 


import json
import os

def update_data(name, related_list):
    filename = "data.json"
    

    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
    else:
        data = {}


    clean_name = name.capitalize()
    clean_related = [r.capitalize() for r in related_list]
    
    data[clean_name] = clean_related


    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Successfully updated {clean_name} with {len(clean_related)} connections.")


update_data("Alexander", ["Alex", "Lex", "Xander", "Sasha"])
update_data("Alex", ["Alexander", "Alexis", "Axel"])
update_data("Xander", ["Alexander", "Zander"])


start = "Alexander"
end = "Zander"
distance = find_distance(start, end)

if distance != -1:
    print(f"\nSUCCESS: '{start}' is {distance} steps away from '{end}'.")
else:
    print(f"\nFAILURE: No connection found between '{start}' and '{end}'.")
    