import heapq

# Simulated road network for the academic prototype.
GRAPH = {
    "Central Hospital": [("Clock Tower", 2.0), ("Patel Nagar", 2.5)],
    "Clock Tower": [("Central Hospital", 2.0), ("ISBT", 2.0), ("Raipur", 4.0)],
    "ISBT": [("Clock Tower", 2.0), ("Patel Nagar", 2.0), ("Prem Nagar", 4.0)],
    "Patel Nagar": [("Central Hospital", 2.5), ("ISBT", 2.0), ("Prem Nagar", 3.0)],
    "Prem Nagar": [("ISBT", 4.0), ("Patel Nagar", 3.0), ("Raipur", 5.0)],
    "Raipur": [("Clock Tower", 4.0), ("Prem Nagar", 5.0)],
}


def shortest_path(start: str, destination: str):
    if start not in GRAPH or destination not in GRAPH:
        raise ValueError("Unknown location")
    distances = {node: float("inf") for node in GRAPH}
    previous = {}
    distances[start] = 0.0
    queue = [(0.0, start)]
    while queue:
        distance, node = heapq.heappop(queue)
        if distance > distances[node]:
            continue
        if node == destination:
            break
        for neighbor, weight in GRAPH[node]:
            new_distance = distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = node
                heapq.heappush(queue, (new_distance, neighbor))
    if distances[destination] == float("inf"):
        return [], None
    path = []
    current = destination
    while current != start:
        path.append(current)
        current = previous[current]
    path.append(start)
    path.reverse()
    return path, round(distances[destination], 1)


def all_locations():
    return list(GRAPH.keys())
