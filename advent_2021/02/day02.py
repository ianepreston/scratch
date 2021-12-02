"""Solve day 2 of the advent of code 2021."""
from pathlib import Path
from typing import Generator, NamedTuple


class Instruction(NamedTuple):
    direction: int
    amount: int


class Position(NamedTuple):
    horizontal: int
    depth: int


class SubStatus(NamedTuple):
    position: Position
    aim: int


def split_instruction(line: str) -> Instruction:
    """Take a line input and produce a formatted instruction."""
    direction, amountstr = line.split(" ")
    return Instruction(direction.strip(), int(amountstr))


def generate_instructions(infile: str) -> Generator[Instruction, None, None]:
    """Yield instructions from a text file."""
    inpath = Path(__file__).resolve().parent / infile
    with open(inpath, "r") as f:
        for line in f.readlines():
            yield split_instruction(line)


def part1_update_position(
    current_position: Position, instruction: Instruction
) -> Position:
    """Follow a direction to update position"""
    delta = instruction.amount
    directions = {
        "forward": Position(delta, 0),
        "up": Position(0, -1 * delta),
        "down": Position(0, 1 * delta),
    }
    direction_vector = directions[instruction.direction]
    new_horizontal = current_position.horizontal + direction_vector.horizontal
    new_depth = current_position.depth + direction_vector.depth
    return Position(new_horizontal, new_depth)


def part2_update_sub(current_status: SubStatus, instruction: Instruction) -> SubStatus:
    """Follow a direction to update sub status (position and aim)."""
    if instruction.direction == "forward":
        horizontal_delta = instruction.amount
        depth_delta = current_status.aim * instruction.amount
        new_horizontal = current_status.position.horizontal + horizontal_delta
        new_depth = current_status.position.depth + depth_delta
        new_status = SubStatus(Position(new_horizontal, new_depth), current_status.aim)
    else:
        aim_dict = {"up": instruction.amount * -1, "down": instruction.amount}
        aim_delta = aim_dict[instruction.direction]
        new_aim = current_status.aim + aim_delta
        new_status = SubStatus(current_status.position, new_aim)
    return new_status


def part1_navigate(infile: str) -> Position:
    """Follow instructions."""
    current_position = Position(0, 0)
    for instruction in generate_instructions(infile):
        current_position = part1_update_position(current_position, instruction)
    return current_position


def part1(infile: str) -> int:
    """Complete part 1."""
    final_position = part1_navigate(infile)
    return final_position.depth * final_position.horizontal


def part2(infile: str) -> int:
    """Complete part 2."""
    current_status = SubStatus(Position(0, 0), 0)
    for instruction in generate_instructions(infile):
        current_status = part2_update_sub(current_status, instruction)
    final_position = current_status.position
    return final_position.depth * final_position.horizontal


if __name__ == "__main__":
    eg1 = part1("example.txt")
    if eg1 != 150:
        raise ValueError(f"Example 1 should be 150, got {eg1}")
    answer1 = part1("input.txt")
    print(f"Part 1: {answer1}")
    eg2 = part2("example.txt")
    if eg2 != 900:
        raise ValueError(f"Example 1 part 2 should be 900, got {eg2}")
    answer2 = part2("input.txt")
    print(f"Part 2: {answer2}")
