import subprocess
from ast import literal_eval
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# Set plot
fig, ax = plt.subplots()
ax.set_xlabel("Connections in netlist")
ax.set_ylabel("Average paths drawn (%)")

total_results = []
total_scores = []
netlist_lengths = []

# Netlist lengths (has to start at 2)
for i in range(2, 55):

    netlist_lengths.append(i)
    results = []
    scores = []

    # Amount of netlist files
    for j in range(1, 50):

        command = "python length55 56 0 " + str(i) +  " " + str(j)
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True).strip()

        result = literal_eval(output.decode('ascii'))

        results.append(result[0]) # paths drawn
        scores.append(result[1]) # score

        print("done with netlist file " + str(j) + " with length: " + str(i))

    # Save average for this length of netlists
    total_results.append(sum(results) / len(results))
    total_scores.append(sum(scores) / len(scores))
    print("length: " + str(i) + " " + str(total_results))
    print("score: " + str(total_scores))

# Plot the result
ax.plot(netlist_lengths, total_results)
plt.show()

#Plot scores
fig, ax = plt.subplots()
ax.set_xlabel("Connections in netlist")
ax.set_ylabel("Average score")
ax.plot(netlist_lengths, total_scores)
plt.show()