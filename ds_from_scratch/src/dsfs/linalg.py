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


def vector_sum(vectors: List[Vector]) -> Vector:
    """Sum a list of vectors.

    Args:
        vectors: The list of vectors

    Returns:
        The combined vector

    Raises:
        ValueError: If any vectors are different lengths or no vectors are supplied
    """
    if not vectors:
        raise ValueError("No vectors provided")
    num_elements: int = len(vectors[0])
    if not all(len(v) == num_elements for v in vectors):
        raise ValueError("All vectors must be same size")
    # The i-th element of the result si the sum of every vector[i]
    return [sum(vector[i] for vector in vectors) for i in range(num_elements)]
