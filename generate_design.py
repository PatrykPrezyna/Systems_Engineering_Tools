import json
import itertools
import math
import pandas as pd

# JSON data
data = [
    {
        "Decision": "(D1) Surgeon Level Of Control",
        "Options": [
            {"name": "OP 1.1 | Robotic Support Of Orientation And  Depth", "cost_factor": 200000, "setting_up_time_factor": 10, "accuracy_factor": 0.5, "experience_factor": -2.0},#surgeron want more control not less
            {"name": "OP 1.2 | Robotic Support Of Orientation", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference 1-10
            {"name": "OP 1.3 | Robotic Stabilization", "cost_factor": -100000, "setting_up_time_factor": 0, "accuracy_factor": 2, "experience_factor": 4.0},      
            {"name": "OP 1.4 | Weight-Bearing Only", "cost_factor": -60000, "setting_up_time_factor": 0, "accuracy_factor": 2, "experience_factor": 1.0},
            {"name": "OP 1.5 | Non-Robotic", "cost_factor": -100000, "setting_up_time_factor": 0, "accuracy_factor": 2, "experience_factor": 2.0},
        ],
    },
    {
        "Decision": "(D2) Device Mount Type",
        "Options": [
            {"name": "OP 2.1 | On Bed", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
            {"name": "OP 2.2 | Free Standing", "cost_factor": 300000, "setting_up_time_factor": -10, "accuracy_factor": 0.5, "experience_factor": 3.0},#flor space, more settings, toller or shorter person
            {"name": "OP 2.3 | Handheld", "cost_factor": -50000, "setting_up_time_factor": -10, "accuracy_factor": 2.0, "experience_factor": 5.0},
        ],
    },
    {
        "Decision": "(D3) Pre-operation Imaging Type",
        "Options": [
            {"name": "OP 3.1 | Pre-Op Imaging Needed", "cost_factor": 50000, "setting_up_time_factor": 0, "accuracy_factor": 0.8, "experience_factor": -2.0},#rationale: software incorporating the images costs
            {"name": "OP 3.2 | Imageless", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference #assume the surgeron is making the marker measuring
        ],
    },
    {
        "Decision": "(D4) Procedure Imaging Type",
        "Options": [
            {"name": "OP 4.1 | IR Markers", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
            {"name": "OP 4.2 | Accelerometers", "cost_factor": -50000, "setting_up_time_factor": 10, "accuracy_factor": 1.0, "experience_factor": 0.0},
            {"name": "OP 4.3 | 3D Scanning", "cost_factor": 200000, "setting_up_time_factor": -15, "accuracy_factor": 1.0, "experience_factor": 2.0},#in case it is perfect 
            {"name": "OP 4.4 | Imageless", "cost_factor": 1.0, "setting_up_time_factor": 1.0, "accuracy_factor": 1.0, "experience_factor": 1.0}, # reaserach needed
        ],
    },
    {
        "Decision": "(D7) Sterilizable Components ",
        "Options": [
            {"name": "OP 7.1 | Entire Device", "cost_factor": 100000, "setting_up_time_factor": -25, "accuracy_factor": 1.0, "experience_factor": 2.0},
            {"name": "OP 7.2 | Device is sterilizable, disposable components exists", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
            {"name": "OP 7.3 | Everything Is Disposable Or Needs Draping", "cost_factor": 0, "setting_up_time_factor": 15, "accuracy_factor": 1.0, "experience_factor": -3.0},
        ],
    },
    {
        "Decision": "(D8) User Input Type",
        "Options": [
            {"name": "OP 8.1 | Surgeon Only", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 3.0},
            {"name": "OP 8.2 | OR Staff Support", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
        ],
    },
    {
        "Decision": "(D9) Onboard vs Offboard Power",
        "Options": [
            {"name": "OP 9.1 | Onboard", "cost_factor": 20000, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},
            {"name": "OP 9.2 | Offboard", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
        ],
    },
    {
        "Decision": "(D10) Onboard vs Offboard Computing",
        "Options": [
            {"name": "OP 10.1 | Onboard", "cost_factor": 30000, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},
            {"name": "OP 10.2 | Offboard", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
        ],
    }
]

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
    #selected_options = [option["name"].partition("|")[0] for option in combination]
    if selected_options == ["Orientation + depth","Free Standing","Pre-Op imaging needed","IR Markers","tool only","with OR stuff","Onboard","Onboard"]:
        name = "ROSA"
        print(name + " -total_cost: " + str(total_cost) + " -total_performance: " + str(total_performance) + " -total_setting_up_time: " + str(total_setting_up_time) + " -total_accuracy_factor: " + str(total_accuracy_factor))
    if selected_options == ["Orientation + depth","Free Standing","Pre-Op imaging needed","IR Markers","tool only","with OR stuff","Onboard","Onboard"]:
        name = "MAKO"
        print(name + " -total_cost: " + str(total_cost) + " -total_performance: " + str(total_performance) + " -total_setting_up_time: " + str(total_setting_up_time) + " -total_accuracy_factor: " + str(total_accuracy_factor))
    if selected_options == ["Orientation","On Bed","Imageless","IR Markers","tool only","with OR stuff","Offboard","Offboard"]:
        name = "Valys_J&J"
        print(name + " -total_cost: " + str(total_cost) + " -total_performance: " + str(total_performance) + " -total_setting_up_time: " + str(total_setting_up_time) + " -total_accuracy_factor: " + str(total_accuracy_factor))
    if selected_options == ["Orientation","Hand Held","Pre-Op imaging needed","IR Markers","tool only","with OR stuff","Offboard","Offboard"]:
        name = "Tmini"
        print(name + " -total_cost: " + str(total_cost) + " -total_performance: " + str(total_performance) + " -total_setting_up_time: " + str(total_setting_up_time) + " -total_accuracy_factor: " + str(total_accuracy_factor))


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

# Print results
# for i, design in enumerate(designs, start=1):
#     print(f"Design {i}:")
#     print(f"  Selected Options: {design['Selected Options']}")
#     print(f"  Estimated Cost: {design['Estimated Cost']}")
#     print(f"  Estimated Performance: {design['Estimated Performance']}")
#     print()

# Save results to a JSON file
with open("designs.json", "w") as json_file:
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
df.to_excel("decision_options.xlsx", index=False)

print("Excel file 'decision_options.xlsx' created successfully.")