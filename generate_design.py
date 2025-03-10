import json
import itertools
import math
import pandas as pd

# Load decisions, options and metrics estimations
with open('input_data/decisions.json', 'r') as file:
    data = json.load(file)

# Extract all decisions and their options
decisions = [decision["Options"] for decision in data]

# Generate all combinations of options (one from each decision)
combinations = list(itertools.product(*decisions))

# Calculate cost and performance for each combination
designs = []
for combination in combinations:
    # COST
    reference_cost=250000 #[$] Cost of the Valys J&J robot, how much does the 
    total_cost = reference_cost+sum(option["cost"] for option in combination)
    # SETTING UP TIME
    reference_interoperative_overhead=30 #[min] assumption setting up time  of the J&J robot
    total_interoperative_overhead = reference_interoperative_overhead+sum(option["interoperative_overhead"] for option in combination)
    if total_interoperative_overhead > 120:
        total_interoperative_overhead = 120
    if total_interoperative_overhead < 10:
        total_interoperative_overhead = 10
    #ergonomics
    reference_ergonomics = 0.5#[mm] cutting ergonomics
    total_ergonomics = reference_ergonomics
    for option in combination:
        total_ergonomics = total_ergonomics*option["ergonomics"]
    if total_ergonomics < 0.05:
        total_ergonomics = 0.5  
    if total_ergonomics >= 2.0:
        total_ergonomics = 2.0    
    # PERFORMENCE
    total_performance = ((120-reference_interoperative_overhead)/110+(2.0-total_ergonomics)/1.95)/2
    
    name = ""
    selected_options = [option["name"] for option in combination]

    design = {
        "Name":name,
        "Selected Options": selected_options,
        "Estimated Cost": total_cost,
        "Estimated Interoperative Overhead": total_interoperative_overhead,
        "Estimated Ergonomics": total_ergonomics,
        "Estimated Performance": total_performance,
    }
    designs.append(design)

# Save results to a JSON file
with open("output_data/designs.json", "w") as json_file:
    json.dump(designs, json_file, indent=4)
print("Designs saved to 'designs.json'")

# Flatten the JSON data
rows = []
for decision in data:
    decision_name = decision["Decision"]
    for option in decision["Options"]:
        row = {
            "Decision": decision_name,
            "Option Name": option["name"],
            "Estimated Cost": option["cost"],
            "Interoperative Overhead": option["interoperative_overhead"],
            "Ergonomics": option["ergonomics"]
        }
        rows.append(row)
# Create DataFrame
df = pd.DataFrame(rows)
# Save to Excel
df.to_excel("output_data/decision_options.xlsx", index=False)
print("Excel file 'decision_options.xlsx' created successfully.")