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

def calculatePath(board, a, b, label):
    '''
    Calculate route between two points
    :param a: first point (tuple of coordinates)
    :param b: second point (tuple of coordinates)
    '''

    #cursor = {"x": ax, "y": ay, "z": az}
    counterLeft = 0
    counterRight = 0
    counterUp = 0
    counterDown = 0
    found = False

    # (X,Y,Z,COUNTER)
    queue = [a]

    a_list = list(a)
    b_list = list(b)

    print("Walking from gate: " + str(a_list) + " to " + str(b_list))
    print("")

    a_left = list(a)
    a_right = list(a)
    a_up = list(a)
    a_down = list (a)

    while not a_left == b_list or a_right == b_list or a_down == b_list or a_up == b_list:

        # # Create a list for the 4 adjacent cells
        # # X-axis

        a_left[0] -= 1
        counterLeft += 1
        print("Step left: " + str(a_left))

        # # If wall/gates/anything
        # if board.board[a_left[2], a_left[1], a_left[0]] == 0:
        #     print ("Free space found.")
        #     print ("Appending a_left to queue")
        #     # counterLeft += 1
        #     # a_left.insert(3, counterLeft)
        #     queue.append(a_left)
        #     print ("counting step")
        #     print ("queue is now:" + str(queue))
        #     print("")

        # else:
        #     print("No free space here.")
        #     print("")

        a_right[0] += 1
        counterRight += 1
        print("Step right: " + str(a_right))

        # # If wall/gates/anything
        # if board.board[a_right[2], a_right[1], a_right[0]] == 0:
        #     print ("Free space found.")
        #     print ("Appending a_right to queue")
        #     # counterRight += 1
        #     # a_right.insert(3, counterRight)
        #     queue.append(a_right)
        #     print ("counting step")
        #     print ("queue is now:" + str(queue))
        #     print("")

        # else:
        #     print("No free space here.")
        #     print("")

        # # # Y-axis
        a_up[1] -= 1
        counterUp -= 1
        print("Step up: " + str(a_up))

        # # If wall/gates/anything
        # if board.board[a_up[2], a_up[1], a_up[0]] == 0:
        #     print ("Free space found.")
        #     print ("Appending a_up to queue")
        #     # counterUp += 1
        #     # a_up.insert(3, counterUp)
        #     queue.append(a_up)
        #     print ("counting step")
        #     print ("queue is now:" + str(queue))
        #     print("")

        # else:
        #     print("No free space here.")
        #     print("")

        a_down[1] += 1
        counterDown += 1
        print("Step down: " + str(a_down))

        # # If wall/gates/anything
        # if board.board[a_down[2], a_down[1], a_down[0]] == 0:
        #     print ("Free space found.")
        #     print ("Appending a_down to queue")
        #     # counterDown += 1
        #     # a_down.insert(3, counterDown)
        #     queue.append(a_down)
        #     print ("counting step")
        #     print ("queue is now:" + str(queue))
        #     print("")

        # else:
        #     print("No free space here.")
        #     print("")

        # # Z-axis


        if a_left == b_list:
            print("")
            print("Found the gate after " + str(counterLeft) + " steps")
            break
        if a_right == b_list:
            print("")
            print("Found the gate after " + str(counterRight) + " steps")
            break
        if a_up == b_list:
            print("")
            print("Found the gate after " + str(counterUp) + " steps")
            break
        if a_down == b_list:
            print("")
            print("Found the gate after " + str(counterDown) + " steps")
            break

    print ("")


def compareTuples(a, b):

    # Check if tuple already is in a list
    compare_list = [(a == b) for a, b in zip(a,b)]
    return all(item == True for item in compare_list)



    # # Walk 1 step through the grid till the endpoint is reached
    # while (cursor["x"] != bx) or (cursor["y"] != by) or (cursor["z"] != bz):



    #     # Check if endpoint is reached
    #     if (cursor["x"] == bx) and (cursor["y"] == by) and (cursor["z"] == bz):
    #         found = True

    #     # Mark the steps while the endpoint is not reached
    #     if found ==  False:
    #         board.set_path(label, cursor["x"], cursor["y"], cursor["z"])

    #     counter += 1







    print("- Steps made: " + str(counter))