def read_inputs(filename):
    with open(filename, "r") as f:
        return [int(x) for x in f.readlines()]


def part1():
    freq = 0
    for mod in read_inputs("advent/day_01/input.txt"):
        freq += mod
    return freq

print(part1())

def part2():
    mods = read_inputs("advent/day_01/input.txt")
    freqs = set()
    freq = 0
    while True:
        for mod in mods:
            freqs.add(freq)
            new_freq = freq + mod
            if new_freq in freqs:
                return new_freq
            freq = new_freq

print(part2())