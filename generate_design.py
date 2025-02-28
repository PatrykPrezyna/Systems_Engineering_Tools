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
    total_cost = reference_cost+sum(option["cost_factor"] for option in combination)
    # SETTING UP TIME
    reference_setting_up_time=30 #[min] assumption setting up time  of the J&J robot
    total_setting_up_time = reference_setting_up_time+sum(option["setting_up_time_factor"] for option in combination)
    if total_setting_up_time > 120:
        total_setting_up_time = 120
    if total_setting_up_time < 10:
        total_setting_up_time = 10
    #ACCURACY
    reference_accuracy_factor = 0.5#[mm] cutting accuracy
    total_accuracy_factor = reference_accuracy_factor
    for option in combination:
        total_accuracy_factor = total_accuracy_factor*option["accuracy_factor"]
    if total_accuracy_factor < 0.05:
        total_accuracy_factor = 0.5  
    if total_accuracy_factor >= 2.0:
        total_accuracy_factor = 2.0    
    # EXPIRIENCE               )
    reference_experience_factor=5 #assumption expirience of the J&J robot
    total_experience_factor = reference_experience_factor+sum(option["experience_factor"] for option in combination)
    if total_experience_factor > 10:
        total_experience_factor = 10
    if total_experience_factor < 0:
        total_experience_factor = 0
    # PERFORMENCE
    total_performance = ((120-reference_setting_up_time)/110+(2.0-total_accuracy_factor)/1.95+total_experience_factor/10)/3
    
    name = ""
    selected_options = [option["name"] for option in combination]

    design = {
        "Name":name,
        "Selected Options": selected_options,
        "Estimated Cost": total_cost,
        "Estimated Setting up Time": total_setting_up_time,
        "Estimated Accuracy": total_accuracy_factor,
        "Estimated Experience": total_experience_factor,
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
            "Cost Factor": option["cost_factor"],
            "Setting Up Time Factor": option["setting_up_time_factor"],
            "Accuracy Factor": option["accuracy_factor"],
            "Experience Factor": option["experience_factor"]
        }
        rows.append(row)
# Create DataFrame
df = pd.DataFrame(rows)
# Save to Excel
df.to_excel("output_data/decision_options.xlsx", index=False)
print("Excel file 'decision_options.xlsx' created successfully.")