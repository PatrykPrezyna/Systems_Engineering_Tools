import json
import numpy as np
import matplotlib.pyplot as plt

# Load designs.json
with open('designs.json', 'r') as file:
    designs = json.load(file)

# Extract cost and performance values
costs = [design['Total Cost'] for design in designs]
performances = [design['Total Performance'] for design in designs]
points = np.array(list(zip(costs, performances)))

# Function to calculate Pareto frontier
def pareto_frontier(points, maxX=False, maxY=True):
    sorted_points = points[np.argsort(points[:, 0])]  # Sort by cost (x-axis)
    pareto_front = np.ones(len(points), dtype=bool)  # Initialize all as Pareto-efficient
    
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if maxX:
                condX = sorted_points[i, 0] <= sorted_points[j, 0]
            else:
                condX = sorted_points[i, 0] >= sorted_points[j, 0]
            
            if maxY:
                condY = sorted_points[i, 1] <= sorted_points[j, 1]
            else:
                condY = sorted_points[i, 1] >= sorted_points[j, 1]
            
            if condX and condY:
                pareto_front[i] = False
                break
    
    return sorted_points[pareto_front]

# Calculate Pareto frontier
pareto_points = pareto_frontier(points)

# Define the utopia point (ideal but unattainable point)
utopia_point = [min(costs), max(performances)]

# Calculate distances from each Pareto point to the utopia point
distances_to_utopia = [
    np.sqrt((point[0] - utopia_point[0])**2 + (point[1] - utopia_point[1])**2)
    for point in pareto_points
]

# Find the Pareto point closest to the utopia point
closest_pareto_point = pareto_points[np.argmin(distances_to_utopia)]

# Plot tradespace and Pareto frontier with utopia point
plt.figure(figsize=(10, 6))
plt.scatter(costs, performances, c='blue', label='Tradespace (All Designs)')
plt.plot(pareto_points[:, 0], pareto_points[:, 1], 'r--', label='Pareto Frontier')
plt.scatter(pareto_points[:, 0], pareto_points[:, 1], c='red', label='Pareto Points')

# Add the utopia point to the plot
plt.scatter(*utopia_point, c='green', s=100, label='Utopia Point')

# Highlight the closest Pareto point to the utopia point
plt.scatter(*closest_pareto_point, c='orange', s=100, label='Closest Pareto Point')

# Add labels and title
plt.xlabel('Total Cost')
plt.ylabel('Total Performance')
plt.title('Tradespace with Pareto Frontier and Utopia Point')
plt.legend()
plt.grid(True)

# Show the plot
# plt.show()
plt.savefig("Tradespace.pdf")


# Print details of the closest Pareto point
print("Utopia Point:", utopia_point)
print("Closest Pareto Point:", closest_pareto_point)
print("Distance to Utopia Point:", min(distances_to_utopia))
