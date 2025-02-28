import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))

# Fixing random state for reproducibility
np.random.seed(19680801)


# generate some random test data
all_data = [np.random.uniform(10, 2, 10000)]
all_data.append(np.random.triangular(2, 6, 10, 10000))
all_data.append( np.random.normal(0, 3, 10000))
all_data.append(np.random.lognormal(9, 0.2, 10000)/1000)


#all_data.append(np.random.normal(-10, 2, 1000))
#all_data.append(np.random.lognormal(1, 1, 100))

print(type(all_data))
print(all_data)

# plot violin plot
axs[0].violinplot(all_data,
                  showmeans=True,
                  showmedians=True)
axs[0].set_title('Probability Density Function')

# plot box plot
axs[1].boxplot(all_data)
axs[1].set_title('Probability Density Function')

# adding horizontal grid lines
for ax in axs:
    ax.yaxis.grid(True)
    ax.set_xticks([y + 1 for y in range(len(all_data))],
                  labels=['Uniform', 'Triangular', 'Normal', 'Longnormal'])
    ax.set_xlabel('For every Option for each dcisson')
    ax.set_ylabel('Metric X')

file_name = "output_data/Uncerainty.png"
plt.savefig(file_name)
plt.close('all')
#plt.show()
