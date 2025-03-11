import json
import numpy as np
import matplotlib.pyplot as plt
import combine_plots
import combine_plots_vertical

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
with open('output_data/designs.json', 'r') as file:
    designs = json.load(file)

#config
factor =  2 # which metric to plot ["Ergonomics", "Estimated Interoperative Overhead", "Performance"]
EROR_BARS = True #FALSE
EROR_BARS_PERCENTILE = 33
PARETOS = [1] # [1, 0.8, 0.6]
#config
# Define the utopia point (ideal but unattainable point)
#costs = [design['Estimated Cost'] for design in designs]


metrics = ["Ergonomics", "Estimated Interoperative Overhead", "Performance"]
print('Estimated '+str(metrics[factor]))
title = 'Estimated '+str(metrics[factor])
y_axis_values = [title]
y_axis_values_pareto = []
x_axis_values_pareto = []
# reference_color_err = ['black','silver','red', "sienna", "cyan", "plum", 'blue','olive','lawngreen', "green", "brown"]# for each option
#reference_color = ['dimgrey','gainsboro','salmon', "chocolate", "lightcyan", "violet", 'cornflowerblue','darkkhaki','palegreen', "forestgreen", "indianred"]# for each option - error bars
reference_color = [
    "#d0d6b8", "#4caf50", "#a9c3ff", "#d1a8a3", "#5f8ae6",
    "#2aa5a0", "#ff9b4c", "#49d267", "#9b6ef3", "#f2e7aa"
]
reference_color_err = [
    "#6b7740", "#1b3c1c", "#4a5a91", "#7f5651", "#1e3b7a",
    "#004d4d", "#8c4c13", "#1e5e2b", "#4b2d73", "#a89a6e"
]


marker = ['o', '^', 's']
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)

for i, design in enumerate(designs):
    metric_values = design[metrics[factor]]
    costs = design['Estimated Cost']
    plot_label = str(design['Name'])
    # sortedd = np.sort( np.array(metric_values))
    # percentile = 1
    # print(str(percentile) + ": " + str(sortedd[round(len(sortedd)*percentile)]))
    # for i, value in enumerate(metric_values):
    #     if value > sortedd[round(len(sortedd)*percentile)]:
    #         metric_values[i] = 0

    plt.scatter(costs, metric_values, c=reference_color[i%len(reference_color)], marker=marker[round(i/len(reference_color))], label=plot_label, s=6)
    x_axis_values_pareto.extend(costs)
    y_axis_values_pareto.extend(metric_values)
    #plot error bars
    print("percentile x: " + str(np.percentile(costs-np.mean(costs), EROR_BARS_PERCENTILE)))
    print("mean x: " + str(np.mean(costs)))
    print("max x: " + str(np.max(costs)))
    print("min x: " + str(np.min(costs)))
    print("percentile y: " + str(np.percentile(metric_values-np.mean(metric_values), EROR_BARS_PERCENTILE)))
    print("mean y: " + str(np.mean(metric_values)))
    print('************************')
    plt.errorbar(np.mean(costs), np.mean(metric_values),
             xerr=[[10000], [40000]],#np.percentile(costs-np.mean(costs), EROR_BARS_PERCENTILE),
             yerr=[[0.05], [0.03]],#np.percentile(metric_values-np.mean(metric_values), EROR_BARS_PERCENTILE),
             c=reference_color_err[i%len(reference_color_err)],
             capsize = 6, capthick = 2, lw = 1)
    # plt.errorbar(x, y,
    #          yerr=y_error,
    #          xerr=x_error,
    #          fmt='o')  

    #if i >= 0: break

#points = np.array(list(zip(sum(x_axis_values_pareto, []), sum(y_axis_values_pareto,[0]))))
points = np.array([x_axis_values_pareto, y_axis_values_pareto]).T
print(points.shape)
# print("points: " + str(points))
pareto = is_efficient_efficient(points)
pareto_points = pareto[0]
print("pareto points: " + str(pareto_points))
xs, ys = zip(*sorted(zip(pareto_points[:, 0], pareto_points[:, 1])))
plt.plot(xs, ys, 'r--', label='Pareto Frontier')
plt.scatter(xs, ys, facecolors='none', edgecolors='green',marker = 'X', s=100, label='Pareto Points')

utopia_point = [min(x_axis_values_pareto), max(y_axis_values_pareto)]
print("utopia point: " + str(utopia_point))
plt.scatter(utopia_point[0], utopia_point[1], c='gold', s=500, marker="*", label='Utopia Point')

