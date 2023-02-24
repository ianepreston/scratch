from collections import Counter
import re

EX = "ex.txt"
IN = "in.txt"


def parse_line(line):
    rgx = r"([a-z]+) \((\d+)\)( -> )?(.*)"
    name, weight, _, children = re.match(rgx, line).groups()
    children = tuple(child for child in children.split(", ") if child)
    return name, weight, children


def read_lines(file):
    with open(file, "r") as f:
        return [parse_line(line) for line in f.readlines()]


class Prog:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.parent = None
        self.children = []
    
    def cumulative_weight(self):
        if not self.children:
            return self.weight
        else:
            return self.weight + sum(child.cumulative_weight() for child in self.children)


def build_tower(file):
    tower = dict()
    for name, weight, children in read_lines(file):
        if name in tower:
            tower[name].weight = int(weight)
        else:
            tower[name] = Prog(name, weight)
        for child in children:
            if child not in tower:
                tower[child] = Prog(child, None)
            tower[child].parent = tower[name]
            tower[name].children.append(tower[child])
    return tower


def validate_tower(file):
    tower = build_tower(file)
    parentless = []
    for prog in tower.values():
        assert prog.weight is not None
        if prog.parent is None:
            parentless.append(prog)
    assert len(parentless) == 1


validate_tower(EX)


def bottom_prog(file):
    tower = build_tower(file)
    bottom = []
    for prog in tower.values():
        if prog.parent is None:
            bottom.append(prog)
    assert len(bottom) == 1
    return bottom[0].name


assert bottom_prog(EX) == "tknk"
print(bottom_prog(IN))

def imbalanced(file):
    tower = build_tower(file)
    parents = set(prog.parent for prog in tower.values() if len(prog.children) == 0)
    while len(parents) > 0:
        for parent in parents:
            if len(set(child.cumulative_weight() for child in parent.children)) != 1: 
                weights = Counter(child.cumulative_weight() for child in parent.children)
                off_weight = [k for k, v in weights.items() if v == 1]
                assert len(off_weight) == 1
                off_weight = off_weight[0]
                good_weight = set(k for k, v in weights.items() if v != 1)
                assert len(good_weight) == 1
                return good_weight
        parents = set(parent.parent for parent in parents)
    return "oh shit"

print(imbalanced(EX))