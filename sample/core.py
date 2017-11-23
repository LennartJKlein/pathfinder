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
import colors as CLR
import settings

def main():
    '''
    Initialise and draw a grid called Board
    Read gate locations from gates file
    '''

    # Config NumPy
    np.set_printoptions(threshold=np.nan)

    # Initiate a board with a specified size
    board = helpers.Board(settings.BOARD_WIDTH, settings.BOARD_HEIGHT, settings.BOARD_DEPTH)

    # Create a netlist and calculate path
    netlist = helpers.Netlist(settings.FILE_NETLIST)

    # Read a CSV file for gate tuples
    with open('data/gates'+ str(settings.FILE_GATES) + '.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        print("Using gates file #" + str(settings.FILE_GATES))
        print("")

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
                board.board[gateZ, gateY, gateX] = settings.SIGN_GATE

    # Calculate the connections in this netlist
    netlist.execute_connections(board)

    # Print the board data
    board.print_board()

    # Plot the board
    board.plot()

if __name__ == '__main__':
    main()
