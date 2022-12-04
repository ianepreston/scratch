"""Command-line interface."""
import datetime as dt
import importlib

import click


@click.command()
@click.version_option()
@click.option("-y", "--year", type=str, default=None)
@click.option("-d", "--day", type=str, default=1)
# @click.option("-p", "--part", type=str, default=None)
def main(year: int, day: int) -> None:
    """Ian's Advent of Code."""
    if year is None:
        year = dt.date.today().year
    if day is None:
        day = dt.date.today().day
    module = f"advent_ipreston.year_{year}.day{str(day).zfill(2)}.puzzle"
    daymod = importlib.import_module(module)

    click.echo(f"Puzzle for {year}, day {day}")
    click.echo(f"Part 1: {daymod.part1('puzzle.txt')}")
    click.echo(f"Part 2: {daymod.part2('puzzle.txt')}")


if __name__ == "__main__":
    main(prog_name="advent-ipreston")  # pragma: no cover
