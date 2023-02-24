"""Test examples and solutions to day 01."""
from advent.day01 import main


def test_part_1_example():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 514579


def test_part_1_actual():
    """Check the actual answer to part 1."""
    test_result = main.part1()
    assert test_result == 1019571


def test_part_2_example():
    """Check the example for part 2."""
    test_result = main.part2("example.txt")
    assert test_result == 241861950


def test_part_2_actual():
    """Check the actual for part 2."""
    test_result = main.part2()
    assert test_result == 100655544
