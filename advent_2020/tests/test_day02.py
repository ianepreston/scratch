"""Test examples and solutions to day 02."""
from advent.day02 import main


def test_part_1_example():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 2


def test_part_1_actual():
    """Check the actual answer to part 1."""
    test_result = main.part1()
    assert test_result == 416


def test_part_2_example():
    """Check the example for part 2."""
    test_result = main.part2("example.txt")
    assert test_result == 1


def test_part_2_actual():
    """Check the actual for part 2."""
    test_result = main.part2()
    assert test_result == 688
