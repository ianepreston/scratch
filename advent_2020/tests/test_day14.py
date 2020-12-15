"""Test examples and solutions to day 14."""
from advent.day14 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 165


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1()
    assert test_result == 13105044880745


def test_part_2_example1():
    """Check the example for part 2."""
    test_result = main.part2("example2.txt")
    assert test_result == 208


def test_part_2_actual():
    """Check the example for part 2."""
    test_result = main.part2()
    assert test_result == 3505392154485
