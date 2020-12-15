"""Test examples and solutions to day 15."""
from advent.day15 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1([0, 3, 6])
    assert test_result == 436


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1([9, 19, 1, 6, 0, 5, 4])
    assert test_result == 1522


# def test_part_2_example1():
#     """Check the example for part 1."""
#     test_result = main.part2([0, 3, 6])
#     assert test_result == 175594


# def test_part_2_actual():
#     """Check the example for part 1."""
#     test_result = main.part2([9, 19, 1, 6, 0, 5, 4])
#     assert test_result == 18234
