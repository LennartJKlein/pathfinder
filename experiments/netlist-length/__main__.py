import subprocess
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Set plot
fig = plt.figure()
ax = fig.gca(projection='2d')
ax.set_xlabel("Connections in netlist")
ax.set_ylabel("Average paths drawn (%)")

total_results = []
total_scores = []
netlist_lengths = []

# Netlist lengths (has to start at 2)
for i in range(2, 80):
    
	netlist_lengths.append(i)
	results = []
	scores = []

	# Amount of netlist files
    for j in range(100):

        command = "python pathfinder 50 0 " + str(i) +  " " + str(j)
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).strip()

        result = literal_eval(output.decode('ascii'))

	    results.append(result[0]) # paths drawn
	    scores.append(result[1]) # score

	# Save average for this length of netlists
	total_results.append(sum(results) / len(results))
	total_score.append(sum(scores) / len(scores))

# Plot the result
ax.plot(netlist_lengths, total_results)
plt.show()