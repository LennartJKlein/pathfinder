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

# Program settings
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

def calculatePath(board, aTuple, bTuple, label):
    '''
    Calculate route between two points
    :param board: a Numpy array
    :param aTuple: first point on the board (tuple of coordinates)
    :param bTuple: second point on the board (tuple of coordinates)
    :param label: the label this path gets on the board
    '''

    print("Walking from gate: " + str(aTuple) + " to " + str(bTuple))

    # Create comparable lists from the point tuples
    a = list(aTuple)
    b = list(bTuple)

    # Initiate queue and constraints
    queue = [a]
    archive = []
    loops = 0
    found = False

    # Algorithm
    while found == False:

        # Track the progress
        print(str(queue))
        loops += 1

        # Pick first coordinate from the queue
        coord = queue.pop(0);

        # Check if this coord is the destination
        if coord == b:
            found = True
        else:
            # Create all the adjacent cells of this coord and add them to the queue
             for i, axes in enumerate(coord):

                # Step forth on this axes
                newCoordPlus = list(coord)
                newCoordPlus[i] += 1
                if not newCoordPlus in queue and newCoordPlus[0] > 0 and newCoordPlus[1] > 0:
                    queue.append(newCoordPlus)
                    coordList = [newCoordPlus, loops]
                    archive.append(coordList)

                # Step back on this axes
                newCoordMin = list(coord)
                newCoordMin[i] -= 1
                if not newCoordMin in queue and newCoordMin[0] > 0 and newCoordMin[1] > 0:
                    queue.append(newCoordMin)
                    coordList = [newCoordMin, loops]
                    archive.append(coordList)

    print("Point B has been found!")
    print("Loops needed: " + str(loops))
    print("")
    print("archive is: " + str(archive))
    print("")