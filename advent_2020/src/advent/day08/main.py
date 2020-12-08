"""Day 08 of the advent of code challenge."""
from __future__ import annotations

from pathlib import Path
from typing import List, Set

from advent.compy import Compy, Instruction, instructions_from_file


def part1(filename: str = "input.txt") -> int:
    """Solve part 1 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The value of the accumulator right before a loop
    """
    indices: Set[int] = set()
    infile: Path = Path(__file__).resolve().parent / filename
    compy: Compy = Compy(instructions_from_file(infile))
    while True:
        if compy.index in indices:
            return compy.accumulator
        else:
            indices.add(compy.index)
            compy.step()


def part2(filename: str = "input.txt") -> int:
    """Solve part 2 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The value of the accumulator after a complete run
    """
    # Has to be an index that's encountered
    indices: Set[int] = set()
    infile: Path = Path(__file__).resolve().parent / filename
    compy: Compy = Compy(instructions_from_file(infile))
    original_instructions: List[Instruction] = compy.instructions.copy()
    while compy.index not in indices:
        indices.add(compy.index)
        compy.step()
    # Bad instruction isn't necessarily the last one before the loop
    # I think I have to test all of them
    for candidate_index in indices:
        candidate_instruction: Instruction = compy.instructions[candidate_index]
        # If it's an acc step we know not to change it
        if candidate_instruction.cmd not in ("jmp", "nop"):
            continue
        swap_cmd: str
        if candidate_instruction.cmd == "jmp":
            swap_cmd = "nop"
        else:
            swap_cmd = "jmp"
        swap_instruction: Instruction = Instruction(swap_cmd, candidate_instruction.num)
        swapped_instructions: List[Instruction] = original_instructions.copy()
        swapped_instructions[candidate_index] = swap_instruction
        if not Compy(swapped_instructions).loops_forever():
            break
    compy = Compy(swapped_instructions)
    compy.full_run()
    return compy.accumulator
