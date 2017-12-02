from ast import literal_eval

class ListClass:
    def __init__(self, netlist):
        self.list = netlist

    # Switch the target item with item before
    def switch_back_one(self, target):
        index = self.list.index(target)

        tmp = self.list[index - 1]
        self.list[index - 1] = self.list[index]
        self.list[index] = tmp
        return self.list

    def print_list(self):
        # Print function for debugging
        print(self.list)

class List_log:
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

        self.lists_log = [self.first_list]

    # Push en pop item to lists_log
    def push_list(self, netlist):
        self.lists_log.append(netlist)

    def pop_list(self):
        poped_list = self.lists_log.pop()
        return poped_list

    def get_list(self):
        lenth = len(self.lists_log)
        print(lenth)
        return self.lists_log[lenth - 1]

def main():
    # Make log for used lists
    list_log = List_log(0)

    switch_back_tupple = (3, 5)
    counter = 0
    while switch_back_tupple != True:
        counter += 1
        # Create a netlist and calculate path
        current_list = ListClass(list_log.get_list())
        print(current_list.list)

        new_list = current_list.switch_back_one(switch_back_tupple)
        list_log.push_list(new_list)

        if counter > 5:
            print("LOG: ")
            for items in list_log.lists_log:
                print(items)
            exit()

if __name__ == '__main__':
    main()
