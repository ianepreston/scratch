"""Supply Stacks."""

import re
import string
from typing import Callable
from typing import NamedTuple

from advent_ipreston.helpers import inputs_generator


class Instruction(NamedTuple):
    """Instruction to move a number of crates from one pile to another."""

    quantity: int
    source: int
    target: int


def split_tower_instructions(infile: str) -> tuple[list[str], list[str]]:
    """Split the puzzle input into the tower section and the instructions section."""
    tower = []
    instructions = []
    target_list = tower
    for line in inputs_generator(infile):
        if line == "":
            target_list = instructions
        else:
            target_list.append(line)
    return tower, instructions


def create_tower(tower_list: list[str]) -> dict[int, list[str]]:
    """Take a list of tower entries and create a tower dictionary."""
    # Last piece of the list is tower numbers, find the positions of all of them
    tower_indices = tuple(
        i for i, character in enumerate(tower_list.pop()) if character.strip()
    )
    # Create our tower data structure with empty lists of blocks
    tower = {i + 1: [] for i in range(len(tower_indices))}
    # Map tower names to index position
    index_to_tower = {index: i + 1 for i, index in enumerate(tower_indices)}
    # Start building the tower
    while tower_list:
        row = tower_list.pop()
        for index in tower_indices:
            # Ooops, I trim whitespace so we can have index errors.
            if index < len(row) and row[index] in string.ascii_letters:
                tower[index_to_tower[index]].append(row[index])
    return tower


def parse_instructions(instructions: list[str]) -> list[Instruction]:
    """Clean up the instructions."""
    # Could do this as a giant comprehension but that seems real hard to read
    clean_instructions = []
    for instruction in instructions:
        parts = re.split(r"from|to", instruction.replace("move", ""))
        quantity, source, target = (int(part) for part in parts)
        clean_instructions.append(Instruction(quantity, source, target))
    return clean_instructions


def follow_instruction_part1(
    tower: dict[int, list[str]], instruction: Instruction
) -> dict[int, list[str]]:
    """Follow the instruction and return the updated tower."""
    for _ in range(instruction.quantity):
        block = tower[instruction.source].pop()
        tower[instruction.target].append(block)
    return tower


def follow_instruction_part2(
    tower: dict[int, list[str]], instruction: Instruction
) -> dict[int, list[str]]:
    """Follow the instruction and return the updated tower."""
    blocks = [tower[instruction.source].pop() for _ in range(instruction.quantity)]
    for _ in range(instruction.quantity):
        tower[instruction.target].append(blocks.pop())
    return tower


def follow_instructions(
    tower: dict[int, list[str]],
    instructions: list[Instruction],
    instruction_func: Callable,
) -> dict[int, list[str]]:
    """Follow the instructions and return the updated tower."""
    for instruction in instructions:
        tower = instruction_func(tower, instruction)
    return tower


def find_top_crates(tower: dict[int, list[str]]):
    """Find the message of the top crates in a tower."""
    return "".join(tower[i + 1][-1] for i in range(len(tower)))


def part1(infile: str) -> str:
    """Solve part 1."""
    tower_list, raw_instructions = split_tower_instructions(infile)
    tower = create_tower(tower_list)
    instructions = parse_instructions(raw_instructions)
    finished_tower = follow_instructions(tower, instructions, follow_instruction_part1)
    return find_top_crates(finished_tower)


def part2(infile: str) -> str:
    """Solve part 2."""
    tower_list, raw_instructions = split_tower_instructions(infile)
    tower = create_tower(tower_list)
    instructions = parse_instructions(raw_instructions)
    finished_tower = follow_instructions(tower, instructions, follow_instruction_part2)
    return find_top_crates(finished_tower)