# Add labels and title
plt.xlabel('Estimated Cost [$]')
plt.ylabel(y_axis_values)
title = 'Tradespace'
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.title(title)
#plt.legend()
plt.grid(True)


file_name = "output_data/Tradespace_" + str(metrics[factor]) + ".png"
print(file_name)
plt.savefig(file_name)

# for j in range(len(designs[1]['Selected Options'])):
#     unique_options = set()
#     for item in designs:
#         unique_options.add(item['Selected Options'][j])
#     unique_options = sorted(list(unique_options))

#     if show_generated_designs:
#         for i, option in enumerate(unique_options):
#             costs = [design['Estimated Cost'] for design in designs if design['Selected Options'][j]==option]
#             y_values = [design[y_axis_values[factor]] for design in designs if design['Selected Options'][j]==option]
#             names = [design['Name'] for design in designs if design['Selected Options'][j]==option]
#             plot_label = str(option)
#             plt.scatter(costs, y_values, c=reference_color[i], label=plot_label, s=6)
#             # add label for each design point
#             # for i, cost in enumerate(costs):
#             #     if names[i] != "":
#             #         label_name = names[i]
#             #         print(label_name)
#             #         ax.text(costs[i], y_values[i], label_name)
    
#     #for selected design
#     if show_selected_designs:
#         costs = [design['Estimated Cost'] for design in selected_designs]
#         y_values = [design[y_axis_values[factor]] for design in selected_designs]
#         names = [design['Name'] for design in selected_designs]
#         #names = [design['Name'].partition("|")[0] for design in selected_designs]
#         plt.scatter(costs, y_values, c='red',s=100, marker="X", label="selected designs")
#         # add label for each design point
#         for i, cost in enumerate(costs):
#             if names[i] != "":
#                 label_name = "" + str(names[i])
#                 print(label_name)
#                 ax.text(costs[i], y_values[i], label_name, size=13)
#     if show_reference_designs:
#         #for ref design
#         costs = [design['Estimated Cost'] for design in reference_designs]
#         y_values = [design[y_axis_values[factor]] for design in reference_designs]
#         names = [design['Name'] for design in reference_designs]
#         #names = [design['Name'].partition("|")[0] for design in reference_designs]
#         plt.scatter(costs, y_values, c='orange',s=100, marker="X", label="reference designs")
#         # add label for each design point
#         for i, cost in enumerate(costs):
#             if names[i] != "":
#                 label_name = "" + str(names[i])
#                 print(label_name)
#                 ax.text(costs[i], y_values[i], label_name, size=13)

#     pareto = is_efficient_efficient(points)
#     pareto_points = pareto[0]
#     xs, ys = zip(*sorted(zip(pareto_points[:, 0], pareto_points[:, 1])))
#     plt.plot(xs, ys, 'r--', label='Pareto Frontier')
#     plt.scatter(pareto_points[:, 0], pareto_points[:, 1], facecolors='none', edgecolors='green',marker = 'X', s=100, label='Pareto Points')


#     # Add labels and title
#     plt.xlabel('Estimated Cost')
#     plt.ylabel(y_axis_values[factor])
#     title = 'Tradespace for architectural decision: ' + str(decisions[j])
#     if show_generated_designs == False:
#         title = 'Tradespace for architectural decisions'
#     plt.title(title)
#     plt.legend()
#     plt.grid(True)


#     file_name = "output_data/Tradespace" + str(j) + ".png"
#     plt.savefig(file_name)

# pareto_designs = []
# unique_pareto_designs = []
# unique_performence = []
# for i, is_pareto in enumerate(pareto[1]):
#     if is_pareto:
#         pareto_designs.append(designs[i])
#         print(designs[i]["Estimated Performance"])
#         if designs[i]["Estimated Performance"] not in  unique_performence:
#             unique_pareto_designs.append(designs[i])
#             unique_performence.append(designs[i]["Estimated Performance"])


# pareto_designs.sort(key=lambda x: x['Estimated Performance'], reverse=True)
# unique_pareto_designs.sort(key=lambda x: x['Estimated Performance'], reverse=True)

# print(len(pareto_designs))
# print("unique pareto designs: " + str(len(unique_pareto_designs)))

# with open("output_data/pareto_designs.json", "w") as json_file:
#     json.dump(pareto_designs, json_file, indent=4)

# with open("output_data/unique_pareto_designs.json", "w") as json_file:
#     json.dump(unique_pareto_designs, json_file, indent=4)

# combine_plots_vertical.get_concat_v(y_axis_values[factor])
plt.close('all')
# Show the plot
# plt.show()
