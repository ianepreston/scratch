def gridsize(number):
    rowh = 1
    while rowh ** 2 < number:
        rowh += 2
    return rowh


assert gridsize(1) == 1
assert gridsize(8) == 3
assert gridsize(9) == 3
assert gridsize(25) == 5


def memgrid(number):
    size = gridsize(number)
    corner = size ** 2
    while (corner - size + 1) > number:
        corner = corner - size + 1
    mid = corner - ((size - 1) / 2)
    tot = ((size - 1) / 2) + abs(mid - number)
    return int(tot)


assert memgrid(1) == 0
assert memgrid(12) == 3
assert memgrid(23) == 2
assert memgrid(1024) == 31

print(memgrid(265149))
