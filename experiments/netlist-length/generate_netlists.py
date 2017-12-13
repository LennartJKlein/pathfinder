"""Sample generators for netlists and gates"""
import random
from collections import Counter
import os
import sys

def make_random_netlist(length, min_gate, max_gate):
	"""Make a random array of netlists with respect to the contraints.

	:param length: Number of netlists to generate
	:type length: interger

	:rtype: list of tuples
    """
	netlist = []
	used_gates = []

	for j in range(length):
		netlist.append(tuple((random.sample(range(min_gate, max_gate + 1), 2))))

	for tuple_ in netlist:
		used_gates.append(tuple_[0])
		used_gates.append(tuple_[1])

	# Make two lists for the length of netlist and number occurrences
	counter_connections = dict(Counter(netlist))
	counter_numbers = dict(Counter(used_gates))

	# See if no duplicate connections are made.
	for gate in counter_connections.values():
		if gate > 1:
			return False

	# See if the length of connections is not greater than 5
	for gate in counter_numbers.values():
		if gate > 5:
			return False

	return netlist


# Settings
if len(sys.argv) < 4 or int(sys.argv[1]) <= 0 or int(sys.argv[2]) <= 0:
	print("ERROR - Correct usage: python generate_netlists.py amount-connections amount-files max-gate-number")
else:
	length_netlist = int(sys.argv[1])
	amount_files = int(sys.argv[2])
	min_gate = 0
	max_gate = int(sys.argv[3])


	# Create folder
	os.makedirs("netlists/length95/netlists-" + str(length_netlist), exist_ok=True)

	# Loop for amount of netlists
	counter_netlists = 0
	while counter_netlists < amount_files:

		# Create filename
		filename = "netlists/length95/netlists-" + str(length_netlist) + "/" + str(counter_netlists) + ".txt"

		# Write netlist
		with open(filename, "w") as file:

			random_netlist = make_random_netlist(length_netlist, min_gate, max_gate)
			while random_netlist == False:
				random_netlist = make_random_netlist(length_netlist, min_gate, max_gate)

			print(str(random_netlist), file=file, end='\n')

		# Count netlist
		counter_netlists += 1

	print("DONE. " + str(counter_netlists) + " netlists of length "+ str(length_netlist) +" generated.")



