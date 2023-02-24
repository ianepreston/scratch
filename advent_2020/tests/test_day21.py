"""Test examples and solutions to day 17."""
from advent.day21 import main


def test_part_1_example1():
    """Check the example for part 1."""
    test_result = main.part1("example.txt")
    assert test_result == 5


def test_part_1_actual():
    """Check the example for part 1."""
    test_result = main.part1("input.txt")
    assert test_result == 1679


def test_part_2_example():
    """Check the example for part 2."""
    test_result = main.part2("example.txt")
    assert test_result == "mxmxvkd,sqjhc,fvjkl"


def test_part_2_actual():
    """Check the example for part 1."""
    test_result = main.part2("input.txt")
    assert test_result == "lmxt,rggkbpj,mxf,gpxmf,nmtzlj,dlkxsxg,fvqg,dxzq"
