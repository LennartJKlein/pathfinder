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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Program settings
BOARD_WIDTH = 18
BOARD_HEIGHT = 16
BOARD_DEPTH = 1
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

    # Initiate a board with a specified size
    board = helpers.Board(BOARD_WIDTH, BOARD_HEIGHT, BOARD_DEPTH)

    # Read a CSV file for gate tuples
    with open(FILE_GATES, 'r') as csvfile:
        reader = csv.reader(csvfile)
        print("using: " + FILE_GATES)

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

    # Plot config
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Create a netlist and calculate path
    netlist = helpers.Netlist(FILE_NETLIST)

    print("Using in Netlist #" + str(FILE_NETLIST))
    label = SIGN_PATH_START
    for connection in netlist.list:
        a = connection[0]
        b = connection[1]
        a_tuple = (gates[a].x, gates[a].y, gates[a].z)
        b_tuple = (gates[b].x, gates[b].y, gates[b].z)

        # calculatePathe algorithm returns a object containig info about te route
        newPath = helpers.calculatePath(board, a_tuple, b_tuple, label)

        # Read the data in to a variable to read separete.
        path_data = newPath.return_path()

        # Plot the line. TODO label naar toevoegen.
        lines = plt.plot(path_data[0], path_data[1], path_data[2])

    # Print the board
    board.print_board()

    # Make a scatter graph with the get_coords function
    ax.scatter(board.get_coords('y', SIGN_GATE), board.get_coords('x', SIGN_GATE), board.get_coords('z', SIGN_GATE))

    # Shot the finished product
    plt.show()

if __name__ == '__main__':
    main()
