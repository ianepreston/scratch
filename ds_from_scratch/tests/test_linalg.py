"""Test functionality in the linear algebra library."""
import math

from dsfs import linalg


def test_add() -> None:
    """Test adding two vectors."""
    assert linalg.add([1, 2, 3], [4, 5, 6]) == [5, 7, 9]


def test_subtract() -> None:
    """Test adding two vectors."""
    assert linalg.subtract([5, 7, 9], [4, 5, 6]) == [1, 2, 3]


def test_vector_sum() -> None:
    """Test adding a list of vectors."""
    assert linalg.vector_sum([[1, 2], [3, 4], [5, 6], [7, 8]]) == [16, 20]


def test_scalar_multiply() -> None:
    """Test scalar multiplication."""
    assert linalg.scalar_multiply(2, [1, 2, 3]) == [2, 4, 6]


def test_vector_mean() -> None:
    """Test vector mean."""
    assert linalg.vector_mean([[1, 2], [3, 4], [5, 6]]) == [3, 4]


def test_dot() -> None:
    """Test dot product."""
    assert linalg.dot([1, 2, 3], [4, 5, 6]) == 32


def test_sum_of_squares() -> None:
    """Test sum of squares."""
    assert linalg.sum_of_squares([1, 2, 3]) == 14


def test_magnitude() -> None:
    """Test magnitude."""
    assert linalg.magnitude([3, 4]) == 5


def test_squared_distance() -> None:
    """Test squared distance."""
    assert linalg.squared_distance([1, 5], [5, 1]) == 32


def test_distance() -> None:
    """Test distance."""
    # c^2 == a^2 + b^2
    assert linalg.distance([0, 0], [3, 3]) == math.sqrt(18)
