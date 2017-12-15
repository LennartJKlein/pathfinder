import subprocess
from ast import literal_eval
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

netlist_lengths = np.array([], dtype=float)

for i in range (2, 51):
	netlist_lengths = np.append(netlist_lengths, float(i))

fig,ax = plt.subplots()


x = np.array([28.183673469387756, 40.816326530612244, 53.673469387755105, 70.93877551020408, 81.6938775510204, 93.12244897959184, 106.81632653061224, 125.44897959183673, 127.6734693877551, 142.08163265306123, 156.22448979591837, 161.3877551020408, 174.3877551020408, 188.26530612244898, 206.0, 206.10204081632654, 219.59183673469389, 239.14285714285714, 254.6326530612245, 268.6530612244898, 274.7755102040816, 283.3265306122449, 297.2040816326531, 307.7142857142857, 321.40816326530614, 352.6530612244898, 352.0204081632653, 364.42857142857144, 374.6326530612245, 402.9795918367347, 412.46938775510205, 419.3469387755102, 440.7142857142857, 472.51020408163265, 484.55102040816325, 501.3673469387755, 504.59183673469386, 519.3673469387755, 541.5102040816327, 571.9183673469388, 593.9795918367347, 605.8163265306123, 612.8367346938776, 642.7755102040817, 659.3265306122449, 676.530612244898, 697.469387755102, 713.5714285714286, 735.0204081632653])
y = netlist_lengths

fit = np.polyfit(x, y, deg=1)

# Plot the data
data_line = ax.scatter(x,y, marker='o')
ax.plot(x, fit[0] * x + fit[1], color='red')


# Make a legend
legend = ax.legend(loc='upper right')

plt.show()