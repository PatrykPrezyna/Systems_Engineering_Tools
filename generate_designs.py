import json
import itertools
import math
import pandas as pd

def generate_designs_fun():
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
            #Exclusion
            exclude = False
            for exclusion in config["Exclusions"]["list"]:
                if all(item in selected_options for item in exclusion):#config["Exclusions"][0] in selected_options:
                    exclude = True
            if not(exclude) or config["Exclusions"]["enable"]=="False":
                design = {
                    "Name":str(i),
                    "Selected Options": selected_options,
                    }
                designs.append(design)

    print(len(designs))
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
            print(selected_design)

  


    # Save results to a JSON file
    with open("output_data/designs.json", "w") as json_file:
        json.dump(designs, json_file, indent=4)
    print("Designs saved to 'designs.json'")
    return True


if (__name__ == '__main__'):
    print('Executing as standalone script')
    generate_designs_fun()