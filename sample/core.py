"""
core.py
Authors: - Jurre Brandsen
         - Lennart Klein
         - Thomas de Lange

Pathfinder will find the most efficient path between two gates on a board.
"""

import settings

import numpy as np
import matplotlib.pyplot as plt
import csv

import classes
from classes import Board
from classes import Netlist
from classes import Gate
import colors as CLR

def main():
    '''
    Initialise and draw a grid called Board
    Read gate locations from gates file
    '''

    # Config NumPy
    np.set_printoptions(threshold=np.nan)

    # Show chosen settings
    print("Using netlist #" + str(settings.FILE_NETLIST))
    print("Using gates file #" + str(settings.FILE_GATES))

    # Keep track of results on different weights
    weights = []
    score = []

    for i in range(1):

        # Initiate a board with a specified size
        board = Board(settings.BOARD_WIDTH, settings.BOARD_HEIGHT, settings.BOARD_DEPTH)

        # Create a netlist and calculate path
        netlist = Netlist(settings.FILE_NETLIST)

        # Read a CSV file for gate tuples
        with open('data/gates'+ str(settings.FILE_GATES) + '.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
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
                    new_gate = Gate(netlist, gateLabel, gateX, gateY, gateZ)

                    # Set a gate in the grid for every row in the file
                    board.gatesObjects[gateZ, gateY, gateX] = new_gate
                    board.gatesNumbers[gateZ, gateY, gateX] = gateLabel
                    board.board[gateZ, gateY, gateX] = settings.SIGN_GATE

        # Calculate the connections in this netlist
        amount_paths, amount_fail = netlist.execute_connections(board)

        weights.append(settings.ASTAR_WEIGHT)
        score.append(amount_paths - amount_fail)

        settings.ASTAR_WEIGHT += 2

        if i == 4:
            board.plot()

    # Config graph plot
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(0, 50)
    ax.set_ylim(0, 30)
    ax.set_xlabel("Weight")
    ax.set_ylabel("Paths drawn")
    ax.plot(weights, score)

    plt.show()

    # Print results of this execution
    # amount_paths, amount_fail = netlist.execute_connections(board)
    # print(CLR.YELLOW + "Paths calculated: " + str(amount_paths - amount_fail) + " / " + str(amount_paths) + CLR.DEFAULT)
    # print(CLR.YELLOW + str(round((amount_paths - amount_fail) / amount_paths * 100, 2)) + "%" + CLR.DEFAULT)
    # print("")

    # Print the board data
    # board.print_board()

    # Plot the board
    # board.plot()

if __name__ == '__main__':
    main()
