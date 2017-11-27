"""
helpers.py
- Cell
- Board
- Gate
- Netlist
- Calculate path
"""

import settings

import numpy as np
import matplotlib.pyplot as plt
from ast import literal_eval
from mpl_toolkits.mplot3d import Axes3D
import collections
import heapq

import colors as CLR

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

        print("Using netlist #" + str(number))

    def execute_connections(self, board):
        path_number = settings.SIGN_PATH_START
        amount_fail = 0

        for connection in self.list:
            # Get the coordinates of the two gates in this connection
            a = connection[0]
            b = connection[1]

            #print("")
            #print(str(connection[0]) + "  ->  "  + str(connection[1]))
            
            coordGateA = np.argwhere(board.gatesNumbers == a + 1)
            coordGateB = np.argwhere(board.gatesNumbers == b + 1)

            # Create a new path object
            new_path = Path(coordGateA[0], coordGateB[0], path_number, "grey")

            # Add this path to the board object
            board.paths.append(new_path)

            # Calculate the route for this path
            result = new_path.calculate(settings.PATH_ALGORITHM, board)

            # Count the score
            if result == False:
                amount_fail += 1

            # Set a new path_number for the next path
            path_number += 1

        print(CLR.YELLOW + "Paths not calculated: " + str(amount_fail) + " / " + str(path_number) + CLR.DEFAULT)
        print(CLR.YELLOW + str(round(amount_fail / path_number * 100, 2)) + "%" + CLR.DEFAULT)
        print("")

    def print_list(self):
        # Print function for debugging
        print(self.list)

class Board:

    def __init__(self, width, height, depth):
        """
        :param width: How many columns the board uses
        :param height: How many rows the board uses
        :param depth: How many layers the board uses
        """
        self.x = width
        self.y = height
        self.z = depth
        self.board = np.zeros((self.depth, self.height, self.width), dtype=int)
        self.paths = []
        self.gatesObjects = np.empty((self.depth, self.height, self.width), dtype=object)
        self.gatesNumbers = np.zeros((self.depth, self.height, self.width), dtype=int)

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

    def get_neighbors(self, coord):
        (x, y, z) = coord
        is_valid = []
        neighbors = [[x, y, z+1], [x, y, z-1], [x, y+1, z], [x, y-1, z], [x+1, y, z], [x-1, y, z]]
        for neighbor in neighbors:
            if (self.valid_coord(neighbor)):
                is_valid.append(neighbor)
        return is_valid


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
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_zlim(self.depth, 0)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        # Add paths to the graph
        self.plot_paths(plt, False)

        # Add gates to the graph
        ax.scatter(
          self.get_coords('x', settings.SIGN_GATE),
          self.get_coords('y', settings.SIGN_GATE),
          self.get_coords('z', settings.SIGN_GATE)
        )

        # Show the graph
        plt.show()

    def valid_coord(self, coord):

        # Check if the cords are positive
        if any(axes < 0 for axes in coord):
            return False

        # Check if the new coord falls within the board
        if coord >= self.width or \
           coord >= self.height or \
           coord >= self.depth:
            return False
        return True

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
            # connection + 1 to match label
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

class Queue:
    """
    dequeue, append and count elements in Queue
    :param: none
    """

    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def push(self, x):
        self.elements.append(x)
    
    def pop(self):
        return self.elements.popleft()


def QueuePriority:

    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def push(self, coord, prior):
        heapq.heappush(self.elements, (prior, coord))

    def pop(self):
        return heapq.heappop(self.elements)[1]


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

    def calculate(self, algorithm, board):
        '''
        Calculate route between two points with the A* algorithm
        :param board:       a Numpy array
        :param algorithm:   algorithm to draw the path
        '''

        if algorithm == "DIJKSTRA":
            return self.calculate_DIJKSTRA(board)

        if algorithm == "ASTAR":
            return self.calculate_ASTAR(board)

    def calculate_ASTAR(self, board):

        # # Initiate the dimantions of the board
        # boardDimensions = board.board.shape
        # boardDepth = boardDimensions[0]
        # boardHeight = boardDimensions[1]
        # boardWidth = boardDimensions[2]

        # queue = QueuePriority()
        # queue.push(self.a, 0)
        # came_from = {}
        # cost_so_far = {}
        # came_from[self.a] = None
        # cost_so_far[self.a] = 0

        # while not queue.empty():
        #     current = queue.pop()

        #     if (current == self.b):
        #         break

        #     for 

        #print("Path #" + str(self.label) +  ": " + str(calculate_distance(self.a, self.b)))

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
        archive = np.zeros((boardDepth, boardHeight, boardWidth), dtype=int)

        # Add destination to the path route
        self.add_coordinate(self.b)

        frontier = Queue()
        frontier.push(self.a)

        # Algorithm core logic
        while not frontier.empty() and found == False:

            # Track the distance
            loops += 1

            # Pick first coordinate from the queue
            current = frontier.pop()

            # Create all the adjacent cells of this coord and perhaps add them
            # to the queue. First, loop through all the axes of this coord.
            for i, axes in enumerate(current):

                # Run twice for every axes
                for j in range(-1, 2, 2):   # j=-1  &  j=1
                    coordNew = list(current)
                    coordNew[i] += j
                    coordNewZ = coordNew[0]
                    coordNewY = coordNew[1]
                    coordNewX = coordNew[2]

                    # --------------- HEURISTICS ----------------

                    # Check if this is the destination
                    if (coordNewZ == self.b[0] and \
                        coordNewY == self.b[1] and \
                        coordNewX == self.b[2]):
                        found = True
                        break

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

                    # Check if there are no obstacles on this coord
                    if board.board[coordNewZ, coordNewY, coordNewX] > 0:
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

                                    # Get info from this gate
                                    boardTemp = board.gatesObjects[coordNewerZ, coordNewerY, coordNewerX]

                                    # See if the path may pass
                                    if boardTemp.get_free_spaces(board, coordNewer) < 1:
                                        continue

                    # -------------- / HEURISTICS ---------------

                    # Add the coord to the queue
                    frontier.put(coordNew)

                    # Save the iteration counter to this coordinate in the archive
                    archive[coordNewZ, coordNewY, coordNewX] = loops

        # Backtracking the shortest route
        if found:
            cursor = list(self.b)
            cursorChanged = False

            for i in range(loops - 1, 0, -1):

                # Loop through all the axes of this coord
                # Run twice voor every axes
                for j, axes in enumerate(cursor):
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

                            # Remember this coord for this path
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
            board.gatesObjects[self.a[0], self.a[1], self.a[2]].spaces_needed -= 1
            board.gatesObjects[self.b[0], self.b[1], self.b[2]].spaces_needed -= 1

            return True

        else:
            #print("Path " + str(self.label) + " ERROR. Could not be calculated.")
            return False

def calculate_distance(a, b):
    dx = (a[2] - b[2]) ** 2
    dy = (a[1] - b[1]) ** 2
    dz = (a[0] - b[0]) ** 2
    return (dx + dy + dz) ** 0.5