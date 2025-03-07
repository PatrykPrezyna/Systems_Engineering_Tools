import json
import itertools
import math
import pandas as pd
import numpy as np

rng = np.random.default_rng()

# Load decisions, options and metrics estimations
with open('input_data/decisions.json', 'r') as file:
    decisions = json.load(file)
# Load selected concepts - data points
with open('input_data/selected_designs.json', 'r') as file:
    selected_designs = json.load(file)

#config
NUMBER_OF_MONTE_CARLO_RUNS = 10
#config

new_design_points = []
for i, design_point in enumerate(selected_designs):
    ergonomics = [] #TODO: exted for more metrics
    costs = []
    for j, decision in enumerate(decisions):
        print("Distribution for: " + str(design_point["Selected Options"][j]))
        for option in decisions[j]["Options"]:
            if option["name"].split('|')[0]==design_point["Selected Options"][j].split('|')[0]: # check only the number like "OP1.1"
                #COST #TODO IT IS A SIMPLIFICATION !!!
                costs.append(option["cost"]["mean"])
                #TODO create a graph (distribution function) for each option (for ergonomics) - only one iteration
                #ERGOMETRICS
                if option["ergonomics"]["Probability Density Function"] != "none":
                    print(option["ergonomics"]["Probability Density Function"])
                    print("mean: " + str(option["ergonomics"]["mean"]))
                    mean = option["ergonomics"]["mean"]
                    if option["ergonomics"]["Probability Density Function"] == "normal":
                        print("sigma: " + str(option["ergonomics"]["sigma"]))
                        sigma = option["ergonomics"]["sigma"]
                        ergonomics.append(rng.normal(mean, sigma, NUMBER_OF_MONTE_CARLO_RUNS))#monte carlo here 
                    if option["ergonomics"]["Probability Density Function"] == "beta":
                        print("alfa: " + str(option["ergonomics"]["alfa"]))
                        #alfa
                        print("beta: " + str(option["ergonomics"]["beta"]))
                        ergonomics.append(rng.beta(option["ergonomics"]["alfa"], option["ergonomics"]["beta"], NUMBER_OF_MONTE_CARLO_RUNS))#monte carlo here 
                        #TODO: monte carlo here 

    #sumup costs per option
    cost_average = 135200 + sum(costs)
    #sumup ergonomics
    ergonomics_average = []
    #ergonomics = [[1,2,3],[4,5,6]] # test
    for i in range(len(ergonomics[0])): # for each monte carlo run
        ergonomics_sum_temp = 0
        for j in range(len(ergonomics)): # for each option
            ergonomics_sum_temp  = ergonomics_sum_temp  + ergonomics[j][i]
        ergonomics_average.append(ergonomics_sum_temp/len(ergonomics))
            #summary[i]=ergonomics[i][0]+ergonomics[i][1]+ergonomics[i][1]
    print("ergonomics_average: " + str(ergonomics_average))
    

    # ergonomics_average = []
    # for j, ergonomic in enumerate(ergonomics):
    #     ergonomics_average.append(sum(ergonomics))
    # # ergonomics_average = ergonomics_average/j
    # print(ergonomics_average)
    new_design_point = {
        "Name":design_point["Name"],
        "Selected Options": design_point["Selected Options"],
        "Estimated Cost": cost_average,#simulation for now
        "Estimated Interoperative Overhead": i,#simulation for now
        "Ergonomics": ergonomics_average,#result
        "Estimated Performance": i,#simulation for now
    }
    new_design_points.append(new_design_point)
    #break#TODO extend for all design points

# Save results to a JSON file
with open("output_data/designs.json", "w") as json_file:
    json.dump(new_design_points, json_file, indent=4)
print("Designs saved to 'designs.json'")

# # Generate all combinations of options (one from each decision)
# combinations = list(itertools.product(*decisions))

# # Calculate cost and performance for each combination
# designs = []
# for combination in combinations:
#     # COST
#     reference_cost=250000 #[$] Cost of the Valys J&J robot, how much does the 
#     total_cost = reference_cost+sum(option["cost"] for option in combination)
#     # SETTING UP TIME
#     reference_interoperative_overhead=30 #[min] assumption setting up time  of the J&J robot
#     total_interoperative_overhead = reference_interoperative_overhead+sum(option["interoperative_overhead"] for option in combination)
#     if total_interoperative_overhead > 120:
#         total_interoperative_overhead = 120
#     if total_interoperative_overhead < 10:
#         total_interoperative_overhead = 10
#     #ergonomics
#     reference_ergonomics = 0.5#[mm] cutting ergonomics
#     total_ergonomics = reference_ergonomics
#     for option in combination:
#         total_ergonomics = total_ergonomics*option["ergonomics"]
#     if total_ergonomics < 0.05:
#         total_ergonomics = 0.5  
#     if total_ergonomics >= 2.0:
#         total_ergonomics = 2.0    
#     # PERFORMENCE
#     total_performance = ((120-reference_interoperative_overhead)/110+(2.0-total_ergonomics)/1.95)/2
    
#     name = ""
#     selected_options = [option["name"] for option in combination]

#     design = {
#         "Name":name,
#         "Selected Options": selected_options,
#         "Estimated Cost": total_cost,
#         "Estimated Interoperative Overhead": total_interoperative_overhead,
#         "Estimated Ergonomics": total_ergonomics,
#         "Estimated Performance": total_performance,
#     }
#     designs.append(design)

# # Save results to a JSON file
# with open("output_data/designs.json", "w") as json_file:
#     json.dump(designs, json_file, indent=4)
# print("Designs saved to 'designs.json'")

# # Flatten the JSON data
# rows = []
# for decision in decisions:
#     decision_name = decision["Decision"]
#     for option in decision["Options"]:
#         row = {
#             "Decision": decision_name,
#             "Option Name": option["name"],
#             "Cost PDF": option["cost"]["Probability Density Function"],
#             "Interoperative Overhead PDF": option["interoperative_overhead"]["Probability Density Function"],
#             "Ergonomics PDF": option["ergonomics"]["Probability Density Function"]
#         }
#         rows.append(row)
# # Create DataFrame
# df = pd.DataFrame(rows)
# # Save to Excel
# df.to_excel("output_data/decision_options.xlsx", index=False)
# print("Excel file 'decision_options.xlsx' created successfully.")