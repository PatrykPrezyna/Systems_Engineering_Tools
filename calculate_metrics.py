import json
import itertools
import math
import pandas as pd

#config
# Load config
with open('input_data/config.json', 'r') as file:
    config = json.load(file)

# Load decisions, options and metrics estimations
with open('input_data/decisions.json', 'r') as file:
    decisions = json.load(file)

# Load decisions, options and metrics estimations
with open('output_data/designs.json', 'r') as file:
    designs = json.load(file)

# TESTs:
# Test if the sum of all decisisosn weights per metric:
#a adds up to 1: average calculation 
#b all are 1 or 2: simple sum

new_designs = []
for i, design in enumerate(designs): # for every design point
    total_cost = 0
    total_metrics = [0, 0, 0]
    for j, option in enumerate(design["Selected Options"]): # for each option within the design point
        for decision_option in decisions[j]["Options"]: # for each option within decisison
            if decision_option["name"] == option:
                # TO DO implement uncertainty / probability dencity function
                total_cost = total_cost + decision_option["cost"]["mean"] # take mean if no PDF is selected
                #for every metric
                for m, metric in enumerate(config["metrics"]):
                    for option_metric in decision_option["metrics"]:  # for each metric within an option
                        if option_metric["name"] == metric["name"]:
                            metric_value = min(max(option_metric["mean"], metric["min"]), metric["max"])
                            total_metrics[m] = total_metrics[m] + metric_value*decisions[j]["Weighting " + decision_option["metrics"][m]["name"]]
    # Apply the min and max also to the summed metric
    for tm, total_metric in enumerate(total_metrics):
        total_metrics[tm] = min(max(total_metrics[tm], config["metrics"][tm]["min"]), config["metrics"][tm]["max"])
        print(total_metrics[tm])

    new_design = {
        "Name":design["Name"],
        "Selected Options": design["Selected Options"],
        "Cost": total_cost,
        }
    for m, total_metric in enumerate(total_metrics):
        new_design.update({config["metrics"][m]["name"]: total_metric})
    new_designs.append(new_design)

# Save results to a JSON file
with open("output_data/designs.json", "w") as json_file:
    json.dump(new_designs, json_file, indent=4)