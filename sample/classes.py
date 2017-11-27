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
from mpl_toolkits.mplot3d import Axes3D
from ast import literal_eval
import collections
import heapq

import colors as CLR

class Board:

    def __init__(self, width, height, depth):
        """
        :param width: How many columns the board uses
        :param height: How many rows the board uses
        :param depth: How many layers the board uses
        """
        self.width = width
        self.height = height
        self.depth = depth
        self.board = np.zeros((self.depth, self.height, self.width), dtype=int)
        self.paths = []
        self.gatesObjects = np.empty((self.depth, self.height, self.width), dtype=object)
        self.gatesNumbers = np.zeros((self.depth, self.height, self.width), dtype=int)

    def calculate_distance(self, a, b):
        dx = (a[2] - b[2]) ** 2
        dy = (a[1] - b[1]) ** 2
        dz = (a[0] - b[0]) ** 2
        return (dx + dy + dz) ** 0.5

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
        (z, y, x) = coord
        is_valid = []
        neighbors = [[z, y, x+1], [z, y, x-1], [z, y+1, x], [z, y-1, x], [z+1, y, x], [z-1, y, x]]
        for neighbor in neighbors:
            if self.valid_coord(neighbor):
                is_valid.append(neighbor)
        return is_valid

    def plot_paths(self, graph, ownColor):
        for path in self.paths:
            if ownColor:
                graph.plot(
                  path.get_coords('x'),
                  path.get_coords('y'),
                  path.get_coords('z'),
                  zorder=-1,
                  color=path.color
                )
            else:
                graph.plot(
                  path.get_coords('x'),
                  path.get_coords('y'),
                  path.get_coords('z'),
                  zorder=-1
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
          self.get_coords('z', settings.SIGN_GATE),
          color="black"
        )

        # Show the graph
        plt.show()

    def print_board(self):
        print(self.board)

    def valid_coord(self, coord):
        # Check if the coord is positive
        if any(axes < 0 for axes in coord):
            return False

        # Check if the coord falls within the board
        if coord[2] >= self.width or \
           coord[1] >= self.height or \
           coord[0] >= self.depth:
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
        self.spaces_needed = 0

        for connection in netlist.list:
            # Connection + 1 to match label of gate
            if (connection[0] + 1) == label or (connection[1] + 1) == label:
                self.spaces_needed += 1

    def get_free_spaces(self, board, coord):
        counter = 0

        for neighbor in board.get_neighbors(coord):
            # Count if neighbor is free on the board
            if board.board[neighbor[0], neighbor[1], neighbor[2]] == 0:
                counter += 1

        return counter - self.spaces_needed

    def __str__(self):
        return self.label

class Netlist:
    """
    Netlist are tuples reperesenting the contecion between two gates. Al conections
    must be made to solve the case.

    :param: number:     id of the netlist
    """

    def __init__(self, number):
        self.filename = "data/netlist"
        self.filename += str(number)
        self.filename += ".txt"

        # Open netlist and read with literal evaluation
        with open(self.filename) as f:
            self.list = f.read()

        self.list = literal_eval(self.list)

    def execute_connections(self, board):
        '''
        Draw all the connections in this netlist. Returns the amount of paths not calculated
        :param board:  a threedimensional Numpy array
        '''
        path_number = settings.SIGN_PATH_START
        amount_fail = 0
        amount_paths = 0

        for connection in self.list:
            # Get the coordinates of the two gates in this connection
            a = connection[0]
            b = connection[1]            
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
            amount_paths += 1

        return amount_paths, amount_fail

    def print_list(self):
        '''
        Print function for debugging
        '''
        print(self.list)

