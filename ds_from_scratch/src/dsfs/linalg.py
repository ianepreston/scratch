"""Linear algebra from scratch."""
from typing import List
from typing import Union

Numeric = Union[int, float, complex]
Vector = List[Numeric]


def add(v: Vector, w: Vector) -> Vector:
    """Add two vectors.

    Args:
        v: The first vector
        w: The second vector

    Returns:
        The added vectors

    Raises:
        ValueError: If the vectors are of different lengths

    Example:
        >>> from dsfs.linalg import add
        >>> add([1, 2, 3], [4, 5, 6])
        [5, 7, 9]
    """
    if len(v) != len(w):
        raise ValueError("Vectors must be the same length")
    return [v_i + w_i for v_i, w_i in zip(v, w)]


def subtract(v: Vector, w: Vector) -> Vector:
    """Subtract two vectors.

    Args:
        v: The first vector
        w: The second vector

    Returns:
        The subtracted vectors

    Raises:
        ValueError: If the vectors are of different lengths

    Example:
        >>> from dsfs.linalg import subtract
        >>> subtract([5, 7, 9], [4, 5, 6])
        [1, 2, 3]
    """
    if len(v) != len(w):
        raise ValueError("Vectors must be the same length")
    return [v_i - w_i for v_i, w_i in zip(v, w)]
