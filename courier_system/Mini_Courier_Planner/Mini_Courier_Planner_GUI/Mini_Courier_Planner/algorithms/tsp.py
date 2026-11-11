from algorithms.graph import dijkstra


def nearest_neighbor_tsp(graph, start, destinations):
    """
    Approximate a delivery tour by repeatedly visiting the nearest
    unvisited destination, using Dijkstra distances between locations.
    This is a heuristic and does not guarantee the globally shortest TSP tour.
    """
    unvisited = set(destinations)
    unvisited.discard(start)
    current = start
    route = [start]
    total_distance = 0.0

    while unvisited:
        best_node = None
        best_distance = float("inf")

        for candidate in unvisited:
            distance, _ = dijkstra(graph, current, candidate)
            if distance < best_distance:
                best_distance = distance
                best_node = candidate

        if best_node is None or best_distance == float("inf"):
            break

        total_distance += best_distance
        route.append(best_node)
        unvisited.remove(best_node)
        current = best_node

    # Return to the depot to complete the tour, if every destination was reached.
    if not unvisited:
        return_distance, _ = dijkstra(graph, current, start)
        if return_distance != float("inf"):
            total_distance += return_distance
            route.append(start)

    return route, total_distance
