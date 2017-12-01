"""
core.py
Authors: - Jurre Brandsen
         - Lennart Klein
         - Thomas de Lange

Pathfinder will find the most efficient path between two gates on a board.
"""

import settings

import colors as CLR
import numpy as np
import matplotlib.pyplot as plt

from classes import Board
from classes import Experiment
from classes import Netlist
from classes import Gate

def main():
    '''
    Initialise and draw a grid called Board
    Read gate locations from gates file
    '''
    
    # Set and show chosen settings
    np.set_printoptions(threshold=np.nan)

    print("Using netlist #" + str(settings.FILE_NETLIST))
    print("Using gates file #" + str(settings.FILE_GATES))
    print("")

    # Initiate a new experiment
    experiment = Experiment(settings.ITERATIONS, settings.SHOW_EACH_RESULT, settings.SHOW_EACH_DATA, settings.SHOW_EACH_PLOT);

    # Plot experiment information
    if settings.PLOT_SCORE:
        experiment.plot_score()

    # netlist_log = Netlist_log(settings.FILE_NETLIST)

if __name__ == '__main__':
    main()
