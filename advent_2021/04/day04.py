"""Day 4 of the advent of code challenge 2021."""

from os import unsetenv
from pathlib import Path

from typing import Dict, List, Tuple


def parse_bingo_draws(line: str) -> List[int]:
    """Take the first line of the puzzle input and get a list of bingo draws."""
    return [int(x) for x in line.split(",")]


def read_inputs(infile: str) -> Tuple[List[int], List[Dict[Tuple[int, int], int]]]:
    """Get the puzzle inputs into basic data structures."""
    in_dir = Path(__file__).resolve().parent
    in_path = in_dir / infile
    bingo_boards: List[Dict[Tuple[int, int], int]] = list()
    bingo_board = None
    bingo_row = 0
    with open(in_path, "r") as f:
        draws: List[int] = parse_bingo_draws(f.readline())
        for line in f.readlines():
            if line == "\n":
                if bingo_board:
                    bingo_boards.append(bingo_board)
                bingo_board = dict()
                bingo_row = 0
            else:
                row_entries = [int(x) for x in line.strip().split(" ") if x]
                for col, entry in enumerate(row_entries):
                    bingo_board[(bingo_row, col)] = entry
                bingo_row += 1
    # Add that last board
    bingo_boards.append(bingo_board)
    return draws, bingo_boards


class BingoBoard:
    def __init__(self, board_dict: Dict[Tuple[int, int], int]) -> None:
        self.board: Dict[Tuple[int, int], int] = board_dict
        self.visited: Dict[Tuple[int, int], bool] = self.make_empty_visit_grid()
        self.seen_draws: List[int] = list()

    def make_empty_visit_grid(self):
        visit_dict = dict()
        for x in range(5):
            for y in range(5):
                visit_dict[(x, y)] = False
        return visit_dict

    def add_draw(self, draw: int) -> None:
        self.seen_draws.append(draw)
        for position, value in self.board.items():
            if draw == value:
                self.visited[position] = True

    @property
    def have_won(self) -> bool:
        for a in range(5):
            row_check = all([self.visited[(a, b)] for b in range(5)])
            col_check = all([self.visited[(b, a)] for b in range(5)])
            if row_check or col_check:
                return True
        return False

    def sum_unmarked(self) -> int:
        unseen_draws: List[int] = list()
        for position, value in self.board.items():
            if not self.visited[position]:
                unseen_draws.append(value)
        return sum(unseen_draws)

    def final_score(self) -> int:
        if not self.have_won:
            raise RuntimeError("Shouldn't have called this without winning.")
        return self.sum_unmarked() * self.seen_draws[-1]


def part1(infile: str) -> int:
    draws, raw_boards = read_inputs(infile)
    boards = [BingoBoard(raw_board) for raw_board in raw_boards]
    for draw in draws:
        for board in boards:
            board.add_draw(draw)
            if board.have_won:
                return board.final_score()


def part2(infile: str) -> int:
    draws, raw_boards = read_inputs(infile)
    all_boards = [BingoBoard(raw_board) for raw_board in raw_boards]
    for draw in draws:
        unfinished_boards = [board for board in all_boards if not board.have_won]
        for board in unfinished_boards:
            board.add_draw(draw)
            if board.have_won and len(unfinished_boards) == 1:
                return board.final_score()


if __name__ == "__main__":
    eg1 = part1("example.txt")
    eg1s = 4512
    if eg1 != eg1s:
        raise RuntimeError(f"eg1 got {eg1}, expected {eg1s}")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
    eg2 = part2("example.txt")
    eg2s = 1924
    if eg2 != eg2s:
        raise RuntimeError(f"eg2 got {eg2}, expected {eg2s}")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")