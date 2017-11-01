#___________________________________________________________________________
# pathfinder.py                                                             |
#                                                                           |
# Authors: - Jurre Brandsen                                                 |
#          - Lennart Klein                                                  |
#          - Thomas de Lange                                                |
#                                                                           |
# Pathfinder will find the most efficient path between two gates.           |
#___________________________________________________________________________|

import csv
import netlist as Netlist
from board import *

def calculatePath(a, b):
    '''
    TODO
    '''

    # Calculate route between two points (coordinates used as tuples)
    ax = a[0]
    ay = a[1]
    bx = b[0]
    by = b[1]
    cursor = {"x": ax, "y": ay}
    counter = 0

    # Walk 1 step through the grid till the endpoint is found
    while (cursor["x"] != bx) or (cursor["y"] != by):
    
        if cursor["x"] < bx:
            cursor["x"] += 1
            print("right")
        elif cursor["x"] > bx:
            cursor["x"] -= 1
            print("left")
        elif cursor["y"] < by:
            cursor["y"] += 1
            print("up")
        elif cursor["y"] > by:
            cursor["y"] -= 1
            print("down")

        counter += 1

    print("Steps made: " + str(counter))


def main():
    '''
    Initialise and draw a grid called Board
    Read gate locations from the csv-file: 'gates.csv'
    '''

    # Determine X and Y of the board
    b = Board(10, 10, True)

    # Open the CSV file 'gates.csv'
    with open('gates.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            gate = row

            # retrieve X cord in csv-file
            gateX = ','.join(gate[1])

            # retrieve Y cord in csv-file
            gateY = ''.join(gate[2]).strip(")")
            
            # Turn the cord into intergers
            gateX = int(gateX)
            gateY = int(gateY)

            # Set a gate in the grid for every row in the csv-file
            b.set_gate(gateX, gateY)

    # initialise board
    b.show_board()

if __name__ == '__main__':
    main()