"""This file contains the logic to run the __main__.py body of the program.

Name: classes.py

Authors:
- Jurre Brandsen
- Lennart Klein
- Thomas de Lange

LICENSE: MIT
"""

import collections
from collections import Counter
import copy
import csv
import heapq
import random
import sys
from ast import literal_eval

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import colors as CLR
import helpers
import settings


class Board(object):
    """Create a numpy board filled with numpy zeros upon initialising."""

    def __init__(self, width, height, depth):
        """Initialing the varables of this class.

        :type widht: interger
        :param width: How many columns the board uses

        :type height: interger
        :param height: How many rows the board uses

        :type depth: interger
        :param depth: How many layers the board uses
        """
        self.width = width
        self.height = height
        self.depth = depth
        self.board = np.zeros((self.depth, self.height, self.width), dtype=int)

        self.gates_objects = np.empty((self.depth,
                                       self.height,
                                       self.width), dtype=object)

        self.gates_numbers = np.zeros((self.depth,
                                       self.height,
                                       self.width), dtype=int)

        self.paths = []
        self.paths_broken = []
        self.paths_drawn = []

    def draw_paths(self):
        """Draw all the paths for this board (if possible)."""
        # Calculate the route for this path
        for path in self.paths:
            result = path.draw(settings.PATH_ALGORITHM, self)
            # Save the results of this execution
            if result:
                self.paths_drawn.append(path)
            else:
                self.paths_broken.append(path)

    def redraw_broken_path(self):
        """Get first broken path."""
        broken_path = self.paths_broken.pop(0)
        broken_path.undraw(self)

        amount_drawn_paths = len(self.paths_drawn)

        # Undraw other paths one by one
        for i in range(amount_drawn_paths):

            # Get and undraw first path
            drawn_path = self.paths_drawn.pop(0)
            drawn_path.undraw(self)

            # Try to draw broken path
            if broken_path.draw(settings.PATH_ALGORITHM, self):
                self.paths_drawn.append(broken_path)

                # Try to draw the removed path again
                if drawn_path.draw(settings.PATH_ALGORITHM, self):
                    self.paths_drawn.append(drawn_path)
                else:
                    self.paths_broken.append(drawn_path)

                return True
            else:
                # Reset the removed path
                drawn_path.draw(settings.PATH_ALGORITHM, self)
                self.paths_drawn.append(drawn_path)

        # Couldn't fix this broken path
        self.paths_broken.append(broken_path)
        return False

    def shorten_every_path(self):
        """Redraw every path with DIJKSTRA pathfinding."""
        for path in self.paths:
            path.undraw(self)
            path.draw("DIJKSTRA", self)

    def redraw_random_path(self):
        """Pick three random paths."""
        paths = []
        index = random.randint(1, len(self.paths_drawn) - 1)
        paths.append(self.paths_drawn.pop(len(self.paths_drawn) - index))
        paths.append(self.paths_drawn.pop(len(self.paths_drawn) - 1 - index))

        for path in paths:
            # Undraw the path
            path.undraw(self)

        temp_cost = settings.COST_PASSING_GATE
        settings.COST_PASSING_GATE = 0

        for path in paths:
            # Redraw the path
            if path.draw("ASTAR", self):
                self.paths_drawn.append(path)
            else:
                self.paths_broken.append(path)

        settings.COST_PASSING_GATE = temp_cost

    def get_result(self, type_):
        """Look at the path and analyze if it is commplete.

        :type type_: string
        :param type_: Returned value of a drawn line.
        """
        if type_ == "average":
            return round(len(self.paths_drawn) / len(self.paths) * 100, 2)
        if type_ == "made":
            return len(self.paths_drawn)
        if type_ == "broken":
            return len(self.paths_broken)

    def get_coords(self, axes, label):
        """Get the coordinate of a board with it's label.

        :type axes: string
        :param axes: Devided coord into Z, Y, X

        :type label: numpy(object)
        :param label: Get a coord in board the corresponding label

        :rtype: tuple
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

    def reset_coordinate(self, z, y, x):
        """Reset the coordinates of a board to 0.

        :type z: interger
        :type y: interger
        :type x: interger
        """
        self.board[z, y, x] = 0

    def get_neighbors(self, coord):
        """Get the neighbors of a given coordinate.

        :type coord: coord(tuple)
        :param coord: A coordinate on the board

        :rtype: interger
        """
        (z, y, x) = coord
        valid_coords = []

        neighbors = [[z, y, x+1], [z, y, x-1], [z, y+1, x],
                     [z, y-1, x], [z+1, y, x], [z-1, y, x]]

        for neighbor in neighbors:
            # Check if the coord is positive
            if any(axes < 0 for axes in neighbor):
                continue

            # Check if the coord falls within the board
            if neighbor[2] >= settings.BOARD_WIDTH or \
               neighbor[1] >= settings.BOARD_HEIGHT or \
               neighbor[0] >= settings.BOARD_DEPTH:
                continue

            # Add this neighbor to the output
            valid_coords.append(neighbor)

        return valid_coords

    def get_score(self):
        """Accumulated length of all the paths.

        :rtype: interger
        """
        return len(np.argwhere(self.board >= settings.SIGN_PATH_START))

    def plot(self):
        """Graph configurations uses plt from the ."""
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_zlim(self.depth, 0)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        for path in self.paths:
            ax.plot(path.get_coords('x'),
                    path.get_coords('y'),
                    path.get_coords('z'),
                    zorder=-1)

        # Add gates to the graph
        ax.scatter(self.get_coords('x', settings.SIGN_GATE),
                   self.get_coords('y', settings.SIGN_GATE),
                   self.get_coords('z', settings.SIGN_GATE),
                   color="black")

        # Show the graph
        plt.show()

    def print_board(self):
        """Show the numpyboard in ASCII."""
        np.set_printoptions(threshold=np.nan)
        print(self.board)

    def set_gates(self, gates):
        """Set the gates on the board.

        :type gates: Gate(object)
        :param gates: Give the selected netlist in settings.py.
        """
        # Set very gate in this board
        for gate in gates.gates:
            self.gates_objects[gate.z, gate.y, gate.x] = gate
            self.gates_numbers[gate.z, gate.y, gate.x] = gate.label
            self.board[gate.z, gate.y, gate.x] = gates.sign_gate

    def set_paths(self, netlist):
        """Set the value of the netlist and appends it to the numpyboard.

        :type netlist: Netlist(object)
        :param netlist: Get de netlist object and use it to set the paths
        """
        path_number = settings.SIGN_PATH_START

        for connection in netlist.list:
            # Get the coordinates of the two gates in this connection
            a = connection[0]
            b = connection[1]
            coordGateA = np.argwhere(self.gates_numbers == a + 1)
            coordGateB = np.argwhere(self.gates_numbers == b + 1)

            # Create a new path object
            new_path = Path(coordGateA[0], coordGateB[0], path_number, "grey")

            # Add this path to the board object
            self.paths.append(new_path)

            # Set a new path_number for the next path
            path_number += 1


class Gate(object):
    """Gate sets the gates in a board."""

    def __init__(self, label, x, y, z, spaces_needed):
        """Initiate the varables used by Gate.

        :type label: intergernt
        :param label: Label for a gate

        :type x: interger
        :param x: x-axis location

        :type y: interger
        :param y: y-axis location

        :type z: interger
        :param z: z-axis location

        :type spaces_needed: interger
        :param spaces_needed: Spaces needed in the gate to connect all paths
        """
        self.label = label
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.spaces_needed = spaces_needed

    def get_free_spaces(self, board, coord):
        """Interger with the amount of free spaces.

        :type board: numpy(object)
        :param board: a threedimensional Numpy array

        :type coord: interger
        :param coord:
        """
        counter = 0
        free_spaces = 0

        for neighbor in board.get_neighbors(coord):
            # Count if neighbor is free on the board
            if board.board[neighbor[0], neighbor[1], neighbor[2]] == 0:
                counter += 1

        return free_spaces - self.spaces_needed

    def __str__(self):
        """String return.

        :rtype self: String
        """
        return self.label


class Gates(object):
    """Gates Class that makes a board with gates."""

    def __init__(self, file_nr, amount, sign, netlist):
        """Initiate the Gates class.

        :type number: interger
        :param number: number of gates file used

        :type sign: interger
        :param sign: identifier of the gate

        :type netlist: Netlist(object)
        :param netlist: a netlist object to put in the Gates(object)

        :type number: interger
        :param number: identifier
        """
        self.gates = []
        self.sign_gate = sign

        # Read a CSV file for gate tuples
        file = "gates/gates-"+amount+"/"+file_nr+".csv"
        with open(file, 'r') as csvfile:
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
                        if (connection[0] + 1) == gateLabel or (
                                connection[1] + 1) == gateLabel:
                            spaces_needed += 1

                    # Save gate object in gates list
                    new_gate = Gate(gateLabel, gateX, gateY, gateZ, spaces_needed)
                    self.gates.append(new_gate)

    def reset_spaces_needed(self, netlist):
        """Reset the amount of spaces needed.

        :type netlist: Netlist(object)
        :param number: the netlist object
        """
        for gate in self.gates:

            gate.spaces_needed = 0
            for connection in netlist.list:
                if (connection[0] + 1) == gate.label or (
                        connection[1] + 1) == gate.label:
                    gate.spaces_needed += 1

    def get_gates(self):
        """Return the own gates data.

        :rtype: array
        """
        return self.gates


class Netlist(object):
    """Netlist are tuples reperesenting the contecion between two gates."""

    def __init__(self, file_nr, length):
        """All conections must be made to solve the case.

        :type number: interger
        :param number: id of the netlist
        """

        # Open netlist and read with literal evaluation
        self.filename = "length100/netlists/netlists-"+length+"/"+file_nr+".txt"
        with open(self.filename) as f:
            self.list = f.read()

        self.list = literal_eval(self.list)
        self.connections = len(self.list)

        # Order this list by importance of connections
        self.sort_by_connection()

    def swap_back_one(self, target):
        """Switch the target item with item before it.

        :type targer: tuple
        :param number: the netlist combination that must be switched
        """
        index = self.list.index(target)
        tmp = self.list[index - 1]
        self.list[index - 1] = self.list[index]
        self.list[index] = tmp

    def first_to_back(self):
        """Give back the first ellement with python pop."""
        self.list.append(self.list.pop(0))

    def sort_by_connection(self):
        """Rearrange self.list to a new array based connectins needed."""
        gate_list = []
        for connection in self.list:
            for gate in connection:
                gate_list.append(gate)

        counter_dict = dict(Counter(gate_list))

        # Loop calculate the value of the tuple, make a
        # dict containing the values
        sorted_dict = {}
        for connection in self.list:
            value = counter_dict[connection[0]] + counter_dict[connection[1]]
            sorted_dict[connection] = value

        # Return the sorted array based on the items in revered order.
        self.list = sorted(sorted_dict,
                           key=sorted_dict.__getitem__,
                           reverse=True)


class Path(object):
    """Path from A to B."""

    def __init__(self, coordA, coordB, aLabel, aColor):
        """Initiate the path coordinates a label and the optional collor.

        :type coordA: interger
        :param coordA: first point on the board (list of Z, Y, X coordinates)

        :type coordB: interger
        :param coordB: second point on the board (list of  Z, Y, X coordinates)

        :type aLabel: interger
        :param aLabel: the ID of this path

        :type aColor: hexodecimal value
        :param aColor: the color for plotting
        """
        self.label = aLabel
        self.path = []
        self.a = coordA
        self.b = coordB
        self.color = aColor

    def add_coordinate(self, coord):
        """Add a new coordinate to self.path.

        :type coord: tuple
        :param coord:       a list of [Z, Y, X]
        """
        self.path.append(coord)

    def undraw(self, board):
        """Remove paths from the board.

        :type board: Board(object)
        :param board: a threedimensional Numpy array
        """
        # Add one to the needed connections for gate A and B
        board.gates_objects[self.a[0], self.a[1], self.a[2]].spaces_needed += 1
        board.gates_objects[self.b[0], self.b[1], self.b[2]].spaces_needed += 1

        # Loop through every coord of the path
        for coord in self.path:
            # Reset this coord on the board to 0
            if board.board[coord[0], coord[1], coord[2]] != settings.SIGN_GATE:
                board.reset_coordinate(coord[0], coord[1], coord[2])

        # Empty the path list
        self.path = []

    def draw(self, algorithm, board):
        """Calculate route between two points.

        :type board: Board(object)
        :param board: a threedimensional Numpy array

        :type algorithm: method
        :param algorithm:  algorithm to draw the path
        """
        if algorithm == "DIJKSTRA":
            return self.draw_DIJKSTRA(board)

        if algorithm == "ASTAR":
            return self.draw_ASTAR(board)

    def draw_ASTAR(self, board):
        """Calculate route between two points with the A* algorithm.

        :type board: Board(object)
        :param board: a threedimensional Numpy array
        """
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

                # Calculate distance to goal
                cost_neighbor = cost_archive[current_tpl] + 1
                cost_neighbor += helpers.calculate_delta(neighbor, b_tpl)

                # Make it cheaper to go deeper
                cost_neighbor += ((board.depth - neighbor[0]) * 25)

                # Make expensive if passing a gate
                if neighbor[0] < 2:
                    for next_neighbor in board.get_neighbors(neighbor):

                        # If next_neighbor is a gate
                        gate = board.gates_objects[next_neighbor[0],
                                                   next_neighbor[1],
                                                   next_neighbor[2]]
                        if gate != None:

                            # Make the cost higher if gate has more connections
                            for i in range(gate.spaces_needed):
                                cost_neighbor += settings.COST_PASSING_GATE

                # Check if this coordinate is new or has a lower cost than before
                if neighbor not in path_archive \
                   or (neighbor in cost_archive and cost_neighbor < cost_archive[neighbor]):

                    # Calculate the cost and add it to the queue
                    cost_archive[neighbor] = cost_neighbor
                    prior = cost_neighbor
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
            board.gates_objects[self.a[0],
                                self.a[1],
                                self.a[2]].spaces_needed -= 1

            board.gates_objects[self.b[0],
                                self.b[1],
                                self.b[2]].spaces_needed -= 1

            return True

        else:
            return False

    def draw_DIJKSTRA(self, board):
        """Calculate route between two points with the Dijkstra algorithm.

        :type board: Board(object)
        :param board: a threedimensional Numpy array
        """
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
            # current_tpl = tuple(current)

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
                    if board.gates_objects[neighbor_next[0],
                                           neighbor_next[1],
                                           neighbor_next[2]] != None:

                        # Don't look at the own gates
                        if not (neighbor_next == a_tpl) or (neighbor_next == b_tpl):

                            # Get info from this gate
                            gate = board.gates_objects[neighbor_next[0],
                                                       neighbor_next[1],
                                                       neighbor_next[2]]

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
            board.gates_objects[self.a[0],
                                self.a[1],
                                self.a[2]].spaces_needed -= 1

            board.gates_objects[self.b[0],
                                self.b[1],
                                self.b[2]].spaces_needed -= 1

            return True

        else:
            #if settings.SHOW_EACH_RESULT
                #print("Path " + str(self.label) + " ERROR. Could not be drawn.")
            return False

    def get_coords(self, axes):
        """Get coordinates of point with axes as input.

        :type axes: tuple
        :param number: tuple with value of x, y and z
        """
        coords = []

        for coord in self.path:
            if axes == 'z':
                coords.append(coord[0])
            if axes == 'y':
                coords.append(coord[1])
            if axes == 'x':
                coords.append(coord[2])
        return coords


class Solution(object):
    """Is a wraper class for all functions."""

    def __init__(self):
        """Initiate the variables non needed as arguments."""
        self.best_board = None
        self.best_netlist = None
        self.best_score = 0
        self.best_result = 0

        self.boards = 0
        self.scores = []
        self.results = []

    def get_scores(self):
        """Get all scores in the scores list.

        :rtype: array
        """
        return self.scores

    def plot_scores(self):
        """Plot a graph to show the scores over the different iterations."""
        fig = plt.figure()
        ax = fig.gca()
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Score")
        ax.plot(self.scores)
        plt.show()

    def plot_results(self):
        """Plot a graph to show the results over the different iterations."""
        fig = plt.figure()
        ax = fig.gca()
        ax.set_xlabel("Iteration")
        ax.set_ylabel("Paths drawn (percent)")
        ax.plot(self.results)
        plt.show()

    def plot_best(self):
        """Plot the best result."""
        self.best_board.plot()

    def run(self, gates, netlist):
        """Run the file used in __main.py.

        :type gates: Gates(object)
        :param gates: a instanse of the Gate class

        :type netlist: Netlist(object)
        :param netlist: a instanse of the Netlist class
        """
        # Print inputted netlist
        if settings.SHOW_NETLIST:
            print("Netlist: " + CLR.GREEN + str(netlist.list) + CLR.DEFAULT)
            print("--------------------------------------------------------")

        # Set temporary counters
        no_path_improvements = 0

        # Create a new board
        board = Board(settings.BOARD_WIDTH,
                      settings.BOARD_HEIGHT,
                      settings.BOARD_DEPTH)

        # Place gates and paths on this board
        board.set_gates(gates)
        board.set_paths(netlist)

        # Draw the paths
        board.draw_paths()

        while no_path_improvements <= settings.MAX_NO_IMPROVE:

            # Count this iteration
            self.boards += 1

            # Get the results of this board
            result = board.get_result("average")
            score = board.get_score()

            # Save the scores and result of this iteration
            self.results.append(result)
            self.scores.append(score)

            # Show result of the board
            if settings.SHOW_EACH_RESULT:
                # TODO eventueel ook in __main__.py
                sys.stdout.flush()
                print("Board "
                      + CLR.YELLOW + "#"
                      + str(self.boards)
                      + CLR.DEFAULT, end=":  ")

                print("Paths drawn: "
                      + CLR.YELLOW
                      + str(result)
                      + "%"
                      + CLR.DEFAULT, end="    ")

                print("Score: "
                      + CLR.YELLOW
                      + str(score)
                      + CLR.DEFAULT, end="    ")

                print("Value 'passing gate': "
                      + CLR.YELLOW
                      + str(settings.COST_PASSING_GATE)
                      + CLR.DEFAULT)

            # Plot result of the board
            if settings.SHOW_EACH_PLOT:
                board.plot()

            # Create a copy of this board for next iteration
            board_new = copy.deepcopy(board)
            board_new.paths = []
            board_new.paths_drawn = []
            board_new.paths_broken = []

            for path in board.paths:
                board_new.paths.append(copy.deepcopy(path))

            for path in board.paths_drawn:
                board_new.paths_drawn.append(copy.deepcopy(path))

            for path in board.paths_broken:
                board_new.paths_broken.append(copy.deepcopy(path))

            # See if this board has better scores
            if self.best_score == 0 \
               or result > self.best_result \
               or (result == self.best_result and score < self.best_score):

                self.best_score = score
                self.best_result = result
                self.best_board = board

            else:
                # Count the no improvement on the score
                no_path_improvements += 1

                # Delete this board
                for path in board.paths:
                    del path
                del board

            # Fetch new board for next iteration
            board = board_new

            if len(board.paths_broken) > 0:
                # Try to repair the broken paths
                board.redraw_broken_path()
            else:
                # Make mutations on the paths
                board.shorten_every_path()
                board.redraw_random_path()

        # Print best result of this run TODO: In __main__.py
        if settings.SHOW_BEST_RESULT:
            print("")
            print("------------ BEST RESULT out of "
                  + str(self.boards)
                  + " boards ---------------")

            print("Paths drawn: "
                  + CLR.GREEN
                  + str(self.best_result)
                  + "%" + CLR.DEFAULT)

            print("Score: "
                  + CLR.GREEN
                  + str(self.best_score)
                  + CLR.DEFAULT)

        # Set adapted heuristics for next run
        settings.COST_PASSING_GATE += settings.STEP_COST_PASSING_GATE


class Queue(object):
    """Dequeue, append and count elements in a simple queue."""

    def __init__(self):
        """Initiate the class with elements of the queue."""
        self.elements = collections.deque()

    def empty(self):
        """Empty the queue.

        :rtype: interger
        """
        return len(self.elements) == 0

    def pop(self):
        """Pop a queue item.

        :rtype: Collections(object)
        """
        return self.elements.popleft()

    def push(self, x):
        """Push an element to the queue."""
        self.elements.append(x)


class QueuePriority(object):
    """Dequeue, append and count elements in a priority queue."""

    def __init__(self):
        """Initiate the elements array."""
        self.elements = []

    def empty(self):
        """Empty the array.

        :rtype: interger
        """
        return len(self.elements) == 0

    def pop(self):
        """Pop elements from the queue.

        :rtype: tuple
        """
        return heapq.heappop(self.elements)[1]

    def push(self, data, prior):
        """Push an element on to the queue."""
        heapq.heappush(self.elements, (prior, data))
