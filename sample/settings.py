"""Settings to be used by the classes.py."""

# Return result and score
RETURN_RESULTS = False

# Info at start of the program
SHOW_SETTINGS = False
SHOW_NETLIST = False

# Animated visualisation
PLOT_PROGRESS = True

# Show / plot results
PLOT_BEST = False
PLOT_SCORES = False
PLOT_RESULTS = False
SHOW_EACH_RESULT = False
SHOW_EACH_PLOT = False
SHOW_BEST_RESULT = False

# Program settings
BOARD_WIDTH = 18
BOARD_HEIGHT = 13
BOARD_DEPTH = 8

FILE_NETLIST = 1
FILE_GATES = 1

MAX_NO_IMPROVE = 5

PATH_ALGORITHM = "ASTAR"    # ASTAR / DIJKSTRA

# Heuristics for A*
COST_PASSING_GATE = 1000
STEP_COST_PASSING_GATE = 100

# Do not change
SIGN_PATH_START = 2
SIGN_GATE = 1
REALTIME_GRAPH = None