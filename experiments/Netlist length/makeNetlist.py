import random
from collections import Counter


def make_random_netlist(amount):
	"""
	
	"""

	counter = 0
	min_gate = 0
	max_gate = 51
	netlist = []
	templist = []
	# testnetlist = [(10, 22), (42, 47), (18, 14), (50, 1), (25, 26), (50, 15), (26, 48), (36, 6), (21, 2), (4, 11), (28, 3), (15, 46), (26, 23), (30, 16), (15, 24), (0, 37), (8, 18), (1, 47), (21, 34), (50, 41), (4, 11), (11, 49), (22, 41), (49, 42), (9, 8), (27, 28), (38, 15), (30, 9), (8, 29), (24, 27), (45, 6), (16, 5), (47, 10), (48, 49), (21, 4), (28, 4), (16, 3), (5, 35), (48, 1), (29, 23), (28, 12), (43, 21), (31, 32), (34, 17), (33, 7), (23, 10), (14, 43), (46, 13), (47, 45), (39, 6)]

	for j in range(amount):
		netlist.append(tuple((random.sample(range(min_gate, max_gate), 2))))
		set(netlist)
		list(netlist)

	for tuples_ in netlist:
		templist.append(tuples_[0])
		templist.append(tuples_[1])

	counterlist = dict(Counter(netlist))


	for key in counterlist.values():
		if key > 4:
			make_random_netlist(amount)

	return netlist


# lijst = []
# for i in range(1200):
# 	lijst.append(make_random_netlist(100))


# # for items in lijst:
# # 	print (items)

# print(lijst)





# Make the board with the random netlist here
