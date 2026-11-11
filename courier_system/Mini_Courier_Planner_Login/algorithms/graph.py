import csv
import heapq


def load_graph(filename):
    """Load an undirected weighted graph from an edge-list CSV."""
    graph = {}
    locations = set()

    with open(filename, "r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            source = row["source"]
            target = row["target"]
            distance = float(row["distance"])
            graph.setdefault(source, []).append((target, distance))
            graph.setdefault(target, []).append((source, distance))
            locations.add(source)
            locations.add(target)

    return graph, locations


def dijkstra(graph, start, goal):
    """
    Find the shortest path between two graph nodes.
    Time: O((V + E) log V) with a priority queue.
    """
    if start not in graph or goal not in graph:
        return float("inf"), []

    distances = {node: float("inf") for node in graph}
    previous = {}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue
        if current_node == goal:
            break

        for neighbor, weight in graph[current_node]:
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    if distances[goal] == float("inf"):
        return float("inf"), []

    path = []
    node = goal
    while node != start:
        path.append(node)
        node = previous[node]
    path.append(start)
    path.reverse()

    return distances[goal], path
