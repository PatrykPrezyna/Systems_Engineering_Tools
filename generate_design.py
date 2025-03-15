import json
import itertools
import math
import pandas as pd

# Load config
with open('input_data/config.json', 'r') as file:
    config = json.load(file)

# Load decisions & options
with open('input_data/decisions.json', 'r') as file:
    decisions = json.load(file)

# Load selected designs
with open('input_data/selected_designs.json', 'r') as file:
    selected_designs = json.load(file)

# Extract all decisions and their options
options = [decision["Options"] for decision in decisions]
# Generate all combinations of options (one from each decision) #TODO implement enable
combinations = list(itertools.product(*options))

designs = []
if config["Tradespace_options"]["include generated"]=="True":
    for i, combination in enumerate(combinations):
        selected_options = [option["name"] for option in combination]
        design = {
            "Name":str(i),
            "Selected Options": selected_options,
            }
        designs.append(design)

if config["Tradespace_options"]["include selected"]=="True":
    for i, selected_design in enumerate(selected_designs):
        #test and rename options:
        for j, decision in enumerate(decisions):
            exists = False
            for option in decision["Options"]:
                if selected_design["Selected Options"][j] == option["name"].split("|")[0]:
                    selected_design["Selected Options"][j] = option["name"]
                    exists = True
            if not(exists):
                print("ERORO: OPTION DOES NOT EXISTS !!! Option: " + str(selected_design["Selected Options"][j] ) + " Design: " + selected_design["Name"])
        designs.append(selected_design)


# Save results to a JSON file
with open("output_data/designs.json", "w") as json_file:
    json.dump(designs, json_file, indent=4)
print("Designs saved to 'designs.json'")
