"""The executable file to run the pathfinder module.

file: __main__.py

Authors:
    - Jurre Brandsen
    - Lennart Klein
    - Thomas de Lange

Pathfinder will find the most efficient path between two gates on a board.
"""

"""Main function to execute the program."""
import colors as CLR
import settings
from classes import Gates, Netlist, Solution
import sys

if len(sys.argv) > 1:
    if not sys.argv[1].isdigit() or not sys.argv[2].isdigit() or int(sys.argv[1]) > 2 or int(sys.argv[2]) > 6:
        print("Usage: python sample gates-number netlist-number")
        exit()
    else:
        settings.FILE_GATES = int(sys.argv[1])
        settings.FILE_NETLIST = int(sys.argv[2])

        if settings.FILE_GATES > 1:
            settings.BOARD_HEIGHT = 17
        else:
            settings.BOARD_HEIGHT = 13

# Print program settings
if settings.PRINT_SETTINGS:
    print("")
    print("Using netlist: "
          + CLR.GREEN
          + str(settings.FILE_NETLIST)
          + CLR.DEFAULT)

    print("Using gates file: "
          + CLR.GREEN
          + str(settings.FILE_GATES)
          + CLR.DEFAULT)

    print("Using pathfinding algorithm: "
          + CLR.GREEN
          + str(settings.PATH_ALGORITHM)
          + CLR.DEFAULT)
    print("")
        
# Initiate a new netlist
netlist = Netlist(settings.FILE_NETLIST)

# Print inputted netlist
if settings.PRINT_NETLIST:
    print("Netlist: " + CLR.GREEN + str(netlist.list) + CLR.DEFAULT)
    print("--------------------------------------------------------")

# Initiate the gates
gates = Gates(settings.FILE_GATES, settings.SIGN_GATE, netlist)

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

# Return solutions for this run in a list/array
if settings.RETURN_RESULTS:
    sys.stdout.write("[" + str(solution.best_result) + "," + str(solution.best_score) + "]")