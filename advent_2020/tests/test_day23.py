"""Test examples and solutions to day 23."""
from advent.day23 import main


def test_part_1_example():
    """Check the example for part 1."""
    test_result = main.part1(main.EG_CUPS)
    assert test_result == "67384529"


def test_part_1_actual():
    """Test the actual answer for part 1."""
    test_result = main.part1(main.IN_CUPS)
    assert test_result == "68245739"


# def test_part_2_example():
#     """Check the example for part 2."""
#     test_result = main.part2(main.EG_CUPS)
#     assert test_result == 149245887792


# def test_part_2_actual():
#     """Test the actual answer for part 2."""
#     test_result = main.part2(main.IN_CUPS)
#     assert test_result == 219634632000
