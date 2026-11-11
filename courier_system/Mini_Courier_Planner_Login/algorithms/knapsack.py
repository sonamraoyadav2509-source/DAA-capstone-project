def knapsack(parcels, capacity):
    """
    Solve 0/1 Knapsack using dynamic programming.
    Parcel weights are converted to integer units of 0.1 kg.
    Time: O(n * C), space: O(n * C), where C is capacity in 0.1 kg units.
    """
    scale = 10
    capacity_units = int(round(capacity * scale))
    weights = [int(round(p["weight"] * scale)) for p in parcels]
    n = len(parcels)

    dp = [[0] * (capacity_units + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight = weights[i - 1]
        value = parcels[i - 1]["value"]
        for c in range(capacity_units + 1):
            dp[i][c] = dp[i - 1][c]
            if weight <= c:
                dp[i][c] = max(dp[i][c], value + dp[i - 1][c - weight])

    selected = []
    remaining = capacity_units
    for i in range(n, 0, -1):
        if dp[i][remaining] != dp[i - 1][remaining]:
            selected.append(parcels[i - 1])
            remaining -= weights[i - 1]

    selected.reverse()
    total_weight = sum(p["weight"] for p in selected)
    total_value = sum(p["value"] for p in selected)
    return selected, total_weight, total_value
