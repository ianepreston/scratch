"""Advent of code 2021 day 10 puzzle."""
from pathlib import Path
from statistics import median
from typing import Generator, List

BOPEN = "<{(["
BCLOSE = ">})]"
BPAIRS = tuple(zip(BOPEN, BCLOSE))


def parse_line(line: str) -> List[str]:
    """Check bracket matching.

    Returns a list of either open brackets
    that weren't closed, the first close bracket that
    doesn't correspond to an open one, or an empty list
    if everything is cool.
    """
    open_stack = list()
    for char in line:
        if char in BOPEN:
            open_stack.append(char)
        elif char in BCLOSE:
            if not open_stack:
                return [char]
            else:
                bopen = open_stack.pop()
                if (bopen, char) not in BPAIRS:
                    return [char]
        else:
            raise ValueError(f"Unexpected character: {char}")
    return open_stack


def parsed_line_generator(infile: str) -> Generator[List[str], None, None]:
    inpath = Path(__file__).resolve().parent / infile
    with open(inpath, "r") as f:
        for line in f.readlines():
            yield parse_line(line.strip())


def illegal_points(parsed_line: List[str]) -> int:
    """How many points for illegal characters in this line?"""
    if len(parsed_line) == 0:
        return 0
    checkchar = parsed_line[0]
    if checkchar in BCLOSE:
        point_dict = {
            ")": 3,
            "]": 57,
            "}": 1197,
            ">": 25137,
        }
        return point_dict[checkchar]
    else:
        return 0


def incomplete_line_generator(infile: str) -> Generator[List[str], None, None]:
    """Just show the incomplete lines for part 2."""
    for line in parsed_line_generator(infile):
        if line:
            if line[0] in BOPEN:
                yield line


def complete_brackets(parsed_line: List[str]) -> List[str]:
    """Close those pesky open brackets."""
    pair_dict = {bopen: bclose for bopen, bclose in BPAIRS}
    parsed_line.reverse()
    return [pair_dict[bopen] for bopen in parsed_line]


def score_completion(completed_brackets: List[str]) -> int:
    """Do the weird bracket closing scoring."""
    point_map = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    total_score = 0
    for bracket in completed_brackets:
        total_score = total_score * 5
        total_score += point_map[bracket]
    return total_score


def part1(infile: str) -> int:
    """Solve part 1."""
    return sum(illegal_points(pline) for pline in parsed_line_generator(infile))


def part2(infile: str) -> int:
    """Solve part 2."""
    return int(
        median(
            score_completion(complete_brackets(line))
            for line in incomplete_line_generator(infile)
        )
    )


if __name__ == "__main__":
    eg1 = part1("example.txt")
    eg1a = 26397
    if eg1 != eg1a:
        raise ValueError(f"Expected {eg1a}, got {eg1}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
    eg2 = part2("example.txt")
    eg2a = 288957
    if eg2 != eg2a:
        raise ValueError(f"Expected {eg2a}, got {eg2}")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")
