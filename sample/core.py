"""
core.py
Authors: - Jurre Brandsen
         - Lennart Klein
         - Thomas de Lange

Pathfinder will find the most efficient path between two gates on a board.
"""

import csv
import helpers

# Program settings
BOARD_WIDTH = 6
BOARD_HEIGHT = 6
FILE_GATES = 'data/gates.csv'


def main():
    '''
    Initialise and draw a grid called Board
    Read gate locations from gates file
    '''

    # Initiate a board with a specified size
    board = helpers.Board(BOARD_WIDTH, BOARD_HEIGHT, True)

    # Read a CSV file for gate tuples
    with open(FILE_GATES, 'r') as csvfile:
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

    # Test path calculation
    helpers.calculatePath(board, (1,1), (3,2))

    # Print the board
    board.show_board()

if __name__ == '__main__':
    main()
