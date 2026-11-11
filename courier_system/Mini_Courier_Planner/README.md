# Mini-Courier Planner

A Python implementation of the Capstone Assignment: Mini-Courier Planner.

## Requirements
- Python 3.10 or newer (Python 3.14 is suitable)
- Python package `matplotlib` for generating the runtime chart (optional)

## Folder structure
```text
Mini_Courier_Planner/
|-- main.py
|-- utils.py
|-- performance.py
|-- algorithms/
|   |-- __init__.py
|   |-- sorting.py
|   |-- knapsack.py
|   |-- graph.py
|   `-- tsp.py
`-- data/
    |-- parcels.csv
    `-- deliveries.csv
```

## Run in VS Code
1. Extract the ZIP file.
2. Open the `Mini_Courier_Planner` folder in VS Code.
3. Open Terminal > New Terminal.
4. Install chart support with `python -m pip install matplotlib` (optional, for runtime_chart.png).
5. Run `python --version` to check Python.
6. Run `python main.py` (on some Windows systems use `py main.py`).
7. Enter courier bag capacity in kg, or press Enter for the default 15 kg.

## Algorithms used
- Merge Sort: sorts parcels by descending priority, then ascending deadline.
- 0/1 Knapsack: selects the highest-value set of parcels within the bag capacity.
- Dijkstra: finds shortest paths between the depot and delivery locations.
- Nearest Neighbor TSP: creates an approximate delivery tour. It is a heuristic, not a guaranteed optimal TSP solution.
- Performance testing: records Merge Sort and Knapsack runtime for increasing input sizes, saves performance_results.csv, and creates runtime_chart.png when Matplotlib is installed.

## Data files
Edit `data/parcels.csv` to add parcels. The destination must be a node present in `data/deliveries.csv`.
Edit `data/deliveries.csv` to change the road network. Distances must be non-negative numbers.

## Complexity summary
| Algorithm | Time complexity | Space complexity |
|---|---|---|
| Merge Sort | O(n log n) | O(n) |
| 0/1 Knapsack | O(nC) | O(nC) |
| Dijkstra (heap) | O((V+E) log V) | O(V+E) |
| Nearest Neighbor TSP | O(k^2 * Dijkstra) | Depends on graph and cached route data; this implementation stores no all-pairs cache |

C is the capacity measured in 0.1 kg units; V is number of graph vertices, E is number of edges, and k is number of delivery destinations.

## Important
This is a prototype with sample data. Replace the sample parcels and road distances with your own test dataset before submission. Take screenshots of successful runs and runtime output for the report.
