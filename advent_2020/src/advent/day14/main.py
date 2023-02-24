"""Day 14 of the advent of code challenge."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import re
from typing import List, NamedTuple, Optional


def int_to_bits(num: int, nbits: int = 36) -> str:
    """Turn an integer into a 32 bit unsigned int.

    Parameters
    ----------
    num: int
        input integer
    nbits: int
        length of the bitstring (0 padding)
    
    Returns
    -------
    str
        nbits bit unsigned integer
    """
    return f"{num:0b}".zfill(nbits)


def bits_to_int(bits: str) -> int:
    """Turn a bitstring back to an integer.
    
    Parameters
    ----------
    bits: str
        String representation of binary
    
    Returns
    -------
    int
        The integer equivalent
    """
    return int(bits, 2)


class Address(NamedTuple):
    """Index and value."""

    location: int
    value: int


def parse_bitmasks(line: str) -> str:
    """Parse a bitmask out of a line in the input.

    Parameters
    ----------
    line: str
        Line from the input file
    
    Returns
    -------
    str:
        Clean text string of the bitmask
    """
    return line.strip().replace("mask = ", "")


def apply_bitmasks(bitmasks: str, value: int) -> int:
    """Apply a bitmask to an integer.

    Parameters
    ----------
    bitmasks: str
        The bitmask to apply
    value: int
        The integer to apply the bitmask to
    
    Returns
    -------
    int
        Integer value after bitmask is applied
    """
    value_bitstring = int_to_bits(value)
    value_bitlist = [c for c in value_bitstring]
    for index, bitmask in enumerate(bitmasks):
        if bitmask != "X":
            value_bitlist[index] = bitmask
    return bits_to_int("".join(c for c in value_bitlist))


def apply_bitmasks2(bitmask: str, index: int) -> List[int]:
    """Apply a bitmask using part 2 rules to an integer.

    Parameters
    ----------
    bitmask: str
        The bitmask to apply
    index: int
        The index integer to apply the bitmask on
    
    Returns
    -------
    List[int]
        All permutations of the bitmasked address
    """
    index_bitstring: str = int_to_bits(index)
    index_bitlist: List[str] = [c for c in index_bitstring]
    # Do the simple flips first
    floating_indices = []
    for i, v in enumerate(c for c in bitmask):
        if v == "1":
            index_bitlist[i] = v
        elif v == "X":
            floating_indices.append(i)
    # If there's no masks we're set
    if not floating_indices:
        return [bits_to_int("".join(index_bitlist))]
    # Handle all the permutations
    permutations: int = 2 ** len(floating_indices)
    addresses: List[int] = []
    for i in range(permutations):
        update_bitlist: List[str] = index_bitlist[:]
        mask_str: str = f"{i:0b}".zfill(len(floating_indices))
        for j, v in zip(floating_indices, mask_str):
            update_bitlist[j] = v
        addresses.append(bits_to_int("".join(update_bitlist)))
    return addresses


def parse_address(line: str) -> Address:
    """Line of text to address to update.
    
    Parameters
    ----------
    line: str
        Turn a line from the input into an Address
    
    Returns
    -------
    Address
        Parsed index and value
    """
    rgx = r"mem\[(\d+)\] = (\d+)"
    address_str: str
    value_str: str
    match: Optional[re.Match] = re.match(rgx, line)
    if match is None:
        raise ValueError("No address match for {line}")
    address_str, value_str = match.groups()
    return Address(int(address_str), int(value_str))


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
    # initialize empty bitmask
    bitmask: str = ""
    addresses: Counter = Counter()
    in_path: Path = Path(__file__).resolve().parent / filename
    with open(in_path, "r") as f:
        for line in f.readlines():
            if line.startswith("mask"):
                bitmask = parse_bitmasks(line)
            elif line.startswith("mem"):
                address: Address = parse_address(line)
                addresses[address.location] = apply_bitmasks(bitmask, address.value)
            else:
                raise ValueError(f"unrecognized line: {line}")
    return sum(addresses.values())


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
    bitmask: str = ""
    addresses: Counter = Counter()
    in_path: Path = Path(__file__).resolve().parent / filename
    with open(in_path, "r") as f:
        for line in f.readlines():
            if line.startswith("mask"):
                bitmask = parse_bitmasks(line)
            elif line.startswith("mem"):
                address: Address = parse_address(line)
                for index in apply_bitmasks2(bitmask, address.location):
                    addresses[index] = address.value
            else:
                raise ValueError(f"unrecognized line: {line}")
    return sum(addresses.values())
