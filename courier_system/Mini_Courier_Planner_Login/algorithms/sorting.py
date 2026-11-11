def _comes_first(a, b):
    """Higher priority first; for equal priority, earlier deadline first."""
    if a["priority"] != b["priority"]:
        return a["priority"] > b["priority"]
    return a["deadline"] < b["deadline"]


def merge_sort_parcels(parcels):
    """Sort parcels using Merge Sort. Time: O(n log n), space: O(n)."""
    if len(parcels) <= 1:
        return parcels[:]

    middle = len(parcels) // 2
    left = merge_sort_parcels(parcels[:middle])
    right = merge_sort_parcels(parcels[middle:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if _comes_first(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result
