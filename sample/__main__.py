"""The executable file to run the pathfinder module.

file: __main__.py

Authors: - Jurre Brandsen
         - Lennart Klein
         - Thomas de Lange

Pathfinder will find the most efficient path between two gates on a board.
"""


def main():
    """Main function to execute the pagage."""
    import colors as CLR
    import settings
    from classes import Gates, Netlist, Solution

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

    print("Using pathfinding algorithm: "
          + CLR.GREEN
          + str(settings.PATH_ALGORITHM)
          + CLR.DEFAULT)
    print("")

    # Initiate a new netlist
    netlist = Netlist(settings.FILE_NETLIST)

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


if __name__ == "__main__":
    main()
