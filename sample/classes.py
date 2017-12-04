"""
helpers.py
- Cell
- Board
- Gate
- Netlist
- Calculate path
"""

import settings

import colors as CLR
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ast import literal_eval
import heapq
import collections
import heapq
import csv
import helpers

      
class Board:
    """
    Sum:
        Create a numpy board filled with numpy zeros upon initialising

    Attributes:
        width(int): How many columns the board uses
        height(int): How many rows the board uses
        depth(int): How many layers the board uses
        board(numpy): Multidimentional list
        paths(list): Collective of the paths in the board
        gate_objects(numpy): Ojects assigned to the board
        gate_numbers(numpy): Zeros assigned to the board

    """

    def __init__(self, width, height, depth):
        """
        Args:
            width(int): How many columns the board uses
            height(int): How many rows the board uses
            depth(int): How many layers the board uses
        """

        self.width = width
        self.height = height
        self.depth = depth
        self.board = np.zeros((self.depth, self.height, self.width), dtype=int)
        self.paths = []
        self.gates_objects = np.empty((self.depth, self.height, self.width), dtype=object)
        self.gates_numbers = np.zeros((self.depth, self.height, self.width), dtype=int)

    def get_coords(self, axes, label):
        """
        Args:
            axes(string): Devided coord into Z, Y, X
            label(numpy): Get a coord in board the corresponding label

        Return: 
            The current Z, Y, X of a coord in the numby board
        """

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
        """
        Args:
            coord(tuple): a coordinate on the board

        Return: 
            All valid neighbors of the given coordinate
        """

        (z, y, x) = coord
        valid_coords = []
        neighbors = [[z, y, x+1], [z, y, x-1], [z, y+1, x], [z, y-1, x], [z+1, y, x], [z-1, y, x]]
        for neighbor in neighbors:

            # Check if the coord is positive
            if any(axes < 0 for axes in neighbor):
                return continue

            # Check if the coord falls within the board
            if neighbor[2] >= settings.BOARD_WIDTH or \
               neighbor[1] >= settings.BOARD_HEIGHT or \
               neighbor[0] >= settings.BOARD_DEPTH:
                return continue  

            # Add this neighbor to the output
            valid_coords.append(neighbor)

        return valid_coords
    
    def get_score(self):
        """
        Return: 
            Accumulated length of all the paths
        """

        return len(np.argwhere(self.board >= settings.SIGN_PATH_START))

    def print_score(self):
        """
        Return: 
            Print the score
        """

        print(CLR.YELLOW + "Score: " + str(self.get_score()) + CLR.DEFAULT)
        print("")

    def plot_paths(self, graph, own_color):
        """
        Args:
            graph(matplotlib): Plot a graph
            color(matplotlib): Seperate the paths with a color

        Return: 
            Plot a graph with a score based on iterations
        """

        for path in self.paths:
            if own_color:
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
        """
        Return: 
            Graph configurations
        """

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
        """
        Return: 
            Show the numpyboard in ASCII
        """
        print(self.board)

    def set_gates(self, gates):
        """
        Args:
            netlist(obj): Give the selected netlist in settings.py
        """

        # Set very gate in this board
        for gate in gates.gates:

          self.gates_objects[gate.z, gate.y, gate.x] = gate
          self.gates_numbers[gate.z, gate.y, gate.x] = gate.label
          self.board[gate.z, gate.y, gate.x] = gates.sign_gate


class Gate:
    """
    PLACEHOLDER
    """
    def __init__(self, label, x, y, z, spaces_needed):
        """
        :param netlist: Give the selected netlist in settings.py 
        :param label: Label for a gate
        :param x:     x-axis location
        :param y:     y-axis location
        :param y:     z-axis location 
        """

        self.label = label
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.spaces_needed = spaces_needed

    def get_free_spaces(self, netlist, board, coord):
        """
        :return: Interger with the amount of free spaces
        """

        free_spaces = 0

        for neighbor in board.get_neighbors(coord):
            # Count if neighbor is free on the board
            if board.board[neighbor[0], neighbor[1], neighbor[2]] == 0:
                counter += 1

        return free_spaces - self.spaces_needed

    def __str__(self):
        return self.label

