def calculatePath(a, b):
	# Calculate route between two points (coordinates used as tuples)
	ax = a[0]
	ay = a[1]
	bx = b[0]
	by = b[1]
	cursor = {"x": ax, "y": ay}
	counter = 0

	# Walk 1 step through the grid till the endpoint is found
	while (cursor["x"] != bx) or (cursor["y"] != by):
	
		if cursor["x"] < bx:
			cursor["x"] += 1
			print("right")
		elif cursor["x"] > bx:
			cursor["x"] -= 1
			print("left")
		elif cursor["y"] < by:
			cursor["y"] += 1
			print("up")
		elif cursor["y"] > by:
			cursor["y"] -= 1
			print("down")

		counter += 1

	print("Steps made: " + str(counter))



board = [ ['_'] *5 for i in range(5) ]

for i, line in enumerate(board):
	for char in line:
		print char,

	print

calculatePath((4,3), (1,1))


