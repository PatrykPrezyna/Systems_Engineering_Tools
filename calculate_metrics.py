import json
import itertools
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#initialise random number generator
rng = np.random.default_rng()

# Load decisions, options and metrics estimations
with open('input_data/decisions.json', 'r') as file:
    decisions = json.load(file)
# Load selected concepts - data points
with open('input_data/selected_designs.json', 'r') as file:
    selected_designs = json.load(file)

#config
NUMBER_OF_MONTE_CARLO_RUNS = 100
ERGONOMICS_MIN = 0
ERGONOMICS_MAX = 10
OVERHEAD_MIN = 5
OVERHEAD_MAX = 120
#config

new_design_points = []
for i, design_point in enumerate(selected_designs):
    ergonomics = [] #TODO: exted for more metrics
    interoperative_overhead = []
    costs = []
    for j, decision in enumerate(decisions):
        print("Distribution for: " + str(design_point["Selected Options"][j]))
        for option in decisions[j]["Options"]:
            if option["name"].split('|')[0]==design_point["Selected Options"][j].split('|')[0]: # check only the number like "OP1.1"
                #COST
                if option["cost"]["Probability Density Function"] != "none":
                    if option["cost"]["Probability Density Function"] == "normal":
                        costs.append(rng.normal(option["cost"]["mean"], option["cost"]["sigma"], NUMBER_OF_MONTE_CARLO_RUNS))#monte carlo here 
                    elif option["cost"]["Probability Density Function"] == "beta":
                        costs.append(rng.beta(option["cost"]["alfa"], option["cost"]["beta"], NUMBER_OF_MONTE_CARLO_RUNS)*option["cost"]["mean"])#monte carlo here 
                    elif option["cost"]["Probability Density Function"] == "weibull":
                        costs.append(rng.weibull(8.0, NUMBER_OF_MONTE_CARLO_RUNS)*option["cost"]["mean"])#monte carlo here 
                    else:
                        print("Error: Probability Density Function not implemented: " +  str(option["cost"]["Probability Density Function"]))
                #TODO create a graph (distribution function) for each option (for ergonomics) - only one iteration
                #ERGOMETRICS
                if option["ergonomics"]["Probability Density Function"] != "none":
                    if option["ergonomics"]["Probability Density Function"] == "normal":
                        ergonomics.append(rng.normal(option["ergonomics"]["mean"], option["ergonomics"]["sigma"], NUMBER_OF_MONTE_CARLO_RUNS))#monte carlo here 
                    elif option["ergonomics"]["Probability Density Function"] == "beta":
                        ergonomics.append(rng.beta(option["ergonomics"]["alfa"], option["ergonomics"]["beta"], NUMBER_OF_MONTE_CARLO_RUNS)*option["ergonomics"]["mean"])#monte carlo here 
                    else:
                        print("Error: Probability Density Function not implemented: " +  str(option["ergonomics"]["Probability Density Function"]))
                else:
                    ergonomics.append([0]*NUMBER_OF_MONTE_CARLO_RUNS)# ensure alle decisisons are the same length - for applying weighting
                #"interoperative_overhead"
                if option["interoperative_overhead"]["Probability Density Function"] != "none":
                    if option["interoperative_overhead"]["Probability Density Function"] == "normal":
                        interoperative_overhead.append(rng.normal(option["interoperative_overhead"]["mean"], option["interoperative_overhead"]["sigma"], NUMBER_OF_MONTE_CARLO_RUNS))#monte carlo here 
                    elif option["interoperative_overhead"]["Probability Density Function"] == "beta":
                        interoperative_overhead.append(rng.beta(option["interoperative_overhead"]["alfa"], option["interoperative_overhead"]["beta"], NUMBER_OF_MONTE_CARLO_RUNS)*option["interoperative_overhead"]["mean"])#monte carlo here 
                    elif option["interoperative_overhead"]["Probability Density Function"] == "weibull":
                        interoperative_overhead.append(rng.weibull(8.0, NUMBER_OF_MONTE_CARLO_RUNS)*option["interoperative_overhead"]["mean"])#monte carlo here 
                    elif option["interoperative_overhead"]["Probability Density Function"] == "gamma":
                        interoperative_overhead.append(rng.gamma(option["interoperative_overhead"]["shape"], option["interoperative_overhead"]["scale"], NUMBER_OF_MONTE_CARLO_RUNS))#monte carlo here    
                    elif option["interoperative_overhead"]["Probability Density Function"] == "lognormal":
                        interoperative_overhead.append(rng.lognormal(option["interoperative_overhead"]["mean"], option["interoperative_overhead"]["sigma"], NUMBER_OF_MONTE_CARLO_RUNS))#monte carlo here                
                    else:
                        print("Error: Probability Density Function not implemented: " +  str(option["interoperative_overhead"]["Probability Density Function"]))
    #sumup costs per design point
    costs_average = []
    for i in range(len(costs[0])): # for each monte carlo run
        costs_sum_temp = 0
        for j in range(len(costs)): # for each option
            costs_sum_temp  = costs_sum_temp  + costs[j][i]
        costs_average.append(costs_sum_temp)#TODO: confirm the diference in the calculation

    #sumup ergonomics
    ergonomics_average = []
    for i in range(len(ergonomics[0])): # for each monte carlo run
        ergonomics_sum_temp = 0
        for j in range(len(ergonomics)): # for each option
            ergonomics_sum_temp  = ergonomics_sum_temp  + max(min(ERGONOMICS_MAX, ergonomics[j][i]), ERGONOMICS_MIN)*decisions[j]["Weighting_ergonomics"] 
        ergonomics_average.append(ergonomics_sum_temp)

    #sumup interoperative_overhead
    interoperative_overhead_average = []
    for i in range(len(interoperative_overhead[0])): # for each monte carlo run
        interoperative_overhead_sum_temp = 0
        for j in range(len(interoperative_overhead)): # for each option
            interoperative_overhead_sum_temp  = interoperative_overhead_sum_temp  + max(min(OVERHEAD_MAX, interoperative_overhead[j][i]), OVERHEAD_MIN) 
        interoperative_overhead_average.append(interoperative_overhead_sum_temp/len(interoperative_overhead))
    
    #sumup performence
    performence = []
    for i in range(len(ergonomics_average)): # for each monte carlo run
        ergonomics = ergonomics_average[i]/ERGONOMICS_MAX
        interoperative_overhead = interoperative_overhead_average[i]/OVERHEAD_MAX#(interoperative_overhead_average[i]-OVERHEAD_MIN)/(OVERHEAD_MAX-OVERHEAD_MIN)
        performence.append(ergonomics*0.6+(1-interoperative_overhead)*0.4)

    new_design_point = {
        "Name":design_point["Name"],
        "Selected Options": design_point["Selected Options"],
        "Estimated Cost": costs_average,#simulation for now
        "Estimated Interoperative Overhead": interoperative_overhead_average,#simulation for now
        "Ergonomics": ergonomics_average,#result
        "Performance": performence,#simulation for now
    }
    new_design_points.append(new_design_point)
    #break#TODO extend for all design points

