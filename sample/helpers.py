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
        self.board = []
        self.generate_board()

    def generate_board(self):
        self.board = np.zeros((self.z, self.y, self.x), dtype=int)

    def show_board(self):
        print(self.board)

    def set_gate(self, name, x, y, z):
        self.board[z,y,x] = 2

    def set_path(self, name, x, y, z):
        self.board[z,y,x] = 1

    def get_coords(self, axes, label):
        var = np.argwhere(self.board == label)
        coords = []

        for cord in var:
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
    counter = 0
    found = False

    # Walk 1 step through the grid till the endpoint is reached
    while (cursor["x"] != bx) or (cursor["y"] != by) or (cursor["z"] != bz):

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

        # Check if endpoint is reached
        if (cursor["x"] == bx) and (cursor["y"] == by) and (cursor["z"] == bz):
            found = True

        # Mark the steps while the endpoint is not reached
        if found ==  False:
            board.set_path(label, cursor["x"], cursor["y"], cursor["z"])

        counter += 1

    print("- Steps made: " + str(counter))
