"""
helpers.py
- Cell
- Board
- Gate
- Netlist
- Calculate path
"""

from ast import literal_eval
import numpy as np

SIGN_GATE = 1

class Board:

    def __init__(self, x, y, z):
        """
        :param x: How many columns the board uses
        :param y: How many rows the board uses
        :param z: How many layers the board uses
        """
        self.x = x
        self.y = y
        self.z = z
        self.board = np.zeros((self.z, self.y, self.x), dtype=int)

    def print_board(self):
        print(self.board)

    def set_gate(self, x, y, z):
        self.board[z,y,x] = SIGN_GATE

    def set_path(self, name, x, y, z):
        self.board[z,y,x] = name

    def get_coords(self, axes, label):
        labels = np.argwhere(self.board == label)
        coords = []

        for cord in labels:
            if axes == 'z':
                coords.append(cord[0])
            if axes == 'y':
                coords.append(cord[1])
            if axes == 'x':
                coords.append(cord[2])

        return coords

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
    Netlist are tuples reperesenting the contecion between two gates. Al conections
    must be made to solve the case.

    :param: number:     number of the netlist used
    """

    def __init__(self, number):
        # Make file name used.
        filename = "data/netlist"
        filename += str(number)
        filename += ".txt"

        # Open netlist and read with literal evaluation.
        with open(filename) as f:
            self.list = f.read()
        self.list = literal_eval(self.list)

    # Print function for debugging.
    def print_list(self):
        print(self.list)

class PathMaker:
    """Path maker creates lines to be used in MathPlotLib."""
    def __init__(self, label):
        self.path_walked = ([],[],[])
        self.label = label

    def append_new_coordinate(self, new):
        # Adds a new coordinate to self.path_walked
        new_list = []
        for items in new:
            new_list = new_list + items

        for items in self.path_walked:
            items.append(new_list.pop(0))

        # return base
        return self.path_walked

    # return the variable containing the info on the path.
    def return_path(self):
        return self.path_walked

    # Retrun the name of the path
    def return_label(self):
        return self.label

def calculatePath(board, a, b, label):
    '''
    Calculate route between two points
    :param a: first point (tuple of coordinates)
    :param b: second point (tuple of coordinates)
    '''

    ax = a[0]
    ay = a[1]
    az = a[2]
    bx = b[0]
    by = b[1]
    bz = b[2]
    cursor = {"x": ax, "y": ay, "z": az}
    step_counter = 0
    found = False

    # Create a new instance of PathMaker with label as the name.
    newPath = PathMaker(label)

    # Walk 1 step through the grid till the endpoint is reached
    while (cursor["x"] != bx) or (cursor["y"] != by) or (cursor["z"] != bz):

        if cursor["x"] < bx:
            cursor["x"] += 1
        elif cursor["x"] > bx:
            cursor["x"] -= 1
        elif cursor["y"] < by:
            cursor["y"] += 1
        elif cursor["y"] > by:
            cursor["y"] -= 1

        # Append the path to the path tracker.
        newPath.append_new_coordinate(([cursor["x"]],[cursor["y"]],[cursor["z"]]))

        # Check if endpoint is reached
        if (cursor["x"] == bx) and (cursor["y"] == by) and (cursor["z"] == bz):
            found = True

        # Mark the steps while the endpoint is not reached
        if found ==  False:
            board.set_path(label, cursor["x"], cursor["y"], cursor["z"])

        step_counter += 1

    print("- Steps made: " + str(step_counter))
    # Returns the data on the path to create lines or log.
    return newPath
