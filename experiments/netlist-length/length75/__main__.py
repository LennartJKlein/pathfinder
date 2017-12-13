"""The executable file to run the pathfinder module.

file: __main__.py

Authors:
    - Jurre Brandsen
    - Lennart Klein
    - Thomas de Lange

Pathfinder will find the most efficient path between two gates on a board.
"""


# def main():
"""Main function to execute the pagage."""
import sys
import colors as CLR
import settings
from classes import Gates, Netlist, Solution

if len(sys.argv) < 5:
    print("ERROR. Correct usage: python netlist-length gates-amount gates-filenumber netlist-length netlist-filenumber")
else:

    settings.FILE_GATES = sys.argv[1]
    settings.FILE_GATES_NR = sys.argv[2]
    settings.FILE_NETLIST = sys.argv[3]
    settings.FILE_NETLIST_NR = sys.argv[4]

    if settings.SHOW_SETTINGS:
        # Print program settings
        print("")
        print("Using netlist: "
              + CLR.GREEN
              + str(settings.FILE_NETLIST)
              + CLR.DEFAULT)

        print("Using gates file: "
              + CLR.GREEN
              + str(settings.FILE_GATES)
              + CLR.DEFAULT)
        print("")

    # Initiate a new netlist
    netlist = Netlist(settings.FILE_NETLIST_NR, settings.FILE_NETLIST)

    # Initiate the gates
    gates = Gates(settings.FILE_GATES_NR, settings.FILE_GATES, settings.SIGN_GATE, netlist)

    # Initiate a new solution
    solution = Solution()
    solution.run(gates, netlist)

    # Plot solution information
    if settings.PLOT_SCORES:
        solution.plot_scores()

    # Plot solution information
    if settings.PLOT_RESULTS:
        solution.plot_results()

    # Plot solution board
    if settings.PLOT_BEST:
        solution.plot_best()

    # Simply return solutions for this netlist and gates
    if settings.RETURN_RESULTS:
        sys.stdout.write("[" + str(solution.best_result) + "," + str(solution.best_score) + "]")
        