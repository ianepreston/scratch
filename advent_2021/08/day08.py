"""Advent of code 2021 day 8 puzzle."""
from pathlib import Path
from typing import Dict, Generator, List, Set, NamedTuple


class InputLine(NamedTuple):
    patterns: List[Set[str]]
    output: List[Set[str]]


def _seq_to_set(seq: str) -> Set[str]:
    """Turn a string of characters into a set of them."""
    return {x for x in seq}


def parse_line(line: str) -> InputLine:
    """Turn a puzzle line into a data structure."""
    raw_pattern, raw_output = line.split(" | ")
    patterns = [_seq_to_set(x) for x in raw_pattern.split(" ")]
    output = [_seq_to_set(x) for x in raw_output.split(" ")]
    return InputLine(patterns, output)


def puzzle_gen(infile: str) -> Generator[InputLine, None, None]:
    """Yield puzzle inputs from the file."""
    inpath = Path(__file__).resolve().parent / infile
    with open(inpath, "r") as f:
        for line in f.readlines():
            yield parse_line(line.strip())


def part1(infile: str) -> int:
    """Solve part 1."""
    counter = 0
    lens = (2, 3, 4, 7)
    for puzzle in puzzle_gen(infile):
        outputs = puzzle.output
        matches = sum(1 for x in outputs if len(x) in lens)
        counter += matches
    return counter


def sort_set(inset: Set[str]) -> str:
    """Can't use sets as dictionary keys."""
    return "".join(sorted(list(inset)))


def map_patterns(patterns: List[Set[str]]) -> Dict[Set[str], str]:
    """Match patterns to string representations of numbers.

    Might as well keep them as strings since I need to concatenate
    outputs before parsing back to integers.
    """
    letters = dict()
    numbers = dict()

    # map in the easy ones we did above
    numbers[1] = [x for x in patterns if len(x) == 2].pop()
    numbers[4] = [x for x in patterns if len(x) == 4].pop()
    numbers[7] = [x for x in patterns if len(x) == 3].pop()
    numbers[8] = [x for x in patterns if len(x) == 7].pop()

    # 1 and 7 only differ by the presence of a
    letters["a"] = list(numbers[7] - numbers[1]).pop()
    # 4 has b and d along with the parts of 1
    bd = numbers[4] - numbers[1]
    # All the other length 6 numbers have b and d in them
    numbers[0] = [x for x in patterns if (len(x) == 6) and len(x & bd) == 1].pop()
    # Zero only has b in it, not d
    letters["b"] = list(numbers[0] & bd).pop()
    # So d must be the element that's not in 0
    letters["d"] = list(bd - set(letters["b"])).pop()
    # Six and nine are the other 6 segment numbers
    sixnine = [x for x in patterns if (len(x) == 6) and (x != numbers[0])]
    # Taking the segments of 6 or 9 from the segments of 0 leaves c and e
    ce = (numbers[0] - sixnine[0]) | (numbers[0] - sixnine[1])
    # 5 doesn't have c or e in it so it will have the same length if you subtract them
    numbers[5] = [
        x for x in patterns if (len(x) == 5) and (len(x - ce) == len(x))
    ].pop()
    # c is the only segment in 4 that's not also in 5
    letters["c"] = list(numbers[4] - numbers[5]).pop()
    letters["e"] = list(ce - set(letters["c"])).pop()
    # The only segment in 4 we haven't identified is f so this must be it
    letters["f"] = list(
        numbers[4] - set((letters["b"], letters["c"], letters["d"]))
    ).pop()
    # Can do g by process of elimination
    g = [x for x in "abcdefg" if x not in letters.values()].pop()
    letters["g"] = g
    # So then I can just build everything up from all the known letters
    numbers[2] = set((letters[x] for x in "acdeg"))
    numbers[3] = set((letters[x] for x in "acdfg"))
    numbers[6] = set((letters[x] for x in "abdefg"))
    numbers[9] = set((letters[x] for x in "abcdfg"))
    # Now just reverse it so you can do lookups
    return {sort_set(val): str(key) for key, val in numbers.items()}


def solve_line(line: InputLine) -> int:
    """Take a puzzle line and make a number out of it."""
    mapper = map_patterns(line.patterns)
    numstring = "".join(mapper[sort_set(num)] for num in line.output)
    return int(numstring)


def part2(infile: str) -> int:
    return sum(solve_line(puzzle) for puzzle in puzzle_gen(infile))


if __name__ == "__main__":
    eg1 = part1("example.txt")
    eg1a = 26
    if eg1 != eg1a:
        raise ValueError(f"Expected {eg1a}, got {eg1}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")

    eg2 = part2("example.txt")
    eg2a = 61229
    if eg2 != eg2a:
        raise ValueError(f"Expected {eg2a}, got {eg2}")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")
