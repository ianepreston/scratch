"""Day 22 of the advent of code challenge."""
from __future__ import annotations

from collections import deque
from pathlib import Path
from typing import Deque, Tuple


def read_input(filename: str) -> Tuple[Deque[int], Deque[int]]:
    """Load the puzzle input.

    Parameters
    ----------
    filename: str
        input.txt or example.txt
    
    Returns
    -------
    Tuple[List[int], List[int]]
        The starting decks
    """
    file: Path = Path(__file__).resolve().parent / filename
    with open(file, "r") as f:
        deckstr1, deckstr2 = f.read().split("\n\n")
        deck1 = deque([int(x) for x in deckstr1.split("\n")[1:]])
        deck2 = deque([int(x) for x in deckstr2.split("\n")[1:]])
    return deck1, deck2


def play_war(deck1: Deque[int], deck2: Deque[int]) -> Deque[int]:
    """Play a game of war.
    
    Parameters
    ----------
    deck1: Deque[int]
        Player one's starting hand
    deck2: Deque[int]
        Player two's starting hand
    
    Returns
    -------
    Deque[int]
        The winning deck after playing
    """
    while deck1 and deck2:
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        elif card2 > card1:
            deck2.append(card2)
            deck2.append(card1)
        else:
            raise ValueError("I don't know how to handle ties")
    if deck1:
        return deck1
    else:
        return deck2


def play_recursive_war(deck1: Deque[int], deck2: Deque[int]) -> Tuple[int, Deque[int]]:
    """Play a game of war.
    
    Parameters
    ----------
    deck1: Deque[int]
        Player one's starting hand
    deck2: Deque[int]
        Player two's starting hand
    
    Returns
    -------
    Deque[int]
        The winning deck after playing
    """
    set1 = list()
    set2 = list()
    while deck1 and deck2:
        # Check for infinite loop
        if (deck1 in set1) and (deck2 in set2):
            # player 1 automatically wins those
            return 1, deck1
        set1.append(deck1.copy())
        set2.append(deck2.copy())
        card1 = deck1.popleft()
        card2 = deck2.popleft()
        if (card1 <= len(deck1)) and (card2 <= len(deck2)):
            winning_player, _ = play_recursive_war(
                deque(list(deck1.copy())[:card1]), deque(list(deck2.copy())[:card2])
            )
            if winning_player == 1:
                deck1.append(card1)
                deck1.append(card2)
            else:
                deck2.append(card2)
                deck2.append(card1)
        elif card1 > card2:
            deck1.append(card1)
            deck1.append(card2)
        elif card2 > card1:
            deck2.append(card2)
            deck2.append(card1)
        else:
            raise ValueError("I don't know how to handle ties")
    if deck1:
        return 1, deck1
    else:
        return 2, deck2


def tally_points(deck: Deque[int]) -> int:
    """Score the winning deck.
    
    Parameters
    ----------
    deck: Deque[int]
        The final deck of the winning player
    
    Returns
    -------
    int
        The score of the winner
    """
    # reorder for easier tallying
    deck.reverse()
    return sum(((i + 1) * card) for i, card in enumerate(deck))


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
    deck1, deck2 = read_input(filename)
    winning_deck = play_war(deck1, deck2)
    return tally_points(winning_deck)


def part2(filename: str = "input.txt") -> int:
    """Solve part 2 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    str:
        The answer to part 2
    """
    deck1, deck2 = read_input(filename)
    winning_player, winning_deck = play_recursive_war(deck1, deck2)
    return tally_points(winning_deck)
