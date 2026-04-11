import json
from collections import deque
#data is stored inside data.json

def find_name_distance(start, target, data_file = r"C:\Users\alexa\OneDrive\Desktop\Github\Path Finder\data.json"):

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


start = "example"
end = "example2"
distance = find_name_distance(start, end)

if distance != -1:
    print(f"\nSUCCESS: '{start}' is {distance} steps away from '{end}'.")
else:
    print(f"\nFAILURE: No connection found between '{start}' and '{end}'.")
    