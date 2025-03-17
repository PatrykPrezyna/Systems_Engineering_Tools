import json
import itertools
import math
import pandas as pd

#config
# Load config
with open('input_data/config.json', 'r') as file:
    config = json.load(file)

# Load decisions, options and metrics estimations
with open('output_data/designs.json', 'r') as file:
    designs = json.load(file)

new_designs = []
performance = 0
for i, design in enumerate(designs): # for every design point
    new_design = {
        "Name":design["Name"],
        "Selected Options": design["Selected Options"],
        "Cost": design["Cost"],
        }
    for metric in config["metrics"]:
        metric_value = design[metric["name"]]
        new_design.update({metric["name"]: metric_value})
        # normalise to 0-1
        metric_value = (metric_value-metric["min"])/(metric["max"]-metric["min"])
        if metric["invert"]=="True":
             metric_value = 1 - metric_value
        # new_design.update({metric["name"]: metric_value}) # test
        performance = performance + metric_value*metric["weight"]
    performance = performance/len(config["metrics"])
    new_design.update({"Performance": performance})
    new_designs.append(new_design)

# Save results to a JSON file
with open("output_data/designs.json", "w") as json_file:
    json.dump(new_designs, json_file, indent=4)