# Save results to a JSON file
with open("output_data/designs.json", "w") as json_file:
    json.dump(new_design_points, json_file, indent=4)
print("Designs saved to 'designs.json'")


#initialise plot
matrics = ["cost", "ergonomics", "interoperative_overhead"]
metric_units = ["[$]", "[min]", "[?]"]
for p, metric in enumerate(matrics):
    d_in_row = 4
    fig, axs = plt.subplots(nrows=2, ncols=d_in_row, figsize=(40, 20))#TODO make it dependent on the number of options
    fig.suptitle('Probability Density Function: ' + str(metric), fontsize=60) 
    distributions = []
    distributions_labels = []
    k=0

    for j, decision in enumerate(decisions):
        print("Decision: " + str(decision["Decision"]) + ";\nOption: ", str(distributions_labels))
        for option in decisions[j]["Options"]:
            
            #plot probability distribution for each option separately
            if option[metric]["Probability Density Function"] != "none":
                distributions_labels.append(option["name"].split('|')[0])
                if option[metric]["Probability Density Function"] == "normal":
                    temp_distribution = rng.normal(option[metric]["mean"], option[metric]["sigma"], NUMBER_OF_MONTE_CARLO_RUNS)
                elif option[metric]["Probability Density Function"] == "beta":
                    temp_distribution = rng.beta(option[metric]["alfa"], option[metric]["beta"], NUMBER_OF_MONTE_CARLO_RUNS)*option[metric]["mean"] 
                elif option[metric]["Probability Density Function"] == "weibull":
                    temp_distribution = rng.weibull(8.0, NUMBER_OF_MONTE_CARLO_RUNS)*option[metric]["mean"]
                elif option[metric]["Probability Density Function"] == "gamma":
                    temp_distribution = rng.gamma(option[metric]["shape"], option[metric]["scale"], NUMBER_OF_MONTE_CARLO_RUNS)  
                elif option[metric]["Probability Density Function"] == "lognormal":
                    temp_distribution = rng.lognormal(option[metric]["mean"], option[metric]["sigma"], NUMBER_OF_MONTE_CARLO_RUNS)             
                else:
                    print("Error: Probability Density Function not implemented: " +  str(option[metric]["Probability Density Function"]))

                if metric == "cost":
                    temp_distribution = [max(x, 0) for x in temp_distribution]
                if metric == "ergonomics":
                    temp_distribution = [min(max(x, ERGONOMICS_MIN), ERGONOMICS_MAX) for x in temp_distribution]
                if metric == "interoperative_overhead":
                    temp_distribution = [min(max(x, OVERHEAD_MIN), OVERHEAD_MAX)for x in temp_distribution]
                distributions.append(temp_distribution)
        # for i, distribution in enumerate(distributions):
        #     #break
        #     print("distributions:" + str(distributions))
        #     for j, value in enumerate(distribution):
                
        #         if distributions[i][j]  < 0:
        #             distributions[i][j] = 0
        #         if distributions[i][j]  > 10.0:
        #             distributions[i][j] = 10.1
        #     print("distributions:" + str(distributions))

        if distributions != []:
            if j>=d_in_row: k=1
            axs[k][j%d_in_row].violinplot(distributions,
                        showmeans=True,
                        showmedians=True)
            axs[k][j%d_in_row].set_title("Decision: " + str(decision["Decision"]),fontsize=25)
            axs[k][j%d_in_row].yaxis.grid(True)
            axs[k][j%d_in_row].set_xticks([y + 1 for y in range(len(distributions))],
                        labels=distributions_labels)
            axs[k][j%d_in_row].set_xlabel('Options')
            axs[k][j%d_in_row].set_ylabel(str(metric)+ str(metric_units[p]))
            distributions = []
            distributions_labels = []


    file_name = "output_data/Options_PDF_" +str(metric) + ".png"
    plt.savefig(file_name)
    plt.close('all')
# #TODO: print the cumulative distribution