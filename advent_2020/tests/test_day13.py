"""Test examples and solutions to day 13."""
from advent.day13 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 295


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1()
    assert test_result == 6559


def test_part_2_example1():
    """Check the example for part 2."""
    test_result = main.part2("example.txt")
    assert test_result == 1068781


def test_part_2_actual():
    """Check the example for part 2."""
    test_result = main.part2()
    assert test_result == 626670513163231
