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


def build_tower(file):
    tower = dict()
    for name, weight, children in read_lines(file):
        if name in tower:
            tower[name].weight = weight
        else:
            tower[name] = Prog(name, weight)
        for child in children:
            if child not in tower:
                tower[child] = Prog(child, None)
            tower[child].parent = name
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
