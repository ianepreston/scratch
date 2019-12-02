from collections import defaultdict


def spiral():
    x, y = 0, 0
    dx, dy = 0, -1
    while True:
        if abs(x) == abs(y) and [dx, dy] != [1, 0] or x > 0 and y == 1 - x:
            dx, dy = -dy, dx

        yield x, y
        x, y = x + dx, y + dy


def add_adjacent(x, y, coord_dict):
    adj = 0
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            adj += coord_dict[x + dx, y + dy]
    return adj


def solver(n):
    d = defaultdict(int)
    d[(0, 0)] = 1
    for x, y in spiral():
        if x == y == 0:
            val = 1
        else:
            val = add_adjacent(x, y, d)
        d[(x, y)] = val
        if val > n:
            return val


print(solver(265149))
