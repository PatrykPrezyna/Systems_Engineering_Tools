import json
import numpy as np
import matplotlib.pyplot as plt
import utility_functions.combine_plots_vertical as combine_plots_vertical

def is_efficient_efficient(points, utopia_positive=1):
    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :return: A (n_points, ) boolean array, indicating whether each point is Pareto efficient
    """
    is_efficient = np.ones(points.shape[0], dtype = bool)
    for i, point in enumerate(points):
        if is_efficient[i]:
            # Check if any other point dominates this point
            if utopia_positive:
                dominates = (points[:, 0] <= point[0]) & (points[:, 1] >= point[1])
                is_efficient[i] = ~np.any(dominates & (
                    (points[:, 0] < point[0]) | (points[:, 1] > point[1])
                ))
            else:
                dominates = (points[:, 0] <= point[0]) & (points[:, 1] <= point[1])
                is_efficient[i] = ~np.any(dominates & (
                    (points[:, 0] < point[0]) | (points[:, 1] < point[1])
                ))

            

    return [points[is_efficient], is_efficient]

def tradespace_fun(metric_to_plot):
    # Load designs
    with open('output_data/designs.json', 'r') as file:
        designs = json.load(file)

    with open('input_data/decisions.json', 'r') as file:
        temp_decisions = json.load(file)

    with open('input_data/config.json', 'r') as file:
        config = json.load(file)

    # Define the utopia point (ideal but unattainable point)
    costs = [design['Cost'] for design in designs]
    interoperative_overhead = [design['Interoperative Overhead'] for design in designs]
    ergonomics = [design['Ergonomics'] for design in designs]
    Latency = [design['Latency'] for design in designs]
    performances = [design['Performance'] for design in designs]

    y_axis_values = ['Interoperative Overhead', 'Ergonomics', "Latency", 'Performance']
    y_axis_values_pareto = [interoperative_overhead, ergonomics, Latency, performances]
    metric_limit = [50, 6.0, 0.1, 0] #TODO: load from config
    utopia_positive = [0, 1, 0, 1]#TODO: load from config : 0 means lower metric is better
    reference_color = [
        "#FF8785", "#7BBFFC", "#4EC8DE", "#69C9B9", "#E7B030",
        "#BAC03F", "#E6A6C7", "#D5B480", "#BFD8E5"
    ]# for each option
    reference_color = ['blue','blue','blue', "blue", "blue", "blue"]
    reference_color = ['blue','green','red', "grey", "violet", "grey",'blue','green','red', "grey", "violet", "grey"]
    decisions = ["surgeon control level", "Robot Mount Type","Pre-op Imaging Type","Procedure Navigation","Sterilisability","Onboard vs Offboard Power","Onboard vs Offboard Computing"]
    #TODO: load decisions from config
    if utopia_positive[metric_to_plot]:
        utopia_point = [min(costs), max(y_axis_values_pareto[metric_to_plot])]
    else:
        utopia_point = [min(costs), min(y_axis_values_pareto[metric_to_plot])]
    print("Utopia point: " + str(utopia_point))
    print("Utopia point: " + str(min(y_axis_values_pareto[metric_to_plot])))


    points = np.array(list(zip(costs, y_axis_values_pareto[metric_to_plot])))
    if len(decisions) != len(designs[1]['Selected Options']):#test if the number of decisison is correct
        print("ERORR !!!!!!!!!!!!")
    for j in range(len(designs[1]['Selected Options'])):
        unique_options = set()
        for item in designs:
            unique_options.add(item['Selected Options'][j])
        unique_options = sorted(list(unique_options))
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        for i, option in enumerate(unique_options):
            # show different markers depending on selected option from decisison 0
            dnr = config["Tradespace_options"]["decisison_nr_for_shape"]
            for op, option_decision_1 in enumerate(temp_decisions[dnr]['Options']):
                print("option_decision_1[name]: " + str(option_decision_1["name"]))
                # print("design['Selected Options'][0] : " + str(design['Selected Options'][j]))
                costs = [design['Cost'] for design in designs if design['Selected Options'][j]==option and design['Selected Options'][dnr] == option_decision_1["name"]]
                y_values = [design[y_axis_values[metric_to_plot]] for design in designs if design['Selected Options'][j]==option and design['Selected Options'][dnr] == option_decision_1["name"]]
                names = [design['Name'] for design in designs if design['Selected Options'][j]==option and design['Selected Options'][dnr] == option_decision_1["name"]]
                label = [design['label'] for design in designs if design['Selected Options'][j]==option and design['Selected Options'][dnr] == option_decision_1["name"]]
                dev_time = [((design['dev_time'])*(design['dev_time'])+1)*20 for design in designs if design['Selected Options'][j]==option and design['Selected Options'][dnr] == option_decision_1["name"]]
    
                plot_label = str(option)[:6] + ' + ' + str(option_decision_1["name"])[:10]

                if config["Tradespace_options"]["decisison_shape"] == "True":
                    if op == 0:
                        temp_marker="^"
                    elif op == 1:
                        temp_marker="o"
                    else:
                        temp_marker="s"                 
                else:
                    temp_marker="o"

                if config["Tradespace_options"]["sized_dev_cost"] == "True":
                    marker_size = dev_time
                else:
                    marker_size = 50
                plt.scatter(costs, y_values, c=reference_color[i], label=plot_label, s=marker_size, alpha=0.5, marker=temp_marker)
                #add label for each design point
                for ii, cost in enumerate(costs):
                    if label[ii] == "True":
                        ax.text(costs[ii], y_values[ii], names[ii], fontsize=15)
        plt.scatter(*utopia_point, c='gold', s=500, marker="*", label='Utopia Point')
        #plt.axhline(y=metric_limit[metric_to_plot], color='r', linestyle='--')#(x=80000, ymin=0, ymax=10, linewidth=40, color='r')
        pareto = is_efficient_efficient(points, utopia_positive[metric_to_plot])
        pareto_points = pareto[0]
        xs, ys = zip(*sorted(zip(pareto_points[:, 0], pareto_points[:, 1])))
        plt.plot(xs, ys, 'r--', linewidth=0.5, label='Pareto Frontier')
        plt.scatter(pareto_points[:, 0], pareto_points[:, 1], facecolors='none', edgecolors='green',marker = 'X', s=100, label='Pareto Points')
        

        # Add labels and title
        plt.xlabel('Cost')
        plt.ylabel(y_axis_values[metric_to_plot])
        title = 'Tradespace for architectural decision: ' + str(decisions[j])
        plt.title(title)

        #fig.legend(loc=1)
        fig.legend(loc=1, markerscale=0.8)
        fig.subplots_adjust(right=0.70)   

        plt.grid(True)


        file_name = "output_data/Tradespace" + str(j) + ".png"
        plt.savefig(file_name)

    pareto_designs = []
    unique_pareto_designs = []
    unique_performence = []
    for i, is_pareto in enumerate(pareto[1]):
        if is_pareto:
            pareto_designs.append(designs[i])
            print(designs[i]["Performance"])
            if designs[i]["Performance"] not in  unique_performence:
                unique_pareto_designs.append(designs[i])
                unique_performence.append(designs[i]["Performance"])


    pareto_designs.sort(key=lambda x: x['Performance'], reverse=True)
    unique_pareto_designs.sort(key=lambda x: x['Performance'], reverse=True)

    print(len(pareto_designs))
    print("unique pareto designs: " + str(len(unique_pareto_designs)))

    with open("output_data/pareto_designs.json", "w") as json_file:
        json.dump(pareto_designs, json_file, indent=4)

    with open("output_data/unique_pareto_designs.json", "w") as json_file:
        json.dump(unique_pareto_designs, json_file, indent=4)

    combine_plots_vertical.get_concat_v(y_axis_values[metric_to_plot])
    plt.close('all')
    # Show the plot
    # plt.show()

if (__name__ == '__main__'):
    print('Executing as standalone script')
    tradespace_fun(3) 
    # Select metrics to plot: 0= interoperative_overhead, 1=Ergonomics, 2=Latency, 3=Performance