import csv
import random
import time
from algorithms.sorting import merge_sort_parcels
from algorithms.knapsack import knapsack


def run_performance_tests(graph):
    """Measure algorithm runtime, save a CSV table and optionally create a chart."""
    results = []
    print(f"{'Input size':<15}{'Merge Sort (ms)':<20}{'Knapsack (ms)':<20}")
    print("-" * 55)

    random.seed(42)
    for size in (10, 50, 100, 200):
        sample = []
        for i in range(size):
            sample.append({
                "id": str(i),
                "name": f"Parcel-{i}",
                "priority": random.randint(1, 5),
                "deadline": random.randint(1, 30),
                "weight": round(random.uniform(0.1, 2.0), 1),
                "value": random.randint(10, 500),
                "destination": "A"
            })

        start = time.perf_counter()
        ordered = merge_sort_parcels(sample)
        sort_ms = (time.perf_counter() - start) * 1000

        start = time.perf_counter()
        knapsack(ordered, 20)
        knapsack_ms = (time.perf_counter() - start) * 1000

        results.append({
            "input_size": size,
            "merge_sort_ms": round(sort_ms, 4),
            "knapsack_ms": round(knapsack_ms, 4)
        })
        print(f"{size:<15}{sort_ms:<20.3f}{knapsack_ms:<20.3f}")

    with open("performance_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["input_size", "merge_sort_ms", "knapsack_ms"])
        writer.writeheader()
        writer.writerows(results)

    try:
        import matplotlib.pyplot as plt

        sizes = [row["input_size"] for row in results]
        sort_times = [row["merge_sort_ms"] for row in results]
        knapsack_times = [row["knapsack_ms"] for row in results]

        plt.plot(sizes, sort_times, marker="o", label="Merge Sort")
        plt.plot(sizes, knapsack_times, marker="o", label="0/1 Knapsack")
        plt.xlabel("Number of parcels")
        plt.ylabel("Execution time (milliseconds)")
        plt.title("Mini-Courier Planner - Runtime Comparison")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig("runtime_chart.png")
        plt.close()
        print("\nRuntime chart saved as runtime_chart.png")
    except ImportError:
        print("\nMatplotlib is not installed. CSV saved; install it with: pip install matplotlib")

    print("Runtime data saved as performance_results.csv")
    print("Note: Runtime depends on your computer and may vary between runs.")
