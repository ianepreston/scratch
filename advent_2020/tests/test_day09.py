"""Test examples and solutions to day 08."""
from advent.day09 import main


def test_part_1_example():
    """Check the example for part 1."""
    test_result = main.part1("example.txt", 5)
    assert test_result == 127


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1()
    assert test_result == 32321523


def test_part_2_example():
    """Check the example for part 2."""
    test_result = main.part2("example.txt", 5)
    assert test_result == 62


def test_part_2_actual():
    """Check the example for part 2."""
    test_result = main.part2()
    assert test_result == 4794981
