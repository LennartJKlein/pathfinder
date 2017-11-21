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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Program settings
SIGN_PATH_START = 1
SIGN_GATE = 1

class Netlist:
    """
    Netlist are tuples reperesenting the contecion between two gates. Al conections
    must be made to solve the case.

    :param: number:     number of the netlist used
    """

    def __init__(self, number):
        # Make file name used.
        self.filename = "data/netlist"
        self.filename += str(number)
        self.filename += ".txt"

        # Open netlist and read with literal evaluation.
        with open(self.filename) as f:
            self.list = f.read()

        self.list = literal_eval(self.list)

        print("Using in Netlist #" + str(self.filename))

    def execute_connections(self, board):
        label = SIGN_PATH_START

        for connection in self.list:
            # Get the coordinates of the two gates in this connection
            a = connection[0]
            b = connection[1]
            print("------ OUTPUT -------")
            print("connection[0]", connection[0])
            print("connection[1]", connection[1])
            print("")

            coordGateA = np.argwhere(board.gatesNumbers == a + 1)
            coordGateB = np.argwhere(board.gatesNumbers == b + 1)

            # Create a new path object
            new_path = Path(coordGateA[0], coordGateB[0], label, "grey")

            # Add this path to the board object
            board.paths.append(new_path)

            # Calculate the route for this path
            new_path.calculate_DIJKSTRA(board)

            # Set a new label for the next path
            label += 1

    def print_list(self):
        # Print function for debugging
        print(self.list)

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
        self.paths = []
        self.gatesObjects = np.empty((self.z, self.y, self.x), dtype=object)
        self.gatesNumbers = np.zeros((self.z, self.y, self.x), dtype=int)

    def print_board(self):
        print(self.board)

    def get_coords(self, axes, label):
        labels = np.argwhere(self.board == label)
        coords = []

        for coord in labels:
            if axes == 'z':
                coords.append(coord[0])
            if axes == 'y':
                coords.append(coord[1])
            if axes == 'x':
                coords.append(coord[2])

        return coords

    def plot_paths(self, graph, ownColor):
        for path in self.paths:
            if ownColor:
                graph.plot(
                  path.get_coords('x'),
                  path.get_coords('y'),
                  path.get_coords('z'),
                  color=path.color
                )
            else:
                graph.plot(
                  path.get_coords('x'),
                  path.get_coords('y'),
                  path.get_coords('z')
                )

    def plot(self):
        # Config graph plot
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlim(0, self.x)
        ax.set_ylim(0, self.y)
        ax.set_zlim(self.z, 0)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        # Add paths to the graph
        self.plot_paths(plt, False)

        # Add gates to the graph
        ax.scatter(
          self.get_coords('x', SIGN_GATE),
          self.get_coords('y', SIGN_GATE),
          self.get_coords('z', SIGN_GATE)
        )

        # Show the graph
        plt.show()

class Gate:
    """
    :param x:     x-axis location
    :param y:     y-axis location
    :param y:     z-axis location
    :param name:  label of the gate
    """
    def __init__(self, netlist, label, x, y, z):
        self.label = label
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.spaces_free = 5
        self.spaces_needed = 0

        for connection in netlist.list:
            # connection + 1 plus 1 to match label.
            if ( connection[0] + 1 ) == label or ( connection[1] + 1 )== label:
                self.spaces_needed += 1


    def get_free_spaces(self, board, coord):
        counter = 0

        for i, axes in enumerate(coord):
            # Run twice for every axes
            for j in range(-1, 2, 2):   # j=-1  &  j=1
                coord = [self.z, self.y, self.x]
                coord[i] += j

                if board.board[coord[0], coord[1], coord[2]] == 0:
                    counter += 1

        space_free = counter - self.spaces_needed

        return space_free

    def __str__(self):
        return self.label

