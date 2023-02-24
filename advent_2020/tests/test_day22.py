"""Test examples and solutions to day 22."""
from advent.day22 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 306


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1("input.txt")
    assert test_result == 32629


def test_part_2_example():
    """Check the example for part 2."""
    test_result = main.part2("example.txt")
    assert test_result == 291


def test_part_2_example2():
    """Check we don't have an infinite loop."""
    test_result = main.part2("example2.txt")
    # Just want to ensure it finishes
    assert test_result


def test_part_2_actual():
    """Check the example for part 1."""
    test_result = main.part2("input.txt")
    assert test_result == 32519
