from algorithms.sorting import merge_sort_parcels
from algorithms.knapsack import knapsack
from algorithms.graph import load_graph, dijkstra
from algorithms.tsp import nearest_neighbor_tsp
from performance import run_performance_tests
from utils import load_parcels, print_parcels


def main():
    print("=" * 60)
    print("                 MINI-COURIER PLANNER")
    print("=" * 60)

    parcels = load_parcels("data/parcels.csv")
    graph, locations = load_graph("data/deliveries.csv")

    if not parcels:
        print("No parcels found. Check data/parcels.csv")
        return

    print("\n1. PARCELS RECEIVED")
    print_parcels(parcels)

    print("\n2. PARCEL PRIORITIZATION (MERGE SORT)")
    sorted_parcels = merge_sort_parcels(parcels)
    print_parcels(sorted_parcels)

    try:
        capacity = float(input("\nEnter courier bag capacity (kg) [default 15]: ") or "15")
    except ValueError:
        print("Invalid capacity. Using 15 kg.")
        capacity = 15.0

    print("\n3. OPTIMAL BOX FILLING (0/1 KNAPSACK)")
    selected, total_weight, total_value = knapsack(sorted_parcels, capacity)
    if selected:
        print_parcels(selected)
        print(f"Total selected weight : {total_weight:.2f} kg")
        print(f"Total parcel value    : {total_value:.2f}")
    else:
        print("No parcel fits the given capacity.")

    print("\n4. SHORTEST DELIVERY PATHS (DIJKSTRA)")
    depot = "Depot"
    if depot not in graph:
        print("Depot node is missing from data/deliveries.csv")
        return

    destinations = list(dict.fromkeys(p["destination"] for p in selected))
    valid_destinations = [d for d in destinations if d in graph]

    for destination in valid_destinations:
        distance, path = dijkstra(graph, depot, destination)
        if distance == float("inf"):
            print(f"{destination}: no route available")
        else:
            print(f"{depot} -> {destination}: {' -> '.join(path)} | Distance: {distance:.2f} km")

    print("\n5. OVERALL ROUTE (NEAREST-NEIGHBOR TSP APPROXIMATION)")
    if valid_destinations:
        route, route_distance = nearest_neighbor_tsp(graph, depot, valid_destinations)
        print("Route:", " -> ".join(route))
        print(f"Approximate total route distance: {route_distance:.2f} km")
    else:
        print("No selected parcel has a valid delivery destination.")

    print("\n6. PERFORMANCE TESTING")
    run_performance_tests(graph)

    print("\nPlanning completed successfully.")


if __name__ == "__main__":
    main()
