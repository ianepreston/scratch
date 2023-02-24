"""I'm a computer, stop all the downloading."""
from __future__ import annotations

from pathlib import Path
from typing import List, NamedTuple, Set, Union


class Instruction(NamedTuple):
    """I'm an instruction."""

    cmd: str
    num: int

    @staticmethod
    def parse(line: str) -> Instruction:
        """Turn a line of text into an Instruction.
        
        Parameters
        ----------
        line: str
            An instruction in string form
        
        Returns
        -------
        Instruction
            The parsed instruction
        """
        cmd, num = line.strip().split()
        return Instruction(cmd, int(num))


def instructions_from_file(file: Union[Path, str]) -> List[Instruction]:
    """Read in a text file to get a list of Instructions.

    Parameters
    ----------
    file: Path, str
        The file to load
    
    Returns
    -------
    List[Instructions]
        All the instructions in the file
    """
    with open(file, "r") as f:
        return [Instruction.parse(line) for line in f.readlines()]


class Compy:
    """I'm a computer."""

    def __init__(self, instructions: List[Instruction]) -> None:
        """Instantiate with index and accumulator at 0.
        
        Parameters
        ----------
        instructions: List[Instruction]
            The program to run
        """
        self.index: int = 0
        self.accumulator: int = 0
        self.instructions: List[Instruction] = instructions
        self.run_complete: bool = False

    def _exec_instruction(self, instruction: Instruction) -> None:
        """Run an instruction.
        
        Parameters
        ----------
        instruction: Instruction
            The instruction to run
        """
        if instruction.cmd == "nop":
            pass
            self.index += 1
        elif instruction.cmd == "acc":
            self.accumulator += instruction.num
            self.index += 1
        elif instruction.cmd == "jmp":
            if 0 <= self.index + instruction.num <= len(self.instructions):
                self.index += instruction.num
            else:
                raise IndexError("Jumped out of instruction set")
        else:
            raise ValueError(f"Unsupported instruction: {instruction.cmd}")
        if self.index == len(self.instructions):
            self.run_complete = True

    def step(self) -> None:
        """Execute the next instruction."""
        instruction: Instruction = self.instructions[self.index]
        self._exec_instruction(instruction)

    def full_run(self) -> None:
        """Execute the program all the way through."""
        while not self.run_complete:
            self.step()

    def loops_forever(self) -> bool:
        """Check if a program is an infinite loop.

        Returns
        -------
        bool:
            Whether the program will loop forever or not
        """
        indices: Set[int] = set()
        while True:
            if self.index in indices:
                # Reset before returning
                self.index = 0
                self.accumulator = 0
                self.run_complete = False
                return True
            elif self.run_complete:
                # Reset before returning
                self.index = 0
                self.accumulator = 0
                self.run_complete = False
                return False
            else:
                indices.add(self.index)
                self.step()
