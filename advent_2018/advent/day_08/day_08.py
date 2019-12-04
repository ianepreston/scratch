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
        self.n_meta = None
        self.children = None
        self.meta = list()

    def receive_input(self, num: int):
        if self.children is None:
            self.children = [Node() for _ in range(num)]
            return True
        elif self.n_meta is None:
            self.n_meta = num
            return True
        else:
            for child in self.children:
                if child.receive_input(num):
                    return True
            if len(self.meta) < self.n_meta:
                self.meta.append(num)
                return True
        return False


def traverse(node):
    all_nodes = []
    queue = [node]
    while queue:
        currnode = queue.pop(0)
        all_nodes.append(currnode)
        if currnode.children:
            queue.extend(currnode.children)
    return all_nodes


def part1(filename):
    inputs = treelist(filename)
    root_node = Node()
    for num in inputs:
        root_node.receive_input(num)

    all_nodes = traverse(root_node)
    total = sum(meta for node in all_nodes for meta in node.meta)
    return total


assert part1(EX) == 138
print(part1(IN))
