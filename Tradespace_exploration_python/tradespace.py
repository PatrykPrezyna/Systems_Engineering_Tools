import json
import numpy as np
import matplotlib.pyplot as plt

# Load designs.json
with open('designs.json', 'r') as file:
    designs = json.load(file)

# Extract cost and performance values
costs = [design['Total Cost'] for design in designs]
performances = [design['Total Performance'] for design in designs]
options = [design['Selected Options'] for design in designs]
name = [design['Name'] for design in designs]
print(name)
points = np.array(list(zip(costs, performances)))
# print(type(designs))

#color selected decision
decision_to_color = 1
unique_options = set()
for item in designs:
    unique_options.add(item['Selected Options'][decision_to_color])
unique_options = sorted(list(unique_options))
# print(unique_options)

reference_color = ['blue','yellow','red', "black", "yellow"]
color = []
for item in designs:
    for i, option in enumerate(unique_options):
        if item['Selected Options'][decision_to_color] == option:
            color.append(reference_color[i])
        


# Define the utopia point (ideal but unattainable point)
utopia_point = [min(costs), min(performances)]
# Plot tradespace and Pareto frontier with utopia point
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
plt.scatter(costs, performances, c=color, label='Tradespace (All Designs)')
#plt.plot(pareto_points[:, 0], pareto_points[:, 1], 'r--', label='Pareto Frontier')
#plt.scatter(pareto_points[:, 0], pareto_points[:, 1], c='red', label='Pareto Points')
# Add the utopia point to the plot
plt.scatter(*utopia_point, c='green', s=100, label='Utopia Point')

# Add labels and title
plt.xlabel('Total Cost')
plt.ylabel('Total Preparation time')
combined_array = list(zip(unique_options, reference_color))
title = 'Tradespace: ' + str(combined_array)
plt.title(title)
plt.legend()
plt.grid(True)

# add label for each design point
for i, txt in enumerate(options):
    if name[i] == "":
        label_name = ' '+str(i)
    else:
        label_name = ' '+str(i)+' '+name[i]

    ax.text(costs[i], performances[i], label_name)


# Show the plot
# plt.show()
plt.savefig("Tradespace.pdf")