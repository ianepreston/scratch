"""Test examples and solutions to day 17."""
from advent.day17 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 112


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1("input.txt")
    assert test_result == 276


# def test_part_2_example():
#     """Check the example for part 2."""
#     test_result = main.part2("example.txt")
#     assert test_result == 848


# def test_part_2_actual():
#     """Check the example for part 1."""
#     test_result = main.part2("input.txt")
#     assert test_result == 2136
