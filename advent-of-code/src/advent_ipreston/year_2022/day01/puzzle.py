"""Calorie Counting."""
from advent_ipreston.helpers import inputs_generator


def part1(infile: str) -> int:
    """Solve part 1 of the puzzle.

    Parameters
    ----------
    infile: str
            puzzle input

    Returns
    -------
    int
            Solution to part 1
    """
    max_cals: int = 0
    elf_cals: int = 0
    for snack in inputs_generator(infile):
        if snack.rstrip() == "":
            elf_cals = 0
        else:
            elf_cals += int(snack)
        if elf_cals > max_cals:
            max_cals = elf_cals
    return max_cals


def part2(infile: str) -> int:
    """Solve part 1 of the puzzle.

    Parameters
    ----------
    infile: str
            puzzle input

    Returns
    -------
    int
            Solution to part 1
    """
    top_elves: list[int] = [0, 0, 0]
    elf_cals: int = 0
    for snack in inputs_generator(infile):
        if snack.rstrip() == "":
            elf_cals = 0
            top_elves.sort()
        else:
            elf_cals += int(snack)
        if elf_cals > top_elves[0]:
            top_elves[0] = elf_cals
    return sum(top_elves)


if __name__ == "__main__":
    print(f"Part 1: {part1('puzzle.txt')}")
    print(f"Part 2: {part2('puzzle.txt')}")
