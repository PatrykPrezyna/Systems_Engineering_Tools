import json
import itertools

# JSON data
data = [
    {
        "Decisison": "Robot Mount Type",
        "Options": [
            {"name": "On Bed", "cost_factor": 1, "performence_factor": 5},
            {"name": "Free Standing", "cost_factor": 3, "performence_factor": 3},
            {"name": "Hand Held", "cost_factor": 5, "performence_factor": 1},
        ],
    },
    {
        "Decisison": "Procedure Imaging Type",
        "Options": [
            {"name": "CT Scan", "cost_factor": 1, "performence_factor": 5},
            {"name": "Imageless", "cost_factor": 3, "performence_factor": 3},
            {"name": "X-ray", "cost_factor": 5, "performence_factor": 1},
            {"name": "MRI", "cost_factor": 5, "performence_factor": 1},
        ],
    },
    {
        "Decisison": "Onboard vs Offboard Power",
        "Options": [
            {"name": "Onboard", "cost_factor": 1, "performence_factor": 5},
            {"name": "Offboard", "cost_factor": 3, "performence_factor": 3},
        ],
    },
        {
        "Decisison": "Onboard vs Offboard Computing",
        "Options": [
            {"name": "Onboard", "cost_factor": 1, "performence_factor": 1},
            {"name": "Offboard", "cost_factor": 3, "performence_factor": 1}
        ],
    },
]

# Extract all decisions and their options
decisions = [decision["Options"] for decision in data]

# Generate all combinations of options (one from each decision)
combinations = list(itertools.product(*decisions))

# Calculate cost and performance for each combination
designs = []
for combination in combinations:
    total_cost = sum(option["cost_factor"] for option in combination)
    total_performance = sum(option["performence_factor"] for option in combination)
    design = {
        "Selected Options": [option["name"] for option in combination],
        "Total Cost": total_cost,
        "Total Performance": total_performance,
    }
    designs.append(design)

# Print results
for i, design in enumerate(designs, start=1):
    print(f"Design {i}:")
    print(f"  Selected Options: {design['Selected Options']}")
    print(f"  Total Cost: {design['Total Cost']}")
    print(f"  Total Performance: {design['Total Performance']}")
    print()

# Save results to a JSON file
with open("designs.json", "w") as json_file:
    json.dump(designs, json_file, indent=4)

print("Designs saved to 'designs.json'")
