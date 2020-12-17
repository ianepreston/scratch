"""Test examples and solutions to day 16."""
from advent.day16 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 71


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1("input.txt")
    assert test_result == 22057


# def test_part_2_example1():
#     """Check the example for part 1."""
#     test_result = main.part2("example.txt")
#     assert test_result == 175594


def test_part_2_actual():
    """Check the example for part 1."""
    test_result = main.part2("input.txt")
    assert test_result == 1093427331937
