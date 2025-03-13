import json


with open('reference_designs.json', 'r') as file:
    reference_designs = json.load(file)

for i, design in enumerate(reference_designs):
    total_performance = ((120-design["Estimated Setting up Time"])/110+(2-design["Estimated Accuracy"])/1.95+design["Estimated Experience"]/10)/3
    reference_designs[i]["Performance"]=total_performance
    print(design)
    print(total_performance)

# Save results to a JSON file
with open("reference_designs.json", "w") as json_file:
    json.dump(reference_designs, json_file, indent=4)

