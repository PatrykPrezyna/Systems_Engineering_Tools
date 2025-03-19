import json
import numpy as np
import matplotlib.pyplot as plt
import utility_functions.combine_plots_vertical as combine_plots_vertical

def is_efficient_efficient(points, min_dim=0, max_dim=1):
    """
    Find the pareto-efficient points
    :param costs: An (n_points, n_costs) array
    :return: A (n_points, ) boolean array, indicating whether each point is Pareto efficient
    """
    is_efficient = np.ones(points.shape[0], dtype = bool)
    for i, point in enumerate(points):
        if is_efficient[i]:
            # Check if any other point dominates this point
            dominates = (points[:, min_dim] <= point[min_dim]) & (points[:, max_dim] >= point[max_dim])
            dominates[i] = False  # A point doesn't dominate itself
            is_efficient[i] = ~np.any(dominates & (
                (points[:, min_dim] < point[min_dim]) | (points[:, max_dim] > point[max_dim])
            ))

    return [points[is_efficient], is_efficient]

# Load designs
with open('input_data/selected_designs.json', 'r') as file:
    selected_designs = json.load(file)

with open('output_data/designs.json', 'r') as file:
    designs = json.load(file)

# with open('input_data/reference_designs.json', 'r') as file:
#     reference_designs = json.load(file)

#config
show_selected_designs = False
show_generated_designs = True
ADD_LABEL = True
# show_reference_designs = False
# Select metrics to plot: 0= interoperative_overhead, 1=Ergonomics, 2=Responsiveness, 3=Performance
factor = 3
#config

# Define the utopia point (ideal but unattainable point)
costs = [design['Cost'] for design in designs]
interoperative_overhead = [design['Interoperative Overhead'] for design in designs]
ergonomics = [design['Ergonomics'] for design in designs]
responsiveness = [design['Responsiveness'] for design in designs]
performances = [design['Performance'] for design in designs]

y_axis_values = ['Interoperative Overhead', 'Ergonomics', "Responsiveness", 'Performance']
y_axis_values_pareto = [interoperative_overhead, ergonomics, responsiveness, performances]
reference_color = [
    "#FF8785", "#7BBFFC", "#4EC8DE", "#69C9B9", "#E7B030",
    "#BAC03F", "#E6A6C7", "#D5B480", "#BFD8E5"
]# for each option
reference_color = ['blue','yellow','red', "grey", "yellow", "violet", "grey"]# for each option
reference_color = ['blue','yellow','red', "grey", "violet", "grey"]
decisions = ["surgeon control level", "Robot Mount Type","Pre-op Imaging Type","Procedure Navigation","Sterilisability","User Input type","Onboard vs Offboard Power","Onboard vs Offboard Computing"]

utopia_point = [min(costs), max(y_axis_values_pareto[factor])]
points = np.array(list(zip(costs, y_axis_values_pareto[factor])))
if len(decisions) != len(designs[1]['Selected Options']):#test if the number of decisison is correct
    print("ERORR !!!!!!!!!!!!")
for j in range(len(designs[1]['Selected Options'])):
    unique_options = set()
    for item in designs:
        unique_options.add(item['Selected Options'][j])
    unique_options = sorted(list(unique_options))
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    if show_generated_designs:
        for i, option in enumerate(unique_options):
            costs = [design['Cost'] for design in designs if design['Selected Options'][j]==option]
            y_values = [design[y_axis_values[factor]] for design in designs if design['Selected Options'][j]==option]
            names = [design['Name'] for design in designs if design['Selected Options'][j]==option]
            plot_label = str(option)
            plt.scatter(costs, y_values, c=reference_color[i], label=plot_label, s=15)
            #add label for each design point
            if ADD_LABEL:
                for i, cost in enumerate(costs):
                    if names[i] != "":
                        label_name = names[i]
                        print(label_name)
                        ax.text(costs[i], y_values[i], label_name)
    plt.scatter(*utopia_point, c='gold', s=500, marker="*", label='Utopia Point')
    #for selected design
    if show_selected_designs:
        costs = [design['Cost'] for design in selected_designs]
        y_values = [design[y_axis_values[factor]] for design in selected_designs]
        names = [design['Name'] for design in selected_designs]
        #names = [design['Name'].partition("|")[0] for design in selected_designs]
        plt.scatter(costs, y_values, c='red',s=100, marker="X", label="selected designs")
        # add label for each design point
        for i, cost in enumerate(costs):
            if names[i] != "":
                label_name = "" + str(names[i])
                print(label_name)
                ax.text(costs[i], y_values[i], label_name, size=13) 
    # if show_reference_designs:
    #     #for ref design
    #     costs = [design['Cost'] for design in reference_designs]
    #     y_values = [design[y_axis_values[factor]] for design in reference_designs]
    #     names = [design['Name'] for design in reference_designs]
    #     #names = [design['Name'].partition("|")[0] for design in reference_designs]
    #     plt.scatter(costs, y_values, c='orange',s=100, marker="X", label="reference designs")
    #     # add label for each design point
    #     for i, cost in enumerate(costs):
    #         if names[i] != "":
    #             label_name = "" + str(names[i])
    #             print(label_name)
    #             ax.text(costs[i], y_values[i], label_name, size=13)  

    pareto = is_efficient_efficient(points)
    pareto_points = pareto[0]
    xs, ys = zip(*sorted(zip(pareto_points[:, 0], pareto_points[:, 1])))
    plt.plot(xs, ys, 'r--', label='Pareto Frontier')
    plt.scatter(pareto_points[:, 0], pareto_points[:, 1], facecolors='none', edgecolors='green',marker = 'X', s=100, label='Pareto Points')
    

    # Add labels and title
    plt.xlabel('Cost')
    plt.ylabel(y_axis_values[factor])
    title = 'Tradespace for architectural decision: ' + str(decisions[j])
    if show_generated_designs == False:
        title = 'Tradespace for architectural decisions'
    plt.title(title)
    plt.legend()
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

combine_plots_vertical.get_concat_v(y_axis_values[factor])
plt.close('all')
# Show the plot
# plt.show()
