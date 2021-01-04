"""Test functionality in the linear algebra library."""
from dsfs import linalg


def test_add() -> None:
    """Test adding two vectors."""
    assert linalg.add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]


def test_subtract() -> None:
    """Test adding two vectors."""
    assert linalg.subtract([5, 7, 9], [4, 5, 6]) == [1, 2, 3]
