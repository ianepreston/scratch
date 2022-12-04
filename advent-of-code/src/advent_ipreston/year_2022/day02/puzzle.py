"""Rock paper scissors."""

from typing import Dict

from advent_ipreston.helpers import inputs_generator


def match_part1(codes: str) -> Dict[str, int]:
    """Run a single match."""
    elf_code, my_code = codes.split()
    shape_points = {
        "X": 1,
        "Y": 2,
        "Z": 3,
    }
    shape_point = shape_points[my_code]
    # Rock Paper, Paper Scissors, Scissors Rock
    win_conditions = [
        "A Y",
        "B Z",
        "C X",
    ]
    draw_conditions = [
        "A X",
        "B Y",
        "C Z",
    ]
    if codes in draw_conditions:
        match_point = 3
    elif codes in win_conditions:
        match_point = 6
    else:
        match_point = 0
    return {
        "shape": shape_point,
        "match": match_point,
        "total": shape_point + match_point,
    }


def part1(infile: str) -> int:
    """Solve part 1."""
    return sum(match_part1(line)["total"] for line in inputs_generator(infile))


def match_part2(codes: str) -> int:
    """Complete a match in part 2."""
    shape_points = {
        "A": 1,  # Rock
        "B": 2,  # Paper
        "C": 3,  # Scissors
    }
    match_points = {"X": 0, "Y": 3, "Z": 6}
    elf_shape, match_code = codes.split()
    responses = {
        "A X": "C",
        "A Y": "A",
        "A Z": "B",
        "B X": "A",
        "B Y": "B",
        "B Z": "C",
        "C X": "B",
        "C Y": "C",
        "C Z": "A",
    }
    return shape_points[responses[codes]] + match_points[match_code]


def part2(infile: str) -> int:
    """Solve part 2."""
    return sum(match_part2(line) for line in inputs_generator(infile))
