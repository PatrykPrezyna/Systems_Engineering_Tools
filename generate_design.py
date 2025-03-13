import json
import itertools
import math
import pandas as pd

#config
ERGONOMICS_MIN = 0
ERGONOMICS_MAX = 10
OVERHEAD_MIN = 5
OVERHEAD_MAX = 120
#config

# Load decisions, options and metrics estimations
with open('input_data/decisions.json', 'r') as file:
    data = json.load(file)

# Extract all decisions and their options
decisions = [decision["Options"] for decision in data]
# Generate all combinations of options (one from each decision)
combinations = list(itertools.product(*decisions))

# Calculate cost and performance for each combination
designs = []
interoperative_overhead = 0
num = 0
for i, combination in enumerate(combinations):
    total_cost = sum(option["cost"]["mean"] for i, option in enumerate(combination) if option["cost"]["Probability Density Function"] != "none")
    total_ergonomics = sum(option["ergonomics"]["mean"]*data[i]["Weighting_ergonomics"] for i, option in enumerate(combination) if option["ergonomics"]["Probability Density Function"] != "none")
    for option in combination:
        if option["interoperative_overhead"]["Probability Density Function"] != "none":
            interoperative_overhead = interoperative_overhead + option["interoperative_overhead"]["mean"]  
            num = num + 1
    total_interoperative_overhead = (interoperative_overhead/num)/OVERHEAD_MAX
    num = 0
    
    performence = total_ergonomics*0.6+(1-total_interoperative_overhead)*0.4

    selected_options = [option["name"] for option in combination]
    design = {
        "Name":i,
        "Selected Options": selected_options,
        "Estimated Cost": total_cost,
        "Estimated Interoperative Overhead": total_interoperative_overhead,
        "Estimated Ergonomics": total_ergonomics,
        "Estimated Performance": performence,
    }
    designs.append(design)

# Save results to a JSON file
with open("output_data/all_designs.json", "w") as json_file:
    json.dump(designs, json_file, indent=4)
print("Designs saved to 'all_designs.json'")

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