class Path:
    """
    Path from A to B
    :param: coordA:     first point on the board (list of Z, Y, X coordinates)
    :param: coordB:     second point on the board (list of  Z, Y, X coordinates)
    :param: aLabel:     the ID of this path
    :param: aColor:     the color for plotting
    """

    def __init__(self, coordA, coordB, aLabel, aColor):
        self.label = aLabel
        self.path = []
        self.a = coordA
        self.b = coordB
        self.color = aColor

    def add_coordinate(self, coord):
        # Adds a new coordinate (list) to self.path
        self.path.append(coord)

    def get_coords(self, axes):
        coords = []

        for coord in self.path:
            if axes == 'z':
                coords.append(coord[0])
            if axes == 'y':
                coords.append(coord[1])
            if axes == 'x':
                coords.append(coord[2])

        return coords

    def calculate_DIJKSTRA(self, board):
        '''
        Calculate route between two points
        :param board: a Numpy array
        '''

        # Initiate the dimantions of the board
        boardDimensions = board.board.shape
        boardDepth = boardDimensions[0]
        boardHeight = boardDimensions[1]
        boardWidth = boardDimensions[2]

        # Initiate counters
        loops = 0
        found = False

        # Initiate numpy data structures
        queue = [self.a]
        archive = np.zeros((boardDepth, boardHeight, boardWidth), dtype=int)
        self.add_coordinate(self.b)

        # Algorithm core logic
        while found == False and len(queue) > 0:

            # Track the steps
            loops += 1

            # Pick first coordinate from the queue
            coord = queue.pop(0);

            # Create all the adjacent cells of this coord and perhaps add them
            # to the queue. First, loop through all the axes of this coord.
            for i, axes in enumerate(coord):

                # Run twice for every axes
                for j in range(-1, 2, 2):   # j=-1  &  j=1
                    coordNew = list(coord)
                    coordNew[i] += j
                    coordNewZ = coordNew[0]
                    coordNewY = coordNew[1]
                    coordNewX = coordNew[2]

                    # --------------- CONSTRAINTS ----------------

                    # Check if the new coord has positive coordinates
                    if any(axes < 0 for axes in coordNew):
                        continue

                    # Check if the new coord falls within the board
                    if coordNewX >= boardWidth or \
                       coordNewY >= boardHeight or \
                       coordNewZ >= boardDepth:
                        continue

                    # Check if this coord is already in the archive
                    if archive[coordNewZ, coordNewY, coordNewX] != 0:
                        continue

                    # Check if there are no obstacles on the board
                    if board.board[coordNewZ, coordNewY, coordNewX] > 0:
                        if coordNewZ == self.b[0] and \
                           coordNewY == self.b[1] and \
                           coordNewX == self.b[2]:
                            found = True
                            print("Path " + str(self.label) + \
                            " has been found with " + str(loops) + " loops")
                        else:
                            continue

                    # Check surrounding tiles for gates that need space
                    for i, axes in enumerate(coordNew):

                        for j in range(-1, 2, 2):
                            coordNewer = list(coordNew)
                            coordNewer[i] += j
                            coordNewerZ = coordNewer[0]
                            coordNewerY = coordNewer[1]
                            coordNewerX = coordNewer[2]

                            # Check if the new coord has positive coordinates
                            if any(axes < 0 for axes in coordNewer):
                                continue

                            # Check if the new coord falls within the board
                            if coordNewerX >= boardWidth or \
                               coordNewerY >= boardHeight or \
                               coordNewerZ >= boardDepth:
                                continue

                            # Check if this gate needs space around it
                            if board.gatesObjects[coordNewerZ, coordNewerY, coordNewerX] != None:
                                # Don't look at the own gate.
                                if not (coordNewerZ == self.a[0] and \
                                    coordNewerY == self.a[1] and \
                                    coordNewerX == self.a[2]) \
                                    or \
                                   (coordNewerZ == self.b[0] and \
                                    coordNewerY == self.b[1] and \
                                    coordNewerX == self.b[2]):

                                    boardTemp = board.gatesObjects[coordNewerZ, coordNewerY, coordNewerX]

                                    if boardTemp.get_free_spaces(board, coordNewer) < 1:
                                        continue


                    # -------------- / CONSTRAINTS ---------------

                    # Add the coord to the queue
                    queue.append(coordNew)

                    # Save the iteration counter to this coordinate in the archive
                    archive[coordNewZ, coordNewY, coordNewX] = loops

                    # Check if B is found
                    if found:
                        break

        # Backtracking the shortest route
        if found:
            cursor = list(self.b)
            cursorChanged = False

            for i in range(loops - 1, 0, -1):

                # Loop through all the axes of this coord
                for j, axes in enumerate(cursor):

                    # Run twice voor every axes
                    for k in range(-1, 2, 2):   # j=-1  &  j=1

                        coordNew = list(cursor)
                        coordNew[j] += k
                        coordNewZ = coordNew[0]
                        coordNewY = coordNew[1]
                        coordNewX = coordNew[2]

                        # Check if the cell has positive coordinates
                        if any(axes < 0 for axes in coordNew):
                            continue

                        # Check if the cell falls within the board
                        if coordNewX >= boardWidth or \
                           coordNewY >= boardHeight or \
                           coordNewZ >= boardDepth:
                            continue

                        # Check if this cell is on the i'th position in the shortest path
                        if archive[coordNewZ, coordNewY, coordNewX] == i:

                            # Put the ID in the Numpy board
                            board.board[coordNewZ, coordNewY, coordNewX] = self.label

                            # Remember this coord
                            self.add_coordinate([coordNewZ, coordNewY, coordNewX])

                            # Move the cursor
                            cursor = coordNew
                            cursorChanged = True
                            break

                    if cursorChanged:
                        cursorChanged = False
                        break

            # Add the starting point to the end of the path-list
            self.add_coordinate(self.a)

            # Add 1 to the made connections for gate A and B
            # print("----------- Gates Conected  ------------")
            # print(board.gatesObjects[self.a[0], self.a[1], self.a[2]].label)
            # print(board.gatesObjects[self.b[0], self.b[1], self.b[2]].label)
            
            board.gatesObjects[self.a[0], self.a[1], self.a[2]].spaces_needed -= 1
            board.gatesObjects[self.b[0], self.b[1], self.b[2]].spaces_needed -= 1

        else:
            print("Path " + str(self.label) + " ERROR. Could not be calculated.")
