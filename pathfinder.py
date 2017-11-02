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
BOARD_WIDTH = 5
BOARD_HEIGHT = 5
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
        
        # Skip the header
        next(reader, None)
        
        for row in reader:
        
            # Skip row if the data is commented
            if row[0][:1] != '#':

                # Get the name of the gate
                gateName = row[0]            

                # Fetch the coords X and Y
                gateX = int(row[1])
                gateY = int(row[2])

                # Set a gate in the grid for every row in the file
                b.set_gate(gateName, gateX, gateY)

    # Print the board
    b.show_board()

if __name__ == '__main__':
    main()