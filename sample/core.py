"""
core.py
Authors: - Jurre Brandsen
         - Lennart Klein
         - Thomas de Lange

Pathfinder will find the most efficient path between two gates on a board.
"""

import csv
import helpers
import numpy as np

# Program settings
BOARD_WIDTH = 18
BOARD_HEIGHT = 17
BOARD_DEPTH = 7
FILE_NETLIST = 1
FILE_GATES = 'data/gates1.csv'
SIGN_GATE = 1

def main():
    '''
    Initialise and draw a grid called Board
    Read gate locations from gates file
    '''

    # Config NumPy
    np.set_printoptions(threshold=np.nan)

    # Initiate a board with a specified size
    board = helpers.Board(BOARD_WIDTH, BOARD_HEIGHT, BOARD_DEPTH)

    # Create a netlist and calculate path
    netlist = helpers.Netlist(FILE_NETLIST)

    # Read a CSV file for gate tuples
    with open(FILE_GATES, 'r') as csvfile:
        reader = csv.reader(csvfile)
        print("Using: " + FILE_GATES)

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

                # Save gate object in gates list
                new_gate = helpers.Gate(netlist, gateLabel, gateX, gateY, gateZ)

                # Set a gate in the grid for every row in the file
                board.gatesObjects[gateZ, gateY, gateX] = new_gate
                board.gatesNumbers[gateZ, gateY, gateX] = gateLabel
                board.board[gateZ, gateY, gateX] = SIGN_GATE

    # Calculate the connections in this netlist
    netlist.execute_connections(board)

    # Print the board data
    board.print_board()

    # Plot the board
    board.plot()

if __name__ == '__main__':
    main()
