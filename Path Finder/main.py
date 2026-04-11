import requests
from bs4 import BeautifulSoup
from collections import deque

def get_related_names(name):
    """
    Scrapes names.org to find the 'Related Names' section.
    """
    url = f"https://www.names.org/n/{name.lower()}/about"
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the 'Related Names' section - usually in <a> tags within a specific div
        related_section = soup.find('div', id='related-names')
        if not related_section:
            return []
            
        return [a.text.strip() for a in related_section.find_all('a')]
    except:
        return []

def find_distance(start_name, target_name, max_depth=3):
    """
    BFS Algorithm to find the shortest distance between two names.
    """
    # Queue stores: (current_name, current_distance)
    queue = deque([(start_name, 0)])
    visited = {start_name.lower()}
    
    print(f"Searching for connection: {start_name} -> {target_name}...")

    while queue:
        current, distance = queue.popleft()
        
        if current.lower() == target_name.lower():
            return distance
            
        if distance < max_depth:
            print(f"  Exploring {current} (Distance: {distance})...")
            related = get_related_names(current)
            
            for name in related:
                if name.lower() not in visited:
                    visited.add(name.lower())
                    queue.append((name, distance + 1))
                    
    return -1

# --- Run the Search ---
start = "Alexander"
end = "Lex"
dist = find_distance(start, end)

if dist != -1:
    print(f"\nSuccess! {start} is related to {end} by a distance of {dist}.")
else:
    print(f"\nNo connection found within the depth limit.")