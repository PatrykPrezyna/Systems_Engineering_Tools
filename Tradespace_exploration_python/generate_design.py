import json
import itertools
import math

# JSON data
data = [
    {
        "Decisison": "Robot Mount Type",
        "Options": [
            {"name": "On Bed", "cost_factor": 1.0, "setting_up_time_factor": 1.0},
            {"name": "Free Standing", "cost_factor": 1.2, "setting_up_time_factor": 0.5},
            {"name": "Hand Held", "cost_factor": 0.4, "setting_up_time_factor": 1.0},
        ],
    },
    {
        "Decisison": "Procedure Imaging Type",
        "Options": [
            {"name": "CT Scan", "cost_factor": 0.9, "setting_up_time_factor": 1.5},
            {"name": "Imageless", "cost_factor": 1.0, "setting_up_time_factor": 1.0},
            {"name": "X-ray", "cost_factor": 0.95, "setting_up_time_factor": 1.4},
            {"name": "MRI", "cost_factor": 0.85, "setting_up_time_factor": 1.3},
        ],
    },
    {
        "Decisison": "Onboard vs Offboard Power",
        "Options": [
            {"name": "Onboard", "cost_factor": 1.1, "setting_up_time_factor": 1.0},
            {"name": "Offboard", "cost_factor": 1.0, "setting_up_time_factor": 1.0},
        ],
    },
        {
        "Decisison": "Onboard vs Offboard Computing",
        "Options": [
            {"name": "Onboard", "cost_factor": 1.2, "setting_up_time_factor": 1.0},
            {"name": "Offboard", "cost_factor": 1.0, "setting_up_time_factor": 1.0}
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
    reference_cost=700000 #[$] Cost of the Rosa robot, how much does the 
    total_cost = reference_cost+reference_cost*sum(option["cost_factor"]-1.0 for option in combination)
    # for option in combination:
    #     print(option["cost_factor"])
    # print(combination)
    reference_setting_up_time=30 #[min] assumption setting up time  of the J&J robot
    total_setting_up_time = reference_setting_up_time+reference_setting_up_time*sum(option["setting_up_time_factor"]-1.0 for option in combination)

    total_performance = total_setting_up_time
    name = ""
    selected_options = [option["name"] for option in combination]
    print(selected_options)
    if selected_options == ["Free Standing","CT Scan","Onboard","Onboard"]:
        name = "ROSA"
    if selected_options == ["Free Standing","X-ray","Onboard","Onboard"]:
        name = "MAKO"
    if selected_options == ["On Bed","Imageless","Offboard","Offboard"]:
        name = "J&J"


    design = {
        "Name":name,
        "Selected Options": selected_options,
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
