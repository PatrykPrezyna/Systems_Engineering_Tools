import json
import itertools
import math

# JSON data
data = [
    {
        "Decision": "surgeon control level",
        "Options": [
            {"name": "Orientation", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference 1-10
            {"name": "Orientation + depth", "cost_factor": 200000, "setting_up_time_factor": 10, "accuracy_factor": 0.5, "experience_factor": -2.0},#surgeron want more control not less
            {"name": "only support ", "cost_factor": -100000, "setting_up_time_factor": 0, "accuracy_factor": 2, "experience_factor": 4.0},
            {"name": "Only Information", "cost_factor": -100000, "setting_up_time_factor": 0, "accuracy_factor": 2, "experience_factor": 2.0},
        ],
    },
    {
        "Decision": "Robot Mount Type",
        "Options": [
            {"name": "On Bed", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
            {"name": "Free Standing", "cost_factor": 300000, "setting_up_time_factor": -10, "accuracy_factor": 0.5, "experience_factor": 3.0},#flor space, more settings, toller or shorter person
            {"name": "Hand Held", "cost_factor": -50000, "setting_up_time_factor": -10, "accuracy_factor": 2.0, "experience_factor": 5.0},
        ],
    },
    {
        "Decision": "Pre-op Imaging Type",
        "Options": [
            {"name": "CT Scan", "cost_factor": 50000, "setting_up_time_factor": 0, "accuracy_factor": 0.8, "experience_factor": -2.0},#rationale: software incorporating the images costs
            {"name": "Imageless", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference #assume the surgeron is making the marker measuring
            {"name": "X-ray", "cost_factor": 70000, "setting_up_time_factor": 0, "accuracy_factor": 0.8, "experience_factor": -2.0},
            {"name": "MRI", "cost_factor": 60000, "setting_up_time_factor": 0, "accuracy_factor": 0.8, "experience_factor": -2.0},
            #idea: lets reduce the decisison to image less or "X-ray or CT scan or MRI"
        ],
    },
    {
        "Decision": "Procedure Imaging Type",
        "Options": [
            {"name": "3D Volumetric imaging", "cost_factor": 200000, "setting_up_time_factor": -15, "accuracy_factor": 1.0, "experience_factor": 2.0},#in case it is perfect 
            # {"name": "Electro Magnetic", "cost_factor": 1.0, "setting_up_time_factor": 1.0, "accuracy_factor": 1.0, "experience_factor": 1.0}, # reaserach needed
            {"name": "IR Markers", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
            {"name": "accelometers, giroscope", "cost_factor": -50000, "setting_up_time_factor": 10, "accuracy_factor": 1.0, "experience_factor": 0.0},
        ],
    },
    {
        "Decision": "Sterilisability",
        "Options": [
            {"name": "entire device", "cost_factor": 100000, "setting_up_time_factor": -25, "accuracy_factor": 1.0, "experience_factor": 2.0},
            {"name": "tool only", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
            {"name": "nothing", "cost_factor": 0, "setting_up_time_factor": 15, "accuracy_factor": 1.0, "experience_factor": -3.0},
        ],
    },
    {
        "Decision": "User Input type",
        "Options": [
            {"name": "surgeron only", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 3.0},
            {"name": "with OR stuff", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
        ],
    },
    {
        "Decision": "Onboard vs Offboard Power",
        "Options": [
            {"name": "Onboard", "cost_factor": 20000, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},
            {"name": "Offboard", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
        ],
    },
    {
        "Decision": "Onboard vs Offboard Computing",
        "Options": [
            {"name": "Onboard", "cost_factor": 30000, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},
            {"name": "Offboard", "cost_factor": 0, "setting_up_time_factor": 0, "accuracy_factor": 1.0, "experience_factor": 0.0},#reference
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
    # EXPIRIENCE               )
    reference_experience_factor=5 #assumption expirience of the J&J robot
    total_experience_factor = reference_experience_factor+sum(option["experience_factor"] for option in combination)
    if total_experience_factor > 10:
        total_experience_factor = 10
    if total_experience_factor < 0:
        total_experience_factor = 0
    # PERFORMENCE
    total_performance = (reference_setting_up_time/total_setting_up_time+reference_accuracy_factor/total_accuracy_factor+total_experience_factor/reference_experience_factor)/3
    
    name = ""
    selected_options = [option["name"] for option in combination]
    if selected_options == ["Orientation + depth","Free Standing","CT Scan","IR Markers","tool only","with OR stuff","Onboard","Onboard"]:
        name = "ROSA"
        print(name + " -total_cost: " + str(total_cost) + " -total_performance: " + str(total_performance) + " -total_setting_up_time: " + str(total_setting_up_time) + " -total_accuracy_factor: " + str(total_accuracy_factor))
    if selected_options == ["Orientation + depth","Free Standing","X-ray","IR Markers","tool only","with OR stuff","Onboard","Onboard"]:
        name = "MAKO"
        print(name + " -total_cost: " + str(total_cost) + " -total_performance: " + str(total_performance) + " -total_setting_up_time: " + str(total_setting_up_time) + " -total_accuracy_factor: " + str(total_accuracy_factor))
    if selected_options == ["Orientation","On Bed","Imageless","IR Markers","tool only","with OR stuff","Offboard","Offboard"]:
        name = "J&J"
        print(name + " -total_cost: " + str(total_cost) + " -total_performance: " + str(total_performance) + " -total_setting_up_time: " + str(total_setting_up_time) + " -total_accuracy_factor: " + str(total_accuracy_factor))
    if selected_options == ["Orientation","Hand Held","X-ray","IR Markers","tool only","with OR stuff","Offboard","Offboard"]:
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
