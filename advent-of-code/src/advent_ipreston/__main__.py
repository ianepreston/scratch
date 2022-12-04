"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Ian's Advent of Code."""


if __name__ == "__main__":
    main(prog_name="advent-ipreston")  # pragma: no cover
