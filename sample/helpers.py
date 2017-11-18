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

    # Initiate data structures
    queue = [a]
    archive = []

    # Initiate constraints
    boardDimensions = board.board.shape
    boardDepth = boardDimensions[0]
    boardHeight = boardDimensions[1]
    boardWidth = boardDimensions[2]
    loops = 0
    found = False

    # Algorithm
    while found == False and len(queue) > 0:

        # Track the progress
        # print(str(queue))
        loops += 1

        # Pick first coordinate from the queue
        coord = queue.pop(0);

        # Check if this coord is the destination
        if coord == b:
            found = True
        else:
            # Create all the adjacent cells of this coord and perhaps add them to the queue

            # Loop through all the axes of this coord
            for i, axes in enumerate(coord):

                # Run twice voor every axes
                for j in range(-1, 2, 2):   # j=-1  &  j=1
                    coordNew = list(coord)
                    coordNew[i] += j
                    coordNewX = coordNew[0]
                    coordNewY = coordNew[1]
                    coordNewZ = coordNew[2]
                    
                    if coordNew in archive:
                        continue
                    
                    # Check if the new coord has positive coordinates
                    if any(axes < 0 for axes in coordNew):
                        continue

                    # Check if the new coord falls within the board
                    if coordNewX >= boardWidth or coordNewY >= boardHeight or coordNewZ >= boardDepth:
                        continue

                    # Check if the new coord is empty
                    if board.board[coordNewZ, coordNewY, coordNewX] != 0:
                        if coordNew != b:
                            continue

                    # Add the coord to the queue
                    queue.append(coordNew)

                    # TESTING: print this coord as a 3 on the board
                    #if coordNew != b:
                    #    board.set_path(3, coordNewX, coordNewY, coordNewZ)

                    # Add loop counter to the coord and save it in the archive
                    coordList = [coordNew, loops]
                    archive.append(coordList)

    print("Point B has been found!")
    print("Loops needed: " + str(loops))
    print("")
    print("archive is: " + str(archive))
    print("")