import json
import numpy as np
import matplotlib.pyplot as plt
import combine_plots

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

# Load designs.json
with open('designs.json', 'r') as file:
#with open('reference_designs.json', 'r') as file:
    designs = json.load(file)

# Define the utopia point (ideal but unattainable point)
costs = [design['Estimated Cost'] for design in designs]
setting_up_times = [design['Estimated Setting up Time'] for design in designs]
accuracies = [design['Estimated Accuracy'] for design in designs]
experiences = [design['Estimated Experience'] for design in designs]
performances = [design['Estimated Performance'] for design in designs]


y_axis_values = ['Estimated Setting up Time', 'Estimated Accuracy', 'Estimated Experience', 'Estimated Performance']
y_axis_values_pareto = [setting_up_times, accuracies, experiences, performances]
reference_color = ['blue','yellow','red', "grey", "yellow", "violet", "grey"]# for each option
decisions = ["surgeon control level", "Robot Mount Type","Pre-op Imaging Type","Procedure Imaging Type","Sterilisability","User Input type","Onboard vs Offboard Power","Onboard vs Offboard Computing"]


factor = 3
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
    for i, option in enumerate(unique_options):
        costs = [design['Estimated Cost'] for design in designs if design['Selected Options'][j]==option]
        y_values = [design[y_axis_values[factor]] for design in designs if design['Selected Options'][j]==option]
        names = [design['Name'] for design in designs if design['Selected Options'][j]==option]
        plot_label = str(option)
        plt.scatter(costs, y_values, c=reference_color[i], label=plot_label)
        # add label for each design point
        for i, cost in enumerate(costs):
            if names[i] != "":
                label_name = names[i]
                ax.text(costs[i], y_values[i], label_name)
    plt.scatter(*utopia_point, c='green', s=100, label='Utopia Point')

    pareto = is_efficient_efficient(points)
    pareto_points = pareto[0]
    xs, ys = zip(*sorted(zip(pareto_points[:, 0], pareto_points[:, 1])))
    plt.plot(xs, ys, 'r--', label='Pareto Frontier')
    plt.scatter(pareto_points[:, 0], pareto_points[:, 1], facecolors='none', edgecolors='green',marker = 'X', s=100, label='Pareto Points')
    

    # Add labels and title
    plt.xlabel('Estimated Cost')
    plt.ylabel(y_axis_values[factor])
    title = 'Tradespace for architectural decision: ' + str(decisions[j])
    plt.title(title)
    plt.legend()
    plt.grid(True)


    file_name = "Tradespace" + str(j) + ".png"
    plt.savefig(file_name)

pareto_designs = []
unique_pareto_designs = []
unique_performence = []
for i, is_pareto in enumerate(pareto[1]):
    if is_pareto:
        pareto_designs.append(designs[i])
        print(designs[i]["Estimated Performance"])
        if designs[i]["Estimated Performance"] not in  unique_performence:
            unique_pareto_designs.append(designs[i])
            unique_performence.append(designs[i]["Estimated Performance"])

        # print(is_pareto)
        # print(designs[i])


print(len(pareto_designs))
print(len(unique_pareto_designs))

with open("pareto_designs.json", "w") as json_file:
    json.dump(pareto_designs, json_file, indent=4)

with open("unique_pareto_designs.json", "w") as json_file:
    json.dump(unique_pareto_designs, json_file, indent=4)

combine_plots.get_concat_v(y_axis_values[factor])
plt.close('all')
# Show the plot
# plt.show()
