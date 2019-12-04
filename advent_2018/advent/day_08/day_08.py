EX = "advent/day_08/example.txt"
IN = "advent/day_08/input.txt"

def treelist(file):
    with open(file, "r") as f:
        line = f.readline()
        return [int(char) for char in line.split()]

def lunch_method(file):
    data = treelist(file)
    i = 0
    j = len(data)
    total = list()
    while i != j:
        if data[i] == 0:
            i += 1
            for x in range(i, i + data[i] + 1):
                total.append(data[x])
            i += data[i]
        else:
            i += 1
            for x in range(j - data[i] + 1, j):
                total.append(data[x])
            j = j - data[i]
    return total


# assert lunch_method(EX) == 138
    

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
