"""
core.py
Authors: - Jurre Brandsen
         - Lennart Klein
         - Thomas de Lange

Pathfinder wil find the most efficient path between two gates on a board.

"""

import csv
from helpers import *

# Program settings
BOARD_WIDTH = 6
BOARD_HEIGHT = 6
FILE_GATES = 'csv/gates.csv'

# Initiate a board with a specified size
board = Board(BOARD_WIDTH, BOARD_HEIGHT, True)

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

        # Mark the steps
        board.set_gate("#", cursor["x"], cursor["y"])

        counter += 1


    print("Steps made: " + str(counter))


def main():
    '''
    Initialise and draw a grid called Board
    Read gate locations from 'gates.csv'
    '''

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
                board.set_gate(gateName, gateX, gateY)

    # Test
    calculatePath((1,1),(3,2))

    # Print the board
    board.show_board()

if __name__ == '__main__':
    main()
