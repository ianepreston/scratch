"""Test examples and solutions to day 05."""
import pytest

from advent.day05 import main


@pytest.mark.parametrize(
    "test_input,boarding_pass",
    [
        ("BFFFBBFRRR", (70, 7, 567)),
        ("FFFBBBFRRR", (14, 7, 119)),
        ("BBFFBBFRLL", (102, 4, 820)),
    ],
)
def test_parsing_passes(test_input, boarding_pass):
    """Test correct parsing of inputs."""
    row, col, seat_id = boarding_pass
    parsed_pass = main.BoardingPass.parse(test_input)
    assert parsed_pass.row == row
    assert parsed_pass.column == col
    assert parsed_pass.seat_id == seat_id


def test_part_1_actual():
    """Check the actual answer to part 1."""
    test_result = main.part1()
    assert test_result == 933


def test_part_2_actual():
    """Check the actual answer to part 2."""
    test_result = main.part2()
    assert test_result == 711
