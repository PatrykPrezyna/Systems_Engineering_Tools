import json
import itertools
import math
import pandas as pd

# Load decisions, options and metrics estimations
with open('input_data/decisions.json', 'r') as file:
    decisions = json.load(file)
with open('input_data/config.json', 'r') as file:
    config = json.load(file)


# Flatten the JSON data
rows = []
for decision in decisions:
    for option in decision["Options"]:
        row = {
            "Decision": decision["name"],
            "Option Name": option["name"],
            "Cost": option["cost"]["mean"],
            "Interoperative Overhead": option["metrics"][0]["mean"],
            "Weight Overhead": decision["Weighting Interoperative Overhead"],
            "Ergonomics": option["metrics"][1]["mean"],
            "Weight Ergonomics": decision["Weighting Ergonomics"] 
            }
        rows.append(row)

for metric in config["metrics"]:
    row = {
        "Metric": metric["name"],
        "Weight": metric["weight"],
        "Invert": metric["invert"],
        "Min limit": metric["min"],
        "Max limit": metric["max"]
        }
    rows.append(row)

# Create DataFrame
df = pd.DataFrame(rows)
# Save to Excel
df.to_excel("output_data/generated_decision_options.xlsx", index=False)
print("Excel file 'decision_options.xlsx' created successfully.")