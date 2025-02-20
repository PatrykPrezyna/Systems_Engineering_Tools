import json
import numpy as np
import matplotlib.pyplot as plt

# Load designs.json
with open('designs.json', 'r') as file:
# with open('designs_manual.json', 'r') as file:
    designs = json.load(file)

# Extract cost and performance values
costs = [design['Estimated Cost'] for design in designs]
performances = [design['Estimated Performance'] for design in designs]
options = [design['Selected Options'] for design in designs]
name = [design['Name'] for design in designs]
print(name)
points = np.array(list(zip(costs, performances)))

# Define the utopia point (ideal but unattainable point)
utopia_point = [min(costs), max(performances)]

reference_color = ['blue','yellow','red', "black", "yellow", "violet", "grey"]# for each option
decisions = ["Cutting Plane Control Method", "Robot Mount Type","Pre-op Imaging Type","Procedure Imaging Type","Onboard vs Offboard Power","Onboard vs Offboard Computing"]
if len(decisions) != len(designs[1]['Selected Options']):#test if the number of decisison is correct
    print("ERORR !!!!!!!!!!!!")
for j in range(len(designs[1]['Selected Options'])):
    #create scatter plot for each option
    decision_to_color = j
    unique_options = set()
    for item in designs:
        unique_options.add(item['Selected Options'][j])
    unique_options = sorted(list(unique_options))
    print("unique_options"+str(unique_options))
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)

    for i, option in enumerate(unique_options):
        print(option)
        costs = [design['Estimated Cost'] for design in designs]
        performances = [design['Estimated Performance'] for design in designs]
        Tradespace_title = str(decisions[j]) + ": " + str(option)
        plt.scatter(costs, performances, c=reference_color[i], label=Tradespace_title)


    # color = []
    # for item in designs:
    #     for i, option in enumerate(unique_options):
    #         if item['Selected Options'][decision_to_color] == option:
    #             color.append(reference_color[i])

    #plt.scatter(costs, performances, c=color, label='Tradespace')
    # #plt.plot(pareto_points[:, 0], pareto_points[:, 1], 'r--', label='Pareto Frontier')
    # #plt.scatter(pareto_points[:, 0], pareto_points[:, 1], c='red', label='Pareto Points')
    # # Add the utopia point to the plot
    plt.scatter(*utopia_point, c='green', s=100, label='Utopia Point')

    # Add labels and title
    plt.xlabel('Estimated Cost')
    plt.ylabel('Estimated Performence')
    combined_array = list(zip(unique_options, reference_color))
    title = 'Tradespace: ' + str(combined_array)
    plt.title(title)
    plt.legend()
    plt.grid(True)

    # # add label for each design point
    # for i, txt in enumerate(options):
    #     if name[i] == "":
    #         label_name = ' '#+str(i)#label for not design point without name
    #     else:
    #         #label_name = ' '+str(i)+'  '+name[i]
    #         label_name = name[i]

    #     ax.text(costs[i], performances[i], label_name)
    pdf_name = "Tradespace" + str(j) + ".png"
    plt.savefig(pdf_name)

# Show the plot
# plt.show()
