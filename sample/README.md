## Sample

This is where the magic happens.

## Notable content:

# data

The assignment contains 6 net lists and two gate files. Netlist 1-3 are used on gatees1, 4-6 for gates2. The gates are loaded into a Numby board.
The netlist files are .txt and numbered from 1 to 6. 0 is a dummy list for debugging.
Gates are numbered from 1 to 2. Also, the gates files have a dummy named gates0. The gates are comma separated files.

# settings.py

Before running the program, it is good to take a look at the settings. We wil explain the basics.
PLOT_BEST, PLOT_SCORES and PLOT_RESULTS all take a Boolean value are quite self-explanatory, they will activate a plot of the result in a separate window.

SHOW_NETLIST and SHOW_EACH_RESULT  also takes a Bool and will show in the terminal window. SHOW_EACH_PLOTSHOW_PROGRESS also a Bool and shows in a separate window.

PATH_ALGORITHM gives the user the choice to use DIJSKTRA’s algorithm. Although we will use DIJKSTRA while looping for a bather result. To make sure to find the best solutions start off with the A* algorithm. The setting takes a string.

MAX_NO_IMPROVE will kick in the moment a better solution must be found. We will loop and try to find an improvement. Only finding one is not a given thing, and to be sure to not run forever, giving a bound in with a integer is mandatory.

Heuristics for A* are ways to tweak the A*. COST_PASSING_GATE and STEP_COST_PASSING_GATE both take a integer.

To give the numpy board a 3d size use BOARD_WIDTH, BOARD_HEIGHT and BOARD_DEPTH with integer values.

The netlist and gate files are read from the data directory, in the current setup they start with “netlist” and then a number. To use your one net list make sure to do the same. To change any of the predefined files use a integer, for the net lists in range 1-6 and for the gate files in rage 1-2. Mind using the correct netlist with the correct gates file.

Finally SIGN_PATH_START and is a way of numbering the path in a Numpy board. It starts with 2 because gates are all numbered 1 (SIGN_GATE) and empty space has a 0. Changing this will probably break the program. But you can, by changing it into another integer.

# colors.py

Feel free to change it.

# helpers.py and classes.py

This files are documented [here](https://lennartjklein.github.io/pathfinder/). 
