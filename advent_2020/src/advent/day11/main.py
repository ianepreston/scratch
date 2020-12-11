"""Day 11 of the advent of code challenge."""
from __future__ import annotations

import copy
from pathlib import Path
from typing import Callable, Counter, Dict, List, Tuple


class Lobby:
    """Waiting area for the ferry."""

    def __init__(self, state: List[List[str]]) -> None:
        """Set the initial state of the waiting area.

        Parameters
        ----------
        state: List[List[str]]
            the layout of the lobby
        """
        self.state: List[List[str]] = state
        self.rows = len(self.state)
        self.cols = len(self.state[0])

    def _adjacent_values(self, row: int, col: int) -> Counter[str]:
        """Count how many of each type of tile are adjacent to a tile.

        Parameters
        ----------
        row: int
            row coordinate for the value
        col: int
            col coordinate for the value

        Returns
        -------
        Counter
            How many of each type of tile is in the adjacent tiles
        """
        min_row: int = max(0, row - 1)
        max_row: int = min(row + 1, len(self.state) - 1)
        min_col: int = max(0, col - 1)
        max_col: int = min(col + 1, len(self.state[0]) - 1)
        adj_values: Counter[str] = Counter()
        for adj_row in range(min_row, max_row + 1):
            for adj_col in range(min_col, max_col + 1):
                if (row == adj_row) & (col == adj_col):
                    pass
                else:
                    value: str = self.state[adj_row][adj_col]
                    adj_values[value] += 1
        return adj_values

    def _enhanced_adjacent_values(self, row: int, col: int) -> Counter[str]:
        """Count how many of each type of tile are adjacent to a tile by line of sight.

        Parameters
        ----------
        row: int
            row coordinate for the value
        col: int
            col coordinate for the value

        Returns
        -------
        Counter
            How many of each type of tile is in the adjacent tiles
        """
        adj_values: Counter[str] = Counter()
        vectors: Tuple[int, int, int] = (-1, 0, 1)
        # Don't worry about empty tiles
        for row_vec in vectors:
            for col_vec in vectors:
                if row_vec == 0 == col_vec:
                    pass
                else:
                    check_row: int = row
                    check_col: int = col
                    check_val: str = "."
                    while check_val == ".":
                        check_row += row_vec
                        check_col += col_vec
                        row_in_bounds: bool = 0 <= check_row < self.rows
                        col_in_bounds: bool = 0 <= check_col < self.cols
                        if row_in_bounds & col_in_bounds:
                            check_val = self.state[check_row][check_col]
                        else:
                            check_val = "B"
                    adj_values[check_val] += 1
        return adj_values

    def _update_value(self, row: int, col: int) -> str:
        """Calculate the next state of a point based on the rules.

        Parameters
        ----------
        row: int
            The row index of the value
        col: int
            The column index of the value

        Returns
        -------
        str
            What the value should be updated to.
        """
        current_val: str = self.state[row][col]
        if current_val == ".":
            return current_val
        adjacent_vals: Counter[str] = self._adjacent_values(row, col)
        if (current_val == "L") & (adjacent_vals["#"] == 0):
            return "#"
        elif (current_val == "#") & (adjacent_vals["#"] >= 4):
            return "L"
        else:
            return current_val

    def _enhanced_update_value(self, row: int, col: int) -> str:
        """Calculate the next state of a point based on the rules.

        Parameters
        ----------
        row: int
            The row index of the value
        col: int
            The column index of the value

        Returns
        -------
        str
            What the value should be updated to.
        """
        current_val: str = self.state[row][col]
        if current_val == ".":
            return current_val
        adjacent_vals: Counter[str] = self._enhanced_adjacent_values(row, col)
        if (current_val == "L") & (adjacent_vals["#"] == 0):
            return "#"
        elif (current_val == "#") & (adjacent_vals["#"] >= 5):
            return "L"
        else:
            return current_val

    def get_next_state(self, update_func: str = "original") -> List[List[str]]:
        """Calculate what the next state would be.

        Parameters
        ----------
        update_func: str
            Update function to call, "original" or "enhanced"

        Returns
        -------
        List[List[str]]
            The next state of the lobby
        """
        func_dict: Dict[str, Callable[[int, int], str]] = {
            "original": self._update_value,
            "enhanced": self._enhanced_update_value,
        }
        updater: Callable[[int, int], str] = func_dict[update_func]
        new_state: List[List[str]] = copy.deepcopy(self.state)
        for row in range(self.rows):
            for col in range(self.cols):
                new_state[row][col] = updater(row, col)
        return new_state

    def is_stabilized(self, new_layout: List[List[str]]) -> bool:
        """Check if we've reached equilibrium.

        Parameters
        ----------
        new_layout: List[List[str]]
            The updated layout to compare to the current state

        Returns
        -------
        bool:
            Whether all tiles are identical
        """
        if len(self.state) != len(new_layout):
            return False
        if len(self.state[0]) != len(new_layout[0]):
            return False
        for row in range(len(self.state)):
            for col in range(len(self.state[0])):
                if self.state[row][col] != new_layout[row][col]:
                    return False
        return True

    def run_to_equilibrium(self, update_func: str = "original") -> None:
        """Keep updating until we stabilize.

        Parameters
        ----------
        update_func: str
            Update function to call, "original" or "enhanced"
        """
        while True:
            next_state: List[List[str]] = self.get_next_state(update_func)
            if self.is_stabilized(next_state):
                break
            else:
                self.state = next_state

    def calc_occupied_seats(self) -> int:
        """Count the number of currently occupied seats.

        Returns
        -------
        int
            The number of occupied seats.
        """
        occupied_seats: int = 0
        for row in range(len(self.state)):
            for col in range(len(self.state[0])):
                if self.state[row][col] == "#":
                    occupied_seats += 1
        return occupied_seats


def read_inputs(filename: str = "input.txt") -> List[List[str]]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    list[int]
        The layout
    """
    in_path: Path = Path(__file__).resolve().parent / filename
    with open(in_path, "r") as f:
        return [[char for char in line.strip()] for line in f.readlines()]


def part1(filename: str = "input.txt") -> int:
    """Solve part 1 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The answer to part 1
    """
    lobby: Lobby = Lobby(read_inputs(filename))
    lobby.run_to_equilibrium()
    return lobby.calc_occupied_seats()


def part2(filename: str = "input.txt") -> int:
    """Solve part 2 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The answer to part 2
    """
    lobby: Lobby = Lobby(read_inputs(filename))
    lobby.run_to_equilibrium("enhanced")
    return lobby.calc_occupied_seats()


if __name__ == "__main__":
    part2("example.txt")
