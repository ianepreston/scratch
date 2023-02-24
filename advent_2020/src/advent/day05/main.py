"""Day 05 of the advent of code challenge."""
from __future__ import annotations

from pathlib import Path
from typing import Generator, NamedTuple, Set, Tuple


class BoardingPass(NamedTuple):
    """Boarding pass container object."""

    row: int
    column: int

    @property
    def seat_id(self: BoardingPass) -> int:
        """(row * 8) + column.

        Returns
        -------
        int:
            the seat ID
        """
        return (self.row * 8) + self.column

    @staticmethod
    def binary_partition(
        chars: str, low_char: str, high_char: str, upper_bound: int
    ) -> int:
        """Perform binary partition on a row or column string.

        Parameters
        ----------
        chars: str
            The input sequence, e.g. "BBFBFFB"
        low_char: str
            The character representing the low end of the range e.g. F
        high_char: str
            The character representing the high end of the range e.g. B
        upper_bound: int
            The 0 indexed upper bound of the range to partition, e.g. 127

        Returns
        -------
        int
            The row or column associated with the sequence
        """
        low_index: int = 0
        high_index: int = upper_bound
        for char in chars:
            if char not in (low_char, high_char):
                raise ValueError(f"{char} must be {low_char} or {high_char}")
            mid_index: int = ((high_index - low_index) // 2) + low_index
            if char == low_char:
                high_index = mid_index
            else:
                low_index = mid_index + 1
        if high_index != low_index:
            raise ValueError("high and low don't match, something broke")
        return low_index

    @staticmethod
    def parse(line: str) -> BoardingPass:
        """Binary partition a string to get a pass.

        Parameters
        ----------
        line: str
            input line, e.g. FBFBBFFRLR

        Returns
        -------
        BoardingPass
            Row, column and id of the string
        """
        if len(line) != 10:
            raise ValueError("input line must be 10 characters")
        row_chars: str = line[:7]
        col_chars: str = line[7:]
        row_val: int = BoardingPass.binary_partition(row_chars, "F", "B", 127)
        col_val: int = BoardingPass.binary_partition(col_chars, "L", "R", 7)
        return BoardingPass(row_val, col_val)


def read_inputs(filename: str = "input.txt") -> Generator[BoardingPass, None, None]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Yields
    ------
    BoardingPass
        The next fully parsed BoardingPass
    """
    here: Path = Path(__file__).resolve().parent
    in_path: Path = here / filename
    with open(in_path, "r") as f:
        for line in f.readlines():
            yield BoardingPass.parse(line.rstrip())


def part1() -> int:
    """Return the highest seat ID on the list.

    Returns
    -------
    int:
        The highest seat ID
    """
    return max((board_pass.seat_id for board_pass in read_inputs()))


def part2() -> int:
    """Find your seat ID.

    Returns
    -------
    int:
        Your seat ID
    """
    seat_ids: Set[int] = set(board_pass.seat_id for board_pass in read_inputs())
    min_id: int = min(seat_ids)
    max_id: int = max(seat_ids)
    missing_seats: Tuple[int, ...] = tuple(
        id for id in range(min_id, max_id) if id not in seat_ids
    )
    if len(missing_seats) != 1:
        raise ValueError(f"Found {len(missing_seats)} seats, should have exactly 1")
    return missing_seats[0]
