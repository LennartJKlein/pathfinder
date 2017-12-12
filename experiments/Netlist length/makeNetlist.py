"""Sample generators for netlists and gates"""
import random
from collections import Counter

def make_random_netlist(amount, min_gate=0, max_gate=51):
	"""Make a random array of netlists with respect to the contraints.

	:param amount: Number of netlists to generate
	:type amount: interger

	:rtype: list of tuples
    """
	netlist = []
	templist = []

	for j in range(amount):
		netlist.append(tuple((random.sample(range(min_gate, max_gate), 2))))

	for tuples_ in netlist:
		templist.append(tuples_[0])
		templist.append(tuples_[1])

	# Make to lists for the amount of netist and number occurrences
	counter_list_netlists = dict(Counter(netlist))
	counter_list_numbers = dict(Counter(templist))

	# See if no duplicate netlist are used.
	for key in counter_list_netlists.values():
		if key > 1:
			make_random_netlist(amount)

	# See if the amount of connections is not greater than 5
	for key in counter_list_numbers.values():
		if key > 5:
			make_random_netlist(amount)

	return netlist

# Eventueel de forloop buiten de with plaatsen om zo genummerd Output1.txt,
# Output2.txt etc te maken maar nu maakt die nieuwe lijnen met op iedere lijn
 # een nieuwe random netlist
with open("Output.txt", "w") as text_file:
    for i in range(3):
        print(str(make_random_netlist(10)), file=text_file, end='\n')
