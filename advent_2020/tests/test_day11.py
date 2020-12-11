"""Test examples and solutions to day 11."""
from advent.day11 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 37


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1()
    assert test_result == 2476


def test_part_2_example1():
    """Check the example for part 2."""
    test_result = main.part2("example.txt")
    assert test_result == 26


def test_part_2_actual():
    """Check the example for part 2."""
    test_result = main.part2()
    assert test_result == 2257
