"""Command-line interface."""
import datetime as dt
import importlib

import click


@click.command()
@click.version_option()
@click.option(
    "-y", "--year", type=str, default=None, help="Puzzle year (default current)"
)
@click.option(
    "-d", "--day", type=str, default=None, help="Puzzle day (default current)"
)
# @click.option("-p", "--part", type=str, default=None)
def main(year: int, day: int) -> None:
    """Ian's Advent of Code puzzle runner."""
    if year is None:
        year = dt.date.today().year
    if day is None:
        day = dt.date.today().day
    module = f"advent_ipreston.year_{year}.day{str(day).zfill(2)}.puzzle"
    daymod = importlib.import_module(module)

    click.echo(f"Puzzle for {year}, day {day}")
    try:
        click.echo(f"Part 1: {daymod.part1('puzzle.txt')}")
    except AttributeError:
        click.echo(f"No part 1 for year {year}, day {day}")
    try:
        click.echo(f"Part 2: {daymod.part2('puzzle.txt')}")
    except AttributeError:
        click.echo(f"No part 2 for year {year}, day {day}")


if __name__ == "__main__":
    main(prog_name="advent-ipreston")  # pragma: no cover
