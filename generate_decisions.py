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
        "Weighting Latency": weight,
        "Options": options}
    decisions.append(decision)


with open("input_data/decisions.json", "w") as json_file:
    json.dump(decisions, json_file, indent=4)
print("Decisions saved to 'decisions.json'")



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