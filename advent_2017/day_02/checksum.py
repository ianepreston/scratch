def rowsolver(rowfunc, infile="input.txt"):
    checksum = 0
    with open(infile, "r") as f:
        for line in f.readlines():
            row = [int(num) for num in line.split()]
            checksum += rowfunc(row)
    return checksum


def part1(row):
    return max(row) - min(row)


assert rowsolver(rowfunc=part1, infile="example.txt") == 18
print(rowsolver(part1))


def part2(row):
    row.sort(reverse=True)
    for i in range(len(row)):
        j = i + 1
        for comp in row[j:]:
            if row[i] % comp == 0:
                return row[i] / comp


assert rowsolver(rowfunc=part2, infile="example2.txt") == 9
print("not the cleanest code but seems to work")
print(rowsolver(rowfunc=part2))
