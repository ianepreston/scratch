"""Day 25 of the advent of code challenge."""
from __future__ import annotations

from typing import List


def run_loop(subject_num: int, value: int) -> int:
    """Run a loop for finding the loop size.

    Parameters
    ----------
    subject_num: int
        The subject number
    value: int
        The value to update

    Returns
    -------
    int
        The updated value
    """
    return (value * subject_num) % 20201227


def find_loop_sizes(pub_keys: List[int], subject_num: int = 7) -> List[int]:
    """Keep running loops until we've found the loop sizes for each public key.

    Parameters
    ----------
    pub_keys: List[int]
        public keys to find loop sizes for

    subject_num: int
        The shared subject number we're building the keys from

    Returns
    -------
    List[int]
        The respective loop sizes for the public keys
    """
    loop_sizes = [None for _ in range(len(pub_keys))]
    value = 1
    loops = 0
    while any(x is None for x in loop_sizes):
        value = run_loop(subject_num, value)
        loops += 1
        if value in pub_keys:
            for i, key in enumerate(pub_keys):
                if key == value:
                    loop_sizes[i] = loops  # type: ignore
    return loop_sizes  # type: ignore


def gen_encryption_key(subject_num: int, loops: int) -> int:
    """Take a public key and the other key's loop size to get a shared private key.

    Parameters
    ----------
    subject_num: int
        The public key
    loops: int
        The number of loops for the other public key

    Returns
    -------
    int
        The resulting shared key
    """
    value = 1
    for _ in range(loops):
        value = run_loop(subject_num, value)
    return value


def part1(pub_key_card: int, pub_key_door: int) -> int:
    """Solve part 1.

    Parameters
    ----------
    pub_key_card: int
        The public key of the card
    pub_key_door: int
        The public key of the door

    Returns
    -------
    int:
        The shared encryption key, the answer to part 1 of the puzzle
    """
    loops_card, loops_door = find_loop_sizes([pub_key_card, pub_key_door])
    card_encryption = gen_encryption_key(pub_key_card, loops_door)
    door_encryption = gen_encryption_key(pub_key_door, loops_card)
    if card_encryption != door_encryption:
        raise ValueError(f"card {card_encryption} doesn't match door {door_encryption}")
    return card_encryption
