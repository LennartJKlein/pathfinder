"""
core.py
Authors: - Jurre Brandsen
         - Lennart Klein
         - Thomas de Lange

Pathfinder will find the most efficient path between two gates on a board.
"""

import settings

from classes import Solution
from classes import Gates
from classes import Netlist

def main():
    """" 
    Initialise and draw a grid called Board
    Read gate locations from gates file
    """
    
    # Print program settings
    print("Using netlist #" + str(settings.FILE_NETLIST))
    print("Using gates file #" + str(settings.FILE_GATES))
    print("Using pathfinding algorithm " + str(settings.PATH_ALGORITHM))
    print("")

    # Initiate a new netlist
    netlist = Netlist(settings.FILE_NETLIST)
    # netlist.sort_by_connection()

    # Initiate the gates
    gates = Gates(settings.FILE_GATES, settings.SIGN_GATE, netlist)

    # 
    # COMMANDS TO OPTIMIZE NETLIST HERE
    # 

    # Initiate a new solution
    solution = Solution()
    solution.run(gates, netlist)

    # Plot solution information
    if settings.PLOT_SCORES:
        solution.plot_scores()

if __name__ == '__main__':
    main()