class Gates:

    def __init__(self, number, sign, netlist):

        self.gates = []
        self.sign_gate = sign

        # Read a CSV file for gate tuples
        with open('data/gates'+ str(number) + '.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)

            # Skip the header
            next(reader, None)

            for row in reader:

                # Skip row if the data is commented
                if row[0][:1] != '#':

                    # Get the name of the gate
                    gateLabel = int(row[0])

                    # Fetch the coords X and Y
                    gateX = int(row[1])
                    gateY = int(row[2])
                    gateZ = int(row[3])

                    # Get information on this gate from the netlist
                    spaces_needed = 0
                    for connection in netlist.list:
                        if (connection[0] + 1) == gateLabel or (connection[1] + 1) == gateLabel:
                            spaces_needed += 1

                    # Save gate object in gates list
                    new_gate = Gate(gateLabel, gateX, gateY, gateZ, spaces_needed)
                    self.gates.append(new_gate)
    
    def get_gates(self):
        return self.gates

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
        self.connections = 0
        self.connections_made = 0
        self.connections_broken = 0

        # Open netlist and read with literal evaluation
        with open(self.filename) as f:
            self.list = f.read()

        self.list = literal_eval(self.list)

    def execute_connections(self, board):
        '''
        Draw all the connections in this netlist. Saves the results of this execution
        :param board:  a threedimensional Numpy array
        '''
        path_number = settings.SIGN_PATH_START

        for connection in self.list:
            self.connections += 1

            # Get the coordinates of the two gates in this connection
            a = connection[0]
            b = connection[1]            
            coordGateA = np.argwhere(board.gates_numbers == a + 1)
            coordGateB = np.argwhere(board.gates_numbers == b + 1)

            # Create a new path object
            new_path = Path(coordGateA[0], coordGateB[0], path_number, "grey")

            # Add this path to the board object
            board.paths.append(new_path)

            # Calculate the route for this path
            result = new_path.calculate(settings.PATH_ALGORITHM, board)

            # Save the results of this execution
            if result == True:
                self.connections_made += 1
            else:
                self.connections_broken += 1

            # Set a new path_number for the next path
            path_number += 1

    def get_result(self, type):
        if type is "average":
            return self.connections_made / self.connections
        if type is "made":
            return self.connections_made
        if type is "broken":
            return self.connections_broken

    def print_result(self):
        print(CLR.YELLOW + "Paths drawn: " + str(self.connections_made) + " / " + str(self.connections) + CLR.DEFAULT)
        print(CLR.YELLOW + str(round(self.connections_made / self.connections * 100, 2)) + "%" + CLR.DEFAULT)
        print("")
    
    def switch_back_one(self, target):
        # Switch the target item with item before
        index = self.list.index(target)

        tmp = self.list[index - 1]
        self.list[index - 1] = self.list[index]
        self.list[index] = tmp
        return self.list

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
                cost_depth = 1 - neighbor[0] * 2
                cost_neighbor = cost_archive[current_tpl] + 14 + cost_depth;

                # Sum surrounding gates
                if neighbor[0] < 2:
                    for next_neighbor in board.get_neighbors(neighbor):

                        # If next_neighbor is a gate
                        gate = board.gates_objects[next_neighbor[0], next_neighbor[1], next_neighbor[2]]
                        if gate != None:

                            # Make the cost higher if gate has more connections
                            for i in range(gate.spaces_needed):
                                cost_neighbor += settings.ASTAR_WEIGHT

                # Check if this coordinate is new or has a lower cost than before
                if neighbor not in cost_archive \
                   or cost_neighbor < cost_archive[neighbor]:
                
                    # Calculate the cost and add it to the queue
                    cost_archive[neighbor] = cost_neighbor
                    prior = cost_neighbor + helpers.calculate_delta(neighbor, b_tpl)
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
            board.gates_objects[self.a[0], self.a[1], self.a[2]].spaces_needed -= 1
            board.gates_objects[self.b[0], self.b[1], self.b[2]].spaces_needed -= 1

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
                    if board.gates_objects[neighbor_next[0], neighbor_next[1], neighbor_next[2]] != None:

                        # Don't look at the own gates
                        if not (neighbor_next == a_tpl) or (neighbor_next == b_tpl):

                            # Get info from this gate
                            gate = board.gates_objects[neighbor_next[0], neighbor_next[1], neighbor_next[2]]

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
            board.gates_objects[self.a[0], self.a[1], self.a[2]].spaces_needed -= 1
            board.gates_objects[self.b[0], self.b[1], self.b[2]].spaces_needed -= 1

            return True

        else:
            print("Path " + str(self.label) + " ERROR. Could not be calculated.")

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

class Solution:
    """
    Sum:
        
        
    Attributes:

    """

    def __init__(self):
        """
        :param 
        :param 
        :param 
        :param

        :return: 
        """
        self.best_board = None
        self.best_netlist = None
        self.best_score = 0
        self.best_result = 0

        self.boards = []
        self.netlists = []
        self.scores = []
        self.results = []

    def get_boards(self):
        """
        return: Get all boards in the board list
        """

        return self.boards

    def get_netlists(self):
        """
        :return: Get all netlists in the netlist list
        """

        return self.netlists

    def get_scores(self):
        """
        return: Get all scores in the scores list
        """

        return self.scores

    def plot_scores(self):
        """
        :return: Plot a graph to show the scores over the different iterations
        """

        fig = plt.figure()
        ax = fig.gca()
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Score")
        ax.plot(self.scores)
        plt.show()

    def run(self, gates, netlist):
        
        count_no_improvements = 0

        while count_no_improvements < settings.MAX_NO_IMPROVE:

            # Remember this netlist
            self.netlists.append(netlist)

            # Create and remember a new board
            board = Board(settings.BOARD_WIDTH, settings.BOARD_HEIGHT, settings.BOARD_DEPTH)
            self.boards.append(board)

            # Place gates on this board
            board.set_gates(gates)

            # RUN EXECUTE MULTIPLE TIMES

            # Calculate the connections in this netlist
            netlist.execute_connections(board)

            # // RUN EXECUTE MULTIPLE TIMES

            # Save the scores and result of this iteration
            self.results.append(netlist.get_result("made"))
            self.scores.append(board.get_score())


            # See if this board has better scores
            if self.best_result < netlist.get_result("made") \
               and self.best_score < board.get_score():

                self.best_score = board.get_score()
                self.best_result = netlist.get_result("made")
                self.best_board = board
                self.best_netlist = netlist

            else:
                count_no_improvements += 1

            # ADAPT NETLIST HERE


            # # Print results of this execution
            # if show_results:
            #     print("------------ BOARD: " + str(len(self.boards)) + " --------------")
            #     print(netlist.get_result())
            #     print(board.get_score())

            # if show_data:
            #     board.print_board()

            # if show_plot:
            #     board.plot()

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

    def push(self, data, prior):
        heapq.heappush(self.elements, (prior, data))