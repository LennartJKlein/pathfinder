"""
helpers.py

- Cell
- Board
- Netlist

"""
# TODO (thomas) import in doc zetten
from ast import literal_eval


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
        ''''
        :param x: How many columns the board uses
        :param y: How many rows the board uses
        :param show_labels: Display labels to the player
        '''

        self.x = x
        self.y = y
        self.show_labels = show_labels
        self.board = {}

        self.generate_board()

    def generate_board(self):
        for y in range(0, self.y):

            # Create an empty array in this row
            self.board[y] = []

            # Add a cell to this row for every column
            for x in range(0, self.x):
                # Make a cell at the current x, y and add it to the board
                cell = Cell(x, y)
                self.board[y].append(cell)

    def show_board(self):
        for key, cells in self.board.items():

            # Add the X Labels
            if self.show_labels:
                if key == 0:
                    x_label = []
                    x_label.insert(0, " ")
                    for cell in self.board[key]:
                        x_label.append(str(cell.x))
                    print(" ".join(x_label))

            row = []
            for cell in cells:
                row.append(str(cell))

            # Add the Y labels
            if self.show_labels:
                row.insert(0, str((cell.y)))

            print(" ".join(row))

    def set_gate(self, name, x, y):
        self.board[y][x].visual = name

class Gate:
    """
    :param x:     x-axis location
    :param y:     y-axis location
    :param y:     z-axis location
    :param name:  label of the gate
    """
    def __init__(self, label, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.label = label

    def __str__(self):
        return self.label

class Netlist:
    """
    Netlist is arg1 en moet gegeven worden.
    
    Netlist contains all the given Netlists from http://heuristieken.nl/resources/CC_netlists2.txt and makes them usable as an accessable, readable and searchable object.
    * netlist 0 - length 1
    * netlist 1 - length 30
    * netlist 2 - length 40
    * netlist 3 - length 50
    * netlist 4 - length 50
    * netlist 5 - length 60
    * netlist 6 - length 70

    Creating new instance of the netlist dataset in your code:
        variableName = Netlist()

    Accessing the dataset of one netlist in your code:
        include netlist number
    """

    def __init__(self, number):
        filename = "data/netlist"
        filename += str(number)
        filename += ".txt"

        with open(filename) as f:
            self.netlist = f.read()
        self.netlist = literal_eval(self.netlist)

        # laat zien dat het een array is gevuld met tuples
        # for tuples in self.netlist:
        #     print(type(tuples))


    def print_list(self):
        # Maakt het printen van de objecten mogelijk
        print(self.netlist)

def calculatePath(board, a, b):
    '''
    Calculate route between two points
    :param a: first point (tuple of coordinates)
    :param b: second point (tuple of coordinates)
    '''
    ax = a[0]
    ay = a[1]
    bx = b[0]
    by = b[1]
    cursor = {"x": ax, "y": ay}
    counter = 0

    # Walk 1 step through the grid till the endpoint is reached
    while (cursor["x"] != bx) or (cursor["y"] != by):

        if cursor["x"] < bx:
            cursor["x"] += 1
            print("right", end=' ')
        elif cursor["x"] > bx:
            cursor["x"] -= 1
            print("left", end=' ')
        elif cursor["y"] < by:
            cursor["y"] += 1
            print("down", end=' ')
        elif cursor["y"] > by:
            cursor["y"] -= 1
            print("up", end=' ')

        # Mark the steps
        board.set_gate("#", cursor["x"], cursor["y"])

        counter += 1

    print("- Steps made: " + str(counter))