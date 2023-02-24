"""Test examples and solutions to day 03."""
from advent.day03 import main


def test_part_1_example():
    """Check the example for part 1."""
    test_result = main.Sledding("example.txt").traverse()
    assert test_result == 7


def test_part_1_actual():
    """Check the actual answer to part 1."""
    test_result = main.Sledding().traverse()
    assert test_result == 162


def test_part_2_example():
    """Check the example for part 2."""
    test_result = main.Sledding("example.txt").part2()
    assert test_result == 336


def test_part_2_actual():
    """Check the actual for part 2."""
    test_result = main.Sledding().part2()
    assert test_result == 3064612320
