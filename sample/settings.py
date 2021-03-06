"""Settings to be used by the classes.py."""

# Returns
RETURN_RESULTS = False

# Plots
PLOT_PROGRESS = True
PLOT_BEST = False
PLOT_SCORES = False
PLOT_RESULTS = False

# Export png's of the board
EXPORT_PROGRESS = False

# Prints
PRINT_SETTINGS = True
PRINT_NETLIST = True
PRINT_BEST_RESULT = True
PRINT_EACH_RESULT = True

# Program settings
FILE_NETLIST = 1
FILE_GATES = 1

BOARD_WIDTH = 18
BOARD_HEIGHT = 13
BOARD_DEPTH = 8

MAX_NO_IMPROVE = 15

# Pathfinding
PATH_ALGORITHM = "ASTAR"    # ASTAR / DIJKSTRA
COST_PASSING_GATE = 1000
STEP_COST_PASSING_GATE = 100

# Do not change
SIGN_PATH_START = 2
SIGN_GATE = 1
REALTIME_GRAPH = None
