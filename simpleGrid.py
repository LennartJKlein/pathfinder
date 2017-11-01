import csv
import netlist as Netlist

class Cell:
    """
    :param x: x-axis location
    :param y: y-axis location
    """
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.visual = "."

    def __str__(self):
        return self.visual

class Board:

    def __init__(self, x, y, show_labels=True):
        """
        :param x: How many columns the board uses
        :param y: How many rows the board uses
        :param show_labels: Display labels to the player
        """

        self.x = x
        self.y = y
        self.show_labels = show_labels
        self.board = {}

        self.generate_board()

    def generate_board(self):
        for y in range(0, self.y):

            # Add the key X to the board dictionary
            self.board[y] = []   

            for x in range(0, self.x):
                # Make a cell @ the current x, y and add it to the board
                cell = Cell(x, y)
                self.board[y].append(cell)

    def show_board(self):

        for key, cells in self.board.iteritems():

            # Add the X Labels
            if self.show_labels:
                if key == 0:
                    x_label = []
                    for cell in self.board[key]:
                        x_label.append(str(cell.x + 1))
                    print " ".join(x_label)

            row = []
            for cell in cells:
                row.append(str(cell))

            # Add the Y labels
            if self.show_labels:
                row.append(str(cell.y + 1))

            print " ".join(row)

    def set_gate(self, x, y):
        self.board[x][y].visual = "0"

def main():
	# Determine X and Y of the board
	b = Board(10, 10, True)

	# Open the CSV file 'gates.csv'
	with open('gates.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
		    gate = row

		    # retrieve X cord in csv-file
		    gateX = ','.join(gate[1])

		    # retrieve Y cord in csv-file
		    gateY = ''.join(gate[2]).strip(")")
		    
		    # Turn the cord into intergers
		    gateX = int(gateX)
		    gateY = int(gateY)

		    # Set a gate in the grid for every row in the csv-file
		    b.set_gate(gateX, gateY)

	# initialise board
	b.show_board()

'''
TO MERGE:
'''

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

if __name__ == '__main__':
	main()
