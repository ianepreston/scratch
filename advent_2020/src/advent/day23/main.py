"""Day 23 of the advent of code challenge."""
# mypy: no-strict-optional
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

EG_CUPS = [int(x) for x in "389125467"]
IN_CUPS = [int(x) for x in "459672813"]


@dataclass
class Cup:
    """I'm a cup, also a doubly linked list."""

    val: int
    prev: Optional[Cup] = None
    next: Optional[Cup] = None

    def __repr__(self) -> str:
        """Show an easier representation for debugging.

        Returns
        -------
        str:
            cup val plus the values of its previous and next cups
        """
        if not self.prev:
            prev_txt = "None"
        else:
            prev_txt = str(self.prev.val)
        if not self.next:
            next_txt = "None"
        else:
            next_txt = str(self.next.val)
        return f"val: {self.val}, prev: {prev_txt}, next: {next_txt}"


class CupGame:
    """Let's play a game with a crab."""

    def __init__(self, start_cups: List[int], to_million: bool = False) -> None:
        """Set up the cup game.

        Parameters
        ----------
        start_cups: List[int]
            The puzzle input
        to_million: bool
            Are we doing part 2?
        """
        if to_million:
            extend_start = max(start_cups) + 1
            start_cups.extend(i for i in range(extend_start, 1_000_001))
        self.min: int = min(start_cups)
        self.max: int = max(start_cups)
        self.cup_dict: Dict[int, Cup] = dict()
        first = prev = current = Cup(start_cups[0], None, None)
        self.cup_dict[start_cups[0]] = first
        for cup_num in start_cups[1:]:
            current = Cup(val=cup_num, prev=prev, next=None)
            self.cup_dict[cup_num] = current
            prev.next = current
            prev = current
        # close the loop
        last = self.cup_dict[start_cups[-1]]
        last.next = first
        first.prev = last
        self.current_cup: Cup = first

    def _decrement(self, num: int) -> int:
        """Follow crab decrement rules.

        Parameters
        ----------
        num: int
            The value to decrement

        Returns
        -------
        int:
            The decremented value
        """
        if num <= self.min:
            return self.max
        else:
            return num - 1

    def move(self) -> None:
        """Play a round of the cup game.

        The crab picks up the three cups that are immediately clockwise of the current cup.
        They are removed from the circle; cup spacing is adjusted as necessary to maintain
        the circle.

        The crab selects a destination cup: the cup with a label equal to the current cup's
        label minus one. If this would select one of the cups that was just picked up, the
        crab will keep subtracting one until it finds a cup that wasn't just picked up.
        If at any point in this process the value goes below the lowest value on any cup's
        label, it wraps around to the highest value on any cup's label instead.

        The crab places the cups it just picked up so that they are immediately clockwise of
        the destination cup. They keep the same order as when they were picked up.

        The crab selects a new current cup: the cup which is immediately clockwise of the
        current cup.
        """
        # Pick cups
        next1: Cup = self.current_cup.next
        next2: Cup = next1.next
        next3: Cup = next2.next

        val1 = next1.val
        val2 = next2.val
        val3 = next3.val

        # Close the loop
        self.current_cup.next = next3.next
        next3.next.prev = self.current_cup

        # Pick the destination number
        dest_val = self._decrement(self.current_cup.val)
        while dest_val in [val1, val2, val3]:
            dest_val = self._decrement(dest_val)

        # reinsert the missing cups
        dest_cup = self.cup_dict[dest_val]
        stitch_end = dest_cup.next
        dest_cup.next = next1
        next1.prev = dest_cup
        next3.next = stitch_end
        stitch_end.prev = next3

        # update starting cup for the next round
        self.current_cup = self.current_cup.next

    def part1(self) -> str:
        """Get the output format of part 1 after sufficient rounds.

        Returns
        -------
        str:
            The string representation starting with (but not including) cup 1
        """
        cup = self.cup_dict[1]
        cup_seq = []
        for _ in range(len(self.cup_dict)):
            cup_seq.append(cup.val)
            cup = cup.next
        return "".join(str(cup) for cup in cup_seq)[1:]


def part1(cups: List[int] = IN_CUPS) -> str:
    """Solve part 1 of the puzzle.

    Parameters
    ----------
    cups: List[int]
        The starting sequence of cups

    Returns
    -------
    int:
        The answer to part 1
    """
    cup_game = CupGame(cups, to_million=False)
    for _ in range(100):
        cup_game.move()
    return cup_game.part1()


def part2(cups: List[int] = IN_CUPS) -> int:
    """Solve part 2 of the puzzle.

    Parameters
    ----------
    cups: List[int]
        The starting sequence of cups

    Returns
    -------
    int:
        The answer to part 2
    """
    cup_game = CupGame(cups, to_million=True)
    for _ in range(10_000_000):
        cup_game.move()
    cup1 = cup_game.cup_dict[1]
    next1 = cup1.next
    next2 = next1.next
    return next1.val * next2.val
