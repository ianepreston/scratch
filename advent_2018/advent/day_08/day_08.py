def treelist(file):
    with open(file, "r") as f:
        line = f.readline()
        return [int(char) for char in line.split()]


class Node:
    def __init__(self):
        self.n_children = None
        self.n_meta = None
        self.children = list()
        self.meta = list()
    
    def get_input(self, num: int):
        if self.n_children is None:
            self.n_children = num
        elif self.n_meta is None:
            self.n_meta = num
        elif 
