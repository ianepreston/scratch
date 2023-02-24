"""Test examples and solutions to day 18."""
import pytest

from advent.day18 import main


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("1 + 2 * 3 + 4 * 5 + 6", 71),
        ("1 + (2 * 3) + (4 * (5 + 6))", 51),
        ("2 * 3 + (4 * 5)", 26),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
    ],
)
def test_part_1_examples(test_input, expected):
    """Check the example for part 1."""
    test_result = int(main.parse(test_input))
    assert test_result == expected


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1("input.txt")
    assert test_result == 2743012121210


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("1 + 2 * 3 + 4 * 5 + 6", 231),
        ("1 + (2 * 3) + (4 * (5 + 6))", 51),
        ("2 * 3 + (4 * 5)", 46),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
    ],
)
def test_part_2_examples(test_input, expected):
    """Check the example for part 2."""
    test_result = int(main.parse2(test_input))
    assert test_result == expected


def test_part_2_actual():
    """Check the example for part 1."""
    test_result = main.part2("input.txt")
    assert test_result == 65658760783597
