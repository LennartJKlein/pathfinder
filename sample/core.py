"""
core.py
Authors: - Jurre Brandsen
         - Lennart Klein
         - Thomas de Lange

Pathfinder will find the most efficient path between two gates on a board.
"""

import settings

import numpy as np
import csv

import classes
from classes import Board
from classes import Netlist
from classes import Gate
from classes import Netlist_log
import colors as CLR

def main():
    '''
    Initialise and draw a grid called Board
    Read gate locations from gates file
    '''

    # while connections_compleet == True:

    np.set_printoptions(threshold=np.nan)

    # Make history log for used netlists
    netlist_log = Netlist_log(1)

    complete_list_found = False
    while complete_list_found != True:
        # Create a netlist and calculate path
        netlist = Netlist(netlist_log.get_list())
        # Initiate a board with a specified size
        board = Board(settings.BOARD_WIDTH, settings.BOARD_HEIGHT, settings.BOARD_DEPTH)

        # Read a CSV file for gate tuples
        with open('data/gates'+ str(settings.FILE_GATES) + '.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            # print("Using gates file #" + str(settings.FILE_GATES))
            # print("")

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
        complete_list_found = netlist.execute_connections(board)
        print("--- Complete list found: ")
        print(complete_list_found)

        netlist_log.push_list(netlist.switch_back_one(complete_list_found))
        print("--- Netlist used: ")
        print(netlist_log.get_list())

        # Print the board data
        # board.print_board()

    print(netlist_log.get_list())
    # Plot the board
    board.plot()

if __name__ == '__main__':
    main()
