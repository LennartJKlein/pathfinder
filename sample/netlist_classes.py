class Netlist:
    """
    Netlist are tuples reperesenting the contecion between two gates. Al conections
    must be made to solve the case.

    :param: number:     number of the netlist used
    """

    def __init__(self, netlist):
        self.list = netlist

    # Switch the target item with item before
    def switch_back_one(self, target):
        index = self.list.index(target)

        tmp = self.list[index - 1]
        self.list[index - 1] = self.list[index]
        self.list[index] = tmp
        return self.list

    def switch_back_front(self, target):
        index = self.list.index(target)

        tmp = self.list[0]
        self.list[0] = self.list[index]
        self.list[index] = tmp
        return self.list

    def execute_connections(self, board):
        path_number = settings.SIGN_PATH_START
        amount_fail = 0

        for connection in self.list:
            # Get the coordinates of the two gates in this connection
            a = connection[0]
            b = connection[1]
            progression_counter = 1

            # print("")
            # print(str(connection[0]) + "  ->  "  + str(connection[1]))

            coordGateA = np.argwhere(board.gatesNumbers == a + 1)
            coordGateB = np.argwhere(board.gatesNumbers == b + 1)

            # Create a new path object
            new_path = Path(coordGateA[0], coordGateB[0], path_number, "grey")

            # Add this path to the board object
            board.paths.append(new_path)

            # Calculate the route for this path
            result = new_path.calculate_DIJKSTRA(board)

            # Count the score
            if result == False:
                amount_fail += 1

                i = self.list.index(connection)
                false_result = connection
                print("false_result in classes:")
                print(false_result)
                return false_result

            # Set a new path_number for the next path
            path_number += 1
            progression_counter += 1

            if progression_counter == len(self.list):
                return True

        print(CLR.YELLOW + "Paths not calculated: " + str(amount_fail) + " / " + str(path_number) + CLR.DEFAULT)
        print(CLR.YELLOW + str(round(amount_fail / path_number * 100, 2)) + "%" + CLR.DEFAULT)
        print("")

    def print_list(self):
        # Print function for debugging
        print(self.list)

class Netlist_log:
    """
    :param fisrt_list: first list to be saved.
    Make a stack hostory of the used netlists
    """
    def __init__(self, number):
        # Make file name used.
        self.filename = "data/netlist"
        self.filename += str(number)
        self.filename += ".txt"

        # Open netlist and read with literal evaluation.
        with open(self.filename) as f:
            self.first_list = f.read()

        self.first_list = literal_eval(self.first_list)

        print("Using netlist #" + str(number))

        self.lists_log = []
        self.lists_log.extend([self.first_list])

    # Push en pop item to lists_log
    def push_list(self, netlist):
        # self.lists_log.insert(0, netlist)
        self.lists_log.extend(netlist)

    def pop_list(self):
        poped_list = self.lists_log.pop(0)
        return poped_list

    def return_list(self):
        return self.lists_log[-1][:]

    def look_for_loop(self, input_list):
        amount = 0
        for lists in self.lists_log:
            if amount > 2:
                return True

            if lists == input_list:
                amount += 1
