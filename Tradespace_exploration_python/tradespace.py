import json
import numpy as np
import matplotlib.pyplot as plt

# Load designs.json
with open('designs.json', 'r') as file:
    designs = json.load(file)

# Extract cost and performance values
costs = [design['Total Cost'] for design in designs]
performances = [design['Total Performance'] for design in designs]
label = [design['Selected Options'] for design in designs]
points = np.array(list(zip(costs, performances)))

# Define the utopia point (ideal but unattainable point)
utopia_point = [min(costs), min(performances)]

# Plot tradespace and Pareto frontier with utopia point
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111)
color = []
# for i, design in enumerate(label):
#  if label
#  color.append('blue')
plt.scatter(costs, performances, c='blue', label='Tradespace (All Designs)')
#plt.plot(pareto_points[:, 0], pareto_points[:, 1], 'r--', label='Pareto Frontier')
#plt.scatter(pareto_points[:, 0], pareto_points[:, 1], c='red', label='Pareto Points')

# Add the utopia point to the plot
plt.scatter(*utopia_point, c='green', s=100, label='Utopia Point')

# Add labels and title
plt.xlabel('Total Cost')
plt.ylabel('Total Performance')
plt.title('Tradespace with Pareto Frontier and Utopia Point')
plt.legend()
plt.grid(True)

for i, txt in enumerate(label):
    print(txt)
    ax.text(costs[i], performances[i]+i%5, str(i)+txt[1])#TO DO combine all designs with the same position in one string


# Show the plot
# plt.show()
plt.savefig("Tradespace.pdf")