"""Test examples and solutions to day 19."""
from advent.day19 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 2


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1("input.txt")
    assert test_result == 226


def test_part_2_example_1():
    """Check the example for part 2."""
    test_result = main.part1("example2.txt")
    assert test_result == 3


def test_part_2_example_2():
    """Check the example for part 2."""
    test_result = main.part2("example2.txt")
    assert test_result == 12


def test_part_2_actual():
    """Check the example for part 1."""
    test_result = main.part2("input.txt")
    assert test_result == 355
