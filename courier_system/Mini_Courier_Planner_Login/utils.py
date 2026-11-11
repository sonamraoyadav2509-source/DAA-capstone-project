import csv


def load_parcels(filename):
    """Read parcel records from a CSV file."""
    parcels = []
    with open(filename, "r", newline="", encoding="utf-8") as file:
        for row in csv.DictReader(file):
            parcels.append({
                "id": row["id"],
                "name": row["name"],
                "priority": int(row["priority"]),
                "deadline": int(row["deadline"]),
                "weight": float(row["weight"]),
                "value": int(row["value"]),
                "destination": row["destination"]
            })
    return parcels


def print_parcels(parcels):
    if not parcels:
        print("  (empty)")
        return
    print(f"{'ID':<6}{'Parcel':<18}{'Priority':<10}{'Deadline':<10}{'Weight':<10}{'Value':<10}{'Destination'}")
    print("-" * 85)
    for p in parcels:
        print(f"{p['id']:<6}{p['name']:<18}{p['priority']:<10}{p['deadline']:<10}"
              f"{p['weight']:<10.2f}{p['value']:<10}{p['destination']}")
