"""Test examples and solutions to day 24."""
from advent.day24 import main


def test_part_1_example():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 10


def test_part_1_actual():
    """Test the actual answer for part 1."""
    test_result = main.part1("input.txt")
    assert test_result == 488


# def test_part_2_example():
#     """Check the example for part 2."""
#     test_result = main.part2("example.txt")
#     assert test_result == 2208


# def test_part_2_actual():
#     """Test the actual answer for part 2."""
#     test_result = main.part2("input.txt")
#     assert test_result == 4118
