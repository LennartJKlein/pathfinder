#___________________________________________________________________________
# board.py                                                                  |
#                                                                           |
# Authors:                                                                  |
# - Jurre Brandsen                                                          |
#                                                                           |
# Credit/copyright:                                                         |
# - Westly White, stackoverflow, Jan 12 2016                                |
#                                                                           |
# Generates a grid with variable X- and Y-axisis.                           |
# Option to turn labels on and off                                          |
# Makes gates based on input from pathfinder.py                             |
#___________________________________________________________________________|

class Cell:
    """
    :param x: x-axis location
    :param y: y-axis location
    """
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.visual = "."

    def __str__(self):
        return self.visual

class Board:

    def __init__(self, x, y, show_labels=True):
        ''''
        :param x: How many columns the board uses
        :param y: How many rows the board uses
        :param show_labels: Display labels to the player
        '''

        self.x = x
        self.y = y
        self.show_labels = show_labels
        self.board = {}

        self.generate_board()

    def generate_board(self):
        for y in range(0, self.y):

            # Add the key X to the board dictionary
            self.board[y] = []   

            for x in range(0, self.x):
                # Make a cell @ the current x, y and add it to the board
                cell = Cell(x, y)
                self.board[y].append(cell)

    def show_board(self):

        for key, cells in self.board.iteritems():

            # Add the X Labels
            if self.show_labels:
                if key == 0:
                    x_label = []
                    for cell in self.board[key]:
                        x_label.append(str(cell.x + 1))
                    print " ".join(x_label)

            row = []
            for cell in cells:
                row.append(str(cell))

            # Add the Y labels
            if self.show_labels:
                row.append(str(cell.y + 1))

            print " ".join(row)

    def set_gate(self, name, x, y):
        self.board[x][y].visual = name