import matplotlib.pyplot as plt
import pandas as pd

# build data
data = [
    ["1) Mount type", 10, 9],
    ["2) Real‐Time Position Sensor Type", 11, 8],
    ["3) Cutting Plane Control Method", 10, 8],
    ["4) Open vs. Closed Implant", 14, 7],
    ["5) Onboard vs Offboard Computing", 6, 7],
    ["6) Onboard vs Offboard Power", 6, 7],
    ["7) User Interface", 10, 7],
    ["8) Sterilized/Disposable Components", 5, 8],
    ["9) Imaging Type", 5, 8],
    ["10) Compatible Tools", 2, 8],
]
# create pandas DataFrame
df = pd.DataFrame(data, columns=["Decision", "Sensitivity", "Conectivity"])


# open figure + axis
fig, ax = plt.subplots()
# plot
ax.scatter(x=df["Conectivity"], y=df["Sensitivity"], c="DarkBlue")
# set labels
plt.title("Architectural decisions")
ax.set_xlabel("Degree of Conectivity")
ax.set_ylabel("Degree of Sensitivity")

# annotate points in axis
for idx, row in df.iterrows():
    print(idx)
    if idx == 2 or idx == 4 or idx == 8:
        ax.annotate(row["Decision"], (row["Conectivity"] + 0.02, row["Sensitivity"] - 0.3))
    else:
        ax.annotate(row["Decision"], (row["Conectivity"] + 0.02, row["Sensitivity"] + 0.1))
# force matplotlib to draw the graph

# adding vertical line in data co-ordinates
plt.axvline(8, c="black", ls="--")

# adding horizontal line in data co-ordinates
plt.axhline(8, c="black", ls="--")


plt.savefig("foo.pdf")
plt.show()
