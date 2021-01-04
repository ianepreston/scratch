"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Data Science From Scratch."""


if __name__ == "__main__":
    main(prog_name="ds_from_scratch")  # pragma: no cover
