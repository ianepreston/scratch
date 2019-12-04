with open("day_05/input.txt", "r") as f:
    IN = [int(line) for line in f.readlines()]

EX = [0, 3, 0, 1, -3]


def part1(in_list):
    size = len(in_list)
    i = 0
    steps = 0
    while True:
        next_step = i + in_list[i]
        in_list[i] += 1
        if size <= next_step or next_step < 0:
            return steps + 1
        steps += 1
        i = next_step


assert (part1(EX)) == 5
print(part1(IN))

# Uggghhh I was changing the actual list like a dummy
with open("day_05/input.txt", "r") as f:
    IN = [int(line) for line in f.readlines()]

EX = [0, 3, 0, 1, -3]


def part2(in_list):
    """basically a rewrite of part 1, for shame"""
    size = len(in_list)
    i = 0
    steps = 0
    while True:
        next_step = i + in_list[i]
        if in_list[i] >= 3:
            in_list[i] -= 1
        else:
            in_list[i] += 1
        if size <= next_step or next_step < 0:
            return steps + 1
        steps += 1
        i = next_step


assert part2(EX) == 10
print(part2(IN))
