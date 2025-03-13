import json
import numpy as np
import matplotlib.pyplot as plt
import math

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
EROR_BARS_PERCENTILE = [66.6]
ADD_LABEL = True # True / False 
#config
metrics = ["Ergonomics", "Interoperative Overhead", "Performance"]#TODO look for metrics in decision.json
reference_color = [
    "#FF8785", "#7BBFFC", "#4EC8DE", "#69C9B9", "#E7B030",
    "#BAC03F", "#E6A6C7", "#D5B480", "#BFD8E5"
]
reference_color_err = [
    "#A81829", "#00588D", "#005F73", "#005F52", "#714C00",
    "#4C5900", "#78405F", "#674E1F", "#3F5661"
]
marker = ['o', '^', 's']
label = ""
for metric in range(len(metrics)):
    y_axis_values_pareto = []
    x_axis_values_pareto = []
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    for i, design in enumerate(designs):
        costs = design['Cost']
        metric_values = design[metrics[metric]]
        mean_cost = np.mean(costs)
        mean_metric = np.mean(metric_values)
        if ADD_LABEL:
            label = str(design['Name']).split('|')[0]
            ax.text(mean_cost, mean_metric, label, size=13)

        plt.scatter(costs, metric_values, c=reference_color[i%len(reference_color)], marker=marker[math.floor(i/len(reference_color))%len(marker)], label=label, s=6)
        if design['Name'][0] == "R": #Add reference designs
            plt.scatter(mean_cost, mean_metric, facecolors='none', edgecolors='black',s=100, marker="X")

        costs = costs if hasattr(costs, "__len__") else [costs] # make it work also for a single value
        metric_values = metric_values if hasattr(metric_values, "__len__") else [metric_values]
        x_axis_values_pareto.extend(costs)
        y_axis_values_pareto.extend(metric_values)
        if len(costs) > 1: #plot error bars - take point hat are above the mean, substract the mean and get 33.3 percentile
            for error_bar_percentile in EROR_BARS_PERCENTILE:
                yerr_pos = np.percentile([x-mean_metric for x in metric_values if x > mean_metric], error_bar_percentile)
                yerr_neg = np.percentile([abs(x-mean_metric) for x in metric_values if x < mean_metric], error_bar_percentile)
                xerr_pos = np.percentile([x-mean_cost for x in costs if x > mean_cost], error_bar_percentile)
                xerr_neg = np.percentile([abs(x-mean_cost) for x in costs if x < mean_cost], error_bar_percentile)
                plt.errorbar(mean_cost, mean_metric,
                        xerr=[[xerr_neg], [xerr_pos]],
                        yerr=[[yerr_neg], [yerr_pos]],
                        c=reference_color_err[i%len(reference_color_err)],
                        capsize = 6, capthick = 2, lw = 1)

    points = np.array([x_axis_values_pareto, y_axis_values_pareto]).T
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
    plt.xlabel('Cost [$]')
    plt.ylabel(metrics[metric])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('Tradespace')
    plt.grid(True)

    file_name = "output_data/Tradespace_" + str(metrics[metric]) + ".png"
    print(file_name)
    plt.savefig(file_name)
    plt.close('all')
