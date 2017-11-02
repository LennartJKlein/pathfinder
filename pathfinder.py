#___________________________________________________________________________
# pathfinder.py                                                             |
#                                                                           |
# Authors: - Jurre Brandsen                                                 |
#          - Lennart Klein                                                  |
#          - Thomas de Lange                                                |
#                                                                           |
# Pathfinder will find the most efficient path between two gates on a board.|
#___________________________________________________________________________|

import csv
import netlist as Netlist
from board import *

# Program settings
BOARD_WIDTH = 10
BOARD_HEIGHT = 10
FILE_GATES = 'gates.csv'

def calculatePath(a, b):
    '''
    Calculate route between two points
    :param a: first point (tuple of coordinates)
    :param b: second point (tuple of coordinates)
    '''
    ax = a[0]
    ay = a[1]
    bx = b[0]
    by = b[1]
    cursor = {"x": ax, "y": ay}
    counter = 0

    # Walk 1 step through the grid till the endpoint is reached
    while (cursor["x"] != bx) or (cursor["y"] != by):

        if cursor["x"] < bx:
            cursor["x"] += 1
            print("right")
        elif cursor["x"] > bx:
            cursor["x"] -= 1
            print("left")
        elif cursor["y"] < by:
            cursor["y"] += 1
            print("up")
        elif cursor["y"] > by:
            cursor["y"] -= 1
            print("down")

        counter += 1

    print("Steps made: " + str(counter))


def main():
    '''
    Initialise and draw a grid called Board
    Read gate locations from 'gates.csv'
    '''

    # Initiate a board with a specified size
    b = Board(BOARD_WIDTH, BOARD_HEIGHT, True)

    # Read a CSV file for gate tuples
    with open(FILE_GATES, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:

            # Get the name of the gate
            gateName = '('.join(row[0])

            # Get the X and Y coords of the gate
            gateX = ','.join(row[1])
            gateY = ''.join(row[2]).strip(")")
            
            # Turn the coords into intergers
            gateX = int(gateX)
            gateY = int(gateY)

            # Set a gate in the grid for every row in the file
            b.set_gate(gateName, gateX, gateY)

    # Print the board
    b.show_board()

if __name__ == '__main__':
    main()