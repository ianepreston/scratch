"""Scratchcards"""
from dataclasses import dataclass
from typing import Dict
from typing import Set

from advent_ipreston.helpers import inputs_generator


@dataclass
class Card:
    number: int
    winners: Set[int]
    have: Set[int]
    count: int = 1

    @property
    def matches(self) -> int:
        """Calculate how many matches there are."""
        return len(self.winners.intersection(self.have))

    @property
    def points(self) -> int:
        """Calculate how much the card is worth."""
        value: int = 0
        matches = self.matches
        if matches:
            value = 2 ** (matches - 1)
        return value

def parse_card(line: str) -> Card:
    cardnum, remainder = line.split(":")
    cardnum = int(cardnum.replace("Card", "").strip())
    winstr, havestr = remainder.split("|")
    winners = set(int(i) for i in winstr.split())
    have = set(int(i) for i in havestr.split())
    return Card(cardnum, winners, have)

def part1(infile: str) -> int:
    """Part 1"""
    points = 0
    for line in inputs_generator(infile):
        points += parse_card(line).points
    return points

def part2(infile: str) -> int:
    """Part 2."""
    cards: Dict[int, Card] = {}
    for line in inputs_generator(infile):
        card = parse_card(line)
        cards[card.number] = card
    maxcard: int = max(cards.keys())
    for cardnum in range(1, maxcard + 1):
        card = cards[cardnum]
        matches = card.matches
        if matches:
            for i in range(cardnum + 1, cardnum + matches + 1):
                cards[i].count += card.count
    return sum(card.count for card in cards.values())


if __name__ == "__main__":  # pragma: no cover
    print(f"Part 1: {part1('puzzle.txt')}")
    print(f"Part 2: {part2('puzzle.txt')}")
