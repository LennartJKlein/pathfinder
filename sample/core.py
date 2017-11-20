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
BOARD_HEIGHT = 13
BOARD_DEPTH = 4
SIGN_PATH_START = 2
FILE_NETLIST = 1
FILE_GATES = 'data/gates1.csv'

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

    # Create a netlist and calculate paths
    netlist = helpers.Netlist(FILE_NETLIST)
    print("Using in Netlist #" + str(FILE_NETLIST))
    print("")
    pathsFound = SIGN_PATH_START
    for connection in netlist.list:
        a = connection[0]
        b = connection[1]
        a_list = (gates[a].z, gates[a].y, gates[a].x)
        b_list = (gates[b].z, gates[b].y, gates[b].x)
        helpers.calculatePath(board, a_list, b_list, pathsFound)
        pathsFound += 1

    # Print the board
    print("Board:")
    board.print_board()

    # Plot config
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim(0, BOARD_HEIGHT)
    ax.set_ylim(0, BOARD_WIDTH)
    ax.set_zlim(BOARD_DEPTH, 0)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Make a scatter graph with the get_coords function
    ax.scatter(board.get_coords('y', 1), board.get_coords('x', 1), board.get_coords('z', 1), color="blue")
    
    for i in range(len(netlist.list)):
        j = i + SIGN_PATH_START
        plt.plot(board.get_coords('y', j), board.get_coords('x', j), board.get_coords('z', j), color="grey")

    # Shot the finished product
    plt.show()

if __name__ == '__main__':
    main()
