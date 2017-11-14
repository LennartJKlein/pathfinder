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
BOARD_HEIGHT = 17
BOARD_DEPTH = 7
FILE_GATES = 'data/gates2.csv'


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
                board.set_gate(gateLabel, gateX, gateY, gateZ)

    # Create a netlist and calculate paths
    netlist = helpers.Netlist(0)
    for connection in netlist.list:
        a = connection[0]
        b = connection[1]
        a_tuple = (gates[a].x, gates[a].y, gates[a].z)
        b_tuple = (gates[b].x, gates[b].y, gates[b].z)
        helpers.calculatePath(board, a_tuple, b_tuple, 1)

    # Print the board
    board.print_board()

    # Plot the plot
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.scatter(board.get_coords('y', 2), board.get_coords('x', 2), board.get_coords('z', 2))
    ax.legend()

    plt.show()

if __name__ == '__main__':
    main()
