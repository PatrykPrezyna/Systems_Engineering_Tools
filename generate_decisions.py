import json
import itertools
import math
import pandas as pd

#config
# Load decisions, options and metrics estimations
with open('input_data/config.json', 'r') as file:
    config = json.load(file)

# Load decisions, options and metrics estimations
# with open('input_data/decisions.json', 'r') as file:
#     data = json.load(file)
decisions = []
for ide, decision in enumerate(config["decisions"]):
    options = []
    for io, option in enumerate(decision["options"]):
        metrics = []
        for metric in config["metrics"]:
            metrics.append({
                    "name":metric["name"],
                    "comment":"xyz",
                    "Probability Density Function": "normal",
                    "mean": (ide+1)*(io+1),
                    "sigma": 0,
                    "alfa": 0,
                    "beta": 0,
                    "shape": 0,
                    "scale": 0},
                )
            print(metrics)
        print(metrics)
        options.append({
                    "name": option["name"], 
                    "enable":"True",                
                    "cost": {
                        "Probability Density Function": "normal",
                        "mean": 0,
                        "sigma": 0,                    
                        "alfa": 0,
                        "beta": 0,
                        "shape": 0,
                        "scale": 0},
                    "metrics": metrics})
    #as a default every decisison has the same weight for every metric: 1/number of decisions
    weight = 1.0 / len(config["decisions"])
    print("weight: " + str(weight))
    decision = {
        "name":decision["name"],
        "enable":"True",
        "Weighting Interoperative Overhead": weight,#TODO generate in a loop for every metric
        "Weighting Ergonomics": weight,
        "Weighting Responsiveness": weight,
        "Options": options}
    decisions.append(decision)


with open("input_data/decisions.json", "w") as json_file:
    json.dump(decisions, json_file, indent=4)
print("Decisions saved to 'decisions.json'")


# # Extract all decisions and their options
# decisions = [decision["Options"] for decision in data]
# # Generate all combinations of options (one from each decision)
# combinations = list(itertools.product(*decisions))

# # Calculate cost and performance for each combination
# designs = []
# interoperative_overhead = 0
# num = 0
# for i, combination in enumerate(combinations):


#     # total_cost = sum(option["cost"]["mean"] for i, option in enumerate(combination) if option["cost"]["Probability Density Function"] != "none")
#     # total_ergonomics = sum(option["ergonomics"]["mean"]*data[i]["Weighting_ergonomics"] for i, option in enumerate(combination) if option["ergonomics"]["Probability Density Function"] != "none")
#     # for option in combination:
#     #     if option["interoperative_overhead"]["Probability Density Function"] != "none":
#     #         interoperative_overhead = interoperative_overhead + option["interoperative_overhead"]["mean"]  
#     #         num = num + 1
#     # total_interoperative_overhead = (interoperative_overhead/num)/OVERHEAD_MAX
#     # num = 0
    
#     performence = total_ergonomics*0.6+(1-total_interoperative_overhead)*0.4

#     selected_options = [option["name"] for option in combination]
#     name = "Name"
#     design = {
#         name:str(i),
#         "Selected Options": selected_options,
#         "Cost": total_cost,
#         }
#     for metric in config["metrics"]:
#         design.update({
#             "Interoperative Overhead": total_interoperative_overhead,
#             "Ergonomics": total_ergonomics,
#             "Performance": performence,
#         })
#     design.update({"Performance": performence})
#     designs.append(design)

# # Save results to a JSON file


# # Flatten the JSON data
# rows = []
# for decision in data:
#     decision_name = decision["Decision"]
#     for option in decision["Options"]:
#         row = {
#             "Decision": decision_name,
#             "Option Name": option["name"],
#             "Cost": option["cost"],
#             "Interoperative Overhead": option["interoperative_overhead"],
#             "Ergonomics": option["ergonomics"]
#         }
#         rows.append(row)
# # Create DataFrame
# df = pd.DataFrame(rows)
# # Save to Excel
# df.to_excel("output_data/decision_options.xlsx", index=False)
# print("Excel file 'decision_options.xlsx' created successfully.")