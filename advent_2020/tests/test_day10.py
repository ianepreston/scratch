"""Test examples and solutions to day 10."""
from advent.day10 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1("example1.txt")
    assert test_result == 35


def test_part_1_example2():
    """Check the example for part 1."""
    test_result = main.part1("example2.txt")
    assert test_result == 220


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1()
    assert test_result == 1625


def test_part_2_example1():
    """Check the example for part 2."""
    test_result = main.part2("example1.txt")
    assert test_result == 8


def test_part_2_example2():
    """Check the example for part 2."""
    test_result = main.part2("example2.txt")
    assert test_result == 19208


def test_part_2_actual():
    """Check the example for part 2."""
    test_result = main.part2()
    assert test_result == 3100448333024