class Path:
    """
    Path from A to B
    :param coordA:     first point on the board (list of Z, Y, X coordinates)
    :param coordB:     second point on the board (list of  Z, Y, X coordinates)
    :param aLabel:     the ID of this path
    :param aColor:     the color for plotting
    """

    def __init__(self, coordA, coordB, aLabel, aColor):
        self.label = aLabel
        self.path = []
        self.a = coordA
        self.b = coordB
        self.color = aColor

    def add_coordinate(self, coord):
        '''
        Adds a new coordinate to self.path
        :param coord:       a list of [Z, Y, X]
        '''
        self.path.append(coord)

    def calculate(self, algorithm, board):
        '''
        Calculate route between two points
        :param board:       a threedimensional Numpy array
        :param algorithm:   algorithm to draw the path
        '''

        if algorithm == "DIJKSTRA":
            return self.calculate_DIJKSTRA(board)

        if algorithm == "ASTAR":
            return self.calculate_ASTAR(board)

    def calculate_ASTAR(self, board):
        '''
        Calculate route between two points with the A* algorithm
        :param board: a threedimensional Numpy array
        '''

        a_tpl = tuple(self.a)
        b_tpl = tuple(self.b)

        # Create data structures
        queue = QueuePriority()
        queue.push(a_tpl, 0)

        cost_archive = {}
        cost_archive[a_tpl] = 0
        
        path_archive = {}
        path_archive[a_tpl] = None

        found = False

        # Keep searching till queue is empty or target is found
        while not queue.empty():

            # Pop first coordinate from queue
            current = queue.pop()
            current_tpl = tuple(current)

            # Check if this is the target
            if current_tpl == b_tpl:
                found = True
                break

            # Create all neighbors of this coordinate
            for neighbor in board.get_neighbors(current):

                # Create a tuple
                neighbor = tuple(neighbor)

                # --------------- HEURISTICS ----------------

                # Check if this coordinate on the board is empty
                if board.board[neighbor[0], neighbor[1], neighbor[2]] != 0:
                    if neighbor != b_tpl:
                        continue

                # Save its distance from the start
                cost_neighbor = cost_archive[current_tpl] + 1;

                # Sum surrounding gates
                for next_neighbor in board.get_neighbors(neighbor):

                    # If next_neighbor is a gate
                    gate = board.gatesObjects[next_neighbor[0], next_neighbor[1], next_neighbor[2]]
                    if gate != None:

                        # Make the cost higher if gate has more connections
                        for i in range(gate.spaces_needed):
                            cost_neighbor += settings.ASTAR_WEIGHT

                # Check if this coordinate is new or has a lower cost than before
                if neighbor not in cost_archive \
                   or cost_neighbor < cost_archive[neighbor]:
                
                    # Calculate the cost and add it to the queue
                    cost_archive[neighbor] = cost_neighbor
                    prior = cost_neighbor + board.calculate_distance(neighbor, b_tpl)
                    queue.push(neighbor, prior)

                    # Remember where this neighbor came from
                    path_archive[neighbor] = current

                # -------------- / HEURISTICS ---------------

        # Backtracking the path        
        if found:

            # Add destination to the path route
            self.add_coordinate(self.b)

            cursor = path_archive[b_tpl]
            
            while cursor != a_tpl:
                # Put the ID in the Numpy board
                board.board[cursor[0], cursor[1], cursor[2]] = self.label

                # Remember this coord for this path
                self.add_coordinate([cursor[0], cursor[1], cursor[2]])
                
                cursor = path_archive[cursor]
            
            # Add A to the path
            self.add_coordinate(self.a)

            # Reduce the needed spaces for gate A and B
            board.gatesObjects[self.a[0], self.a[1], self.a[2]].spaces_needed -= 1
            board.gatesObjects[self.b[0], self.b[1], self.b[2]].spaces_needed -= 1

            return True
        
        else:
            return False

    def calculate_DIJKSTRA(self, board):
        '''
        Calculate route between two points with the Dijkstra algorithm
        :param board: a Numpy array
        '''

        # Initiate the dimantions of the board
        boardDimensions = board.board.shape
        boardDepth = boardDimensions[0]
        boardHeight = boardDimensions[1]
        boardWidth = boardDimensions[2]
        a_tpl = tuple(self.a)
        b_tpl = tuple(self.b)
        
        # Initiate counters
        loops = 0
        found = False

        # Initiate numpy data structures
        archive = np.zeros((boardDepth, boardHeight, boardWidth), dtype=int)

        # Add destination to the path route
        self.add_coordinate(self.b)

        queue = Queue()
        queue.push(self.a)

        # Algorithm core logic
        while not queue.empty() and found == False:

            # Track the distance
            loops += 1

            # Pick first coordinate from the queue
            current = queue.pop()
            current_tpl = tuple(current)

            # Create all neighbors of this coordinate
            for neighbor in board.get_neighbors(current):
                neighbor = tuple(neighbor)

                # Check if this is the target
                if neighbor == b_tpl:
                    found = True
                    break

                # --------------- HEURISTICS ----------------

                # Check if this coord is already in the archive
                if archive[neighbor[0], neighbor[1], neighbor[2]] != 0:
                    continue

                # Check if there are no obstacles on this coord
                if board.board[neighbor[0], neighbor[1], neighbor[2]] > 0:
                    continue

                # Check surrounding tiles for gates that need space
                for neighbor_next in board.get_neighbors(neighbor):
                    neighbor_next = tuple(neighbor_next)

                    # Check if this gate needs space around it
                    if board.gatesObjects[neighbor_next[0], neighbor_next[1], neighbor_next[2]] != None:

                        # Don't look at the own gates
                        if not (neighbor_next == a_tpl) or (neighbor_next == b_tpl):

                            # Get info from this gate
                            gate = board.gatesObjects[neighbor_next[0], neighbor_next[1], neighbor_next[2]]

                            # See if the path may pass
                            if gate.get_free_spaces(board, neighbor_next) == 0:
                                continue

                # -------------- / HEURISTICS ---------------

                # Add the coord to the queue
                queue.push(list(neighbor))

                # Save the iteration counter to this coordinate in the archive
                archive[neighbor[0], neighbor[1], neighbor[2]] = loops

        # Backtracking the shortest route
        if found:
            cursor = list(self.b)

            # Loop back the all the made steps
            for i in range(loops - 1, 0, -1):

                # Loop through all the neighbors of this tile
                for neighbor in board.get_neighbors(cursor):

                    neighbor = tuple(neighbor)

                    # Check if this cell is on the i'th position in the shortest path
                    if archive[neighbor[0], neighbor[1], neighbor[2]] == i:

                        # Put the ID in the Numpy board
                        board.board[neighbor[0], neighbor[1], neighbor[2]] = self.label

                        # Remember this coord for this path
                        self.add_coordinate([neighbor[0], neighbor[1], neighbor[2]])

                        # Move the cursor
                        cursor = list(neighbor)
                        break

            # Add the starting point to the end of the path-list
            self.add_coordinate(self.a)

            # Add 1 to the made connections for gate A and B            
            board.gatesObjects[self.a[0], self.a[1], self.a[2]].spaces_needed -= 1
            board.gatesObjects[self.b[0], self.b[1], self.b[2]].spaces_needed -= 1

            return True

        else:
            return False

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

class Queue:
    '''
    Dequeue, append and count elements in a simple queue
    :param: none
    '''

    def __init__(self):
        self.elements = collections.deque()
    
    def empty(self):
        return len(self.elements) == 0
    
    def pop(self):
        return self.elements.popleft()
    
    def push(self, x):
        self.elements.append(x)

class QueuePriority:
    '''
    Dequeue, append and count elements in a priority queue
    :param: none
    '''

    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def pop(self):
        return heapq.heappop(self.elements)[1]

    def push(self, coord, prior):
        heapq.heappush(self.elements, (prior, coord))