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
    print("")

    # Keep track of results on different weights
    weights = []
    score = []

    # Experiment
    for i in range(settings.AMOUNT_BOARDS):

        # Initiate a board with a specified size
        board = Board(settings.BOARD_WIDTH, settings.BOARD_HEIGHT, settings.BOARD_DEPTH)

        # Create a netlist and calculate path
        netlist = Netlist(settings.FILE_NETLIST)

        # Read a CSV file for gate tuples
        with open('data/gates'+ str(settings.FILE_GATES) + '.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)

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
        amount_paths, amount_fail, amount_success = netlist.execute_connections(board)

        weights.append(settings.ASTAR_WEIGHT)
        score.append(amount_success)

        # APPEND SETTINGS
        settings.ASTAR_WEIGHT += 2

        # Print results of this execution
        # print("------------ BOARD: " + str(i) + " --------------")
        # print("Weight: " + str(settings.ASTAR_WEIGHT))
        # print(CLR.YELLOW + "Paths calculated: " + str(amount_success) + " / " + str(amount_paths) + CLR.DEFAULT)
        # print(CLR.YELLOW + str(round(amount_success / amount_paths * 100, 2)) + "%" + CLR.DEFAULT)
        # print("")
        # print(CLR.YELLOW + "Score: " + str(board.get_score()) + CLR.DEFAULT)
        # print("")
        # print("")

        # Print the board data
        # board.print_board()

        # Plot the board
        # board.plot()

    # Config graph plot for iteration information
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 60)
    ax.set_xlabel("Weight")
    ax.set_ylabel("Paths drawn")
    ax.plot(weights, score)
    plt.show()

if __name__ == '__main__':
    main()
