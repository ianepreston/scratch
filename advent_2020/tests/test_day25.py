"""Test examples and solutions to day 25."""
from advent.day25 import main


def test_part_1_example():
    """Check the example for part 1."""
    test_result = main.part1(5764801, 17807724)
    assert test_result == 14897079


def test_part_1_actual():
    """Test the actual answer for part 1."""
    test_result = main.part1(12578151, 5051300)
    assert test_result == 296776


# def test_part_2_example():
#     """Check the example for part 2."""
#     test_result = main.part2("example.txt")
#     assert test_result == 2208


# def test_part_2_actual():
#     """Test the actual answer for part 2."""
#     test_result = main.part2("input.txt")
#     assert test_result == 4118
