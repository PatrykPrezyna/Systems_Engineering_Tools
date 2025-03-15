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

new_designs = []
for i, design in enumerate(designs): # for every design point
    total_cost = 0
    
    total_metrics = [0, 0, 0]
    avg_total_metrics = [0, 0, 0]
    metrics_relevant_decisions = [0, 0, 0]
    performance = 0
    for j, option in enumerate(design["Selected Options"]): # for each decisison
        for one_option in decisions[j]["Options"]: 
            if one_option["name"] == option: # select option from decisison file
                total_cost = total_cost + one_option["cost"]["mean"]
                #for every metric: ehen PDS not noe
                for m, metric in enumerate(config["metrics"]):
                    if one_option["metrics"][m]["Probability Density Function"] != "none":
                        metrics_relevant_decisions[m] = metrics_relevant_decisions[m] + 1
                        metric_value = min(max(one_option["metrics"][m]["mean"], metric["min"]), metric["max"])
                        total_metrics[m] = total_metrics[m] + metric_value*decisions[j]["Weighting " + one_option["metrics"][m]["name"]]#TODO: test the order of metrics in config and decisisons

    new_design = {
        "Name":design["Name"],
        "Selected Options": design["Selected Options"],
        "Cost": total_cost,
        }
    for m, total_metric in enumerate(total_metrics):
        avg_total_metrics[m] = total_metric / metrics_relevant_decisions[m]#TODO: check for none
        performance = performance + avg_total_metrics[m]#TODO: add weight from config file
        new_design.update({config["metrics"][m]["name"]: total_metric})
    #TODO test is the "Weighting Interoperative Overhead" has the same name as the metric itself
    performance = performance/len(config["metrics"])
    new_design.update({"Performance": performance})
    new_designs.append(new_design)

# Save results to a JSON file
with open("output_data/designs.json", "w") as json_file:
    json.dump(new_designs, json_file, indent=4)