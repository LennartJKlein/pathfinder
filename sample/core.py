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
    test_counter = 0
    set_trace()
    # while connections_compleet == True:

    np.set_printoptions(threshold=np.nan)

    # Make history log for used netlists
    netlist_log = Netlist_log(1)

    complete_list_found = False
    counter = 0
    while complete_list_found != True:
        # Create a netlist and calculate path
        netlist = Netlist(netlist_log.lists_log[0])
        print("--- Netlist used: ")
        print(netlist_log.lists_log[0])
        counter += 1

        if counter > 5:
            print("NETLIST LOG: ")
            for items in netlist_log.lists_log:
                print(items)
            exit()
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

        if complete_list_found != True:
            new_netlist = netlist.switch_back_one(complete_list_found)
            netlist_log.push_list(new_netlist)
            # print(new_netlist)
            # netlist_log.push_list(new_netlist)
    # Plot the board
    board.plot()

if __name__ == '__main__':
    main()
