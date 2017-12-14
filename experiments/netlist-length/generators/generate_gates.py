"""Sample generators for netlists and gates"""
import random
from collections import Counter
import os
import numpy as np
import sys

def make_random_gates(amount_gates, width, height, depth):
	"""Make a random array of netlists with respect to the contraints.

	:param length: Number of netlists to generate
	:type length: interger

	:rtype: list of tuples
    """
	
	gatesName = []
	gatesX = []
	gatesY = []
	gatesZ = []
	gates = np.zeros((depth, height, width), dtype=int)

	for i in range(amount_gates):
		
		random_coord = get_random_coord(width, height, depth)
		while gates[random_coord[0], random_coord[1], random_coord[2]] != 0:
			random_coord = get_random_coord(width, height, depth)

		gates[random_coord[0], random_coord[1], random_coord[2]] = i + 1
		gatesName.append(i)
		gatesZ.append(random_coord[0])
		gatesY.append(random_coord[1])
		gatesX.append(random_coord[2])

	return gatesName, gatesX, gatesY, gatesZ

def get_random_coord(width, height, depth):
	x = random.sample(range(1, width - 1), 1)
	y = random.sample(range(1, height - 1), 1)
	z = random.sample(range(1, depth), 1)

	return (z, y, x)

# Settings
if len(sys.argv) < 3 or int(sys.argv[1]) <= 0 or int(sys.argv[2]) <= 0:
	print("ERROR - Correct usage: python generate_gates.py amount-gates amount-files")
else:
	amount_gates = int(sys.argv[1])
	amount_files = int(sys.argv[2])
	width = 18
	height = 17
	depth = 8

	# Create folder
	os.makedirs("gates/gates-" + str(amount_gates), exist_ok=True)

	# Loop for amount of netlists
	counter_files = 0
	while counter_files < amount_files:

		# Create filename
		filename = "gates/gates-" + str(amount_gates) + "/" + str(counter_files) + ".csv"

		# Write netlist
		with open(filename, "w") as file:
			print("name,x,y,z", file=file, end='\n')

			names, xs, ys, zs = make_random_gates(amount_gates + 1, width, height, depth)
			
			for i in range(1, amount_gates + 1):
				print(str(names[i]) + "," + str(xs[i])[1:-1] + "," + str(ys[i])[1:-1] + "," + str(zs[i])[1:-1], file=file, end='\n')

		# Count file
		counter_files += 1

	print("DONE. " + str(counter_files) + " files of "+ str(amount_gates) +" random gates generated.")