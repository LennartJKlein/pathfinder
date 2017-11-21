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
BOARD_HEIGHT = 13
BOARD_DEPTH = 7
SIGN_PATH_START = 2
FILE_NETLIST = 1
FILE_GATES = 'data/gates1.csv'
PATH_NUMBER = 2 # start at two
SIGN_GATE = 1

def main():
    '''
    Initialise and draw a grid called Board
    Read gate locations from gates file
    '''

    np.set_printoptions(threshold=np.nan)
    # Initiate a board with a specified size
    board = helpers.Board(BOARD_WIDTH, BOARD_HEIGHT, BOARD_DEPTH)

    # Read a CSV file for gate tuples
    with open(FILE_GATES, 'r') as csvfile:
        reader = csv.reader(csvfile)
        print("Using: " + FILE_GATES)

        # Skip the header
        next(reader, None)

        # Initiate a list of gates
        gates = {}

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
                gates[gateLabel] = helpers.Gate(gateLabel, gateX, gateY, gateZ)

                # Set a gate in the grid for every row in the file
                board.set_gate(gateX, gateY, gateZ)

    # Create a netlist and calculate path
    netlist = helpers.Netlist(FILE_NETLIST)
    print("Using in Netlist #" + str(FILE_NETLIST))

    # Loop through every connection in the netlist
    label = SIGN_PATH_START
    for connection in netlist.list:
        a = connection[0]
        b = connection[1]
        a_list = [gates[a].z, gates[a].y, gates[a].x]
        b_list = [gates[b].z, gates[b].y, gates[b].x]

        # Create a new path object
        new_path = helpers.Path(a_list, b_list, label, "grey")

        # Add this path to the board object
        board.paths.append(new_path)

        # Calculate the route for this path
        new_path.calculate_DIJKSTRA(board)

        # Set a new label for the next path
        label += 1

    # Print the board data
    board.print_board()

    # Plot the board
    board.plot()

if __name__ == '__main__':
    main()
