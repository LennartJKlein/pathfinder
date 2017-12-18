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
PRINT_SETTINGS = False
PRINT_NETLIST = False
PRINT_BEST_RESULT = False
PRINT_EACH_RESULT = False

# Program settings
FILE_NETLIST = 6
FILE_GATES = 2

BOARD_WIDTH = 18
BOARD_HEIGHT = 17
BOARD_DEPTH = 8

MAX_NO_IMPROVE = 5

# Pathfinding
PATH_ALGORITHM = "ASTAR"    # ASTAR / DIJKSTRA
COST_PASSING_GATE = 1000
STEP_COST_PASSING_GATE = 100

# Do not change
SIGN_PATH_START = 2
SIGN_GATE = 1
REALTIME_GRAPH = None
