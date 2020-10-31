"""CLI for advent challenges.

https://www.pluralsight.com/tech-blog/python-cli-utilities-with-poetry-and-typer/
"""
import typer

app = typer.Typer()


@app.command()
def run_day(
    day: int = typer.Argument(..., help="Challenge day", min=0, max=25),
    part: int = typer.Argument(..., help="Challenge part", min=1, max=2),
) -> None:
    """Call part 1 or 2 of a day's challenge."""
    module = f"day{day:02}"
    partfunc = f"part{part}"
    try:
        exec(f"from .{module}.main import {partfunc}")
    except ImportError:
        typer.echo(f"Couldn't import {partfunc} from {module}.main")
        raise typer.Exit(code=1)
    typer.echo(f"Day: {module} Part: {partfunc}")
    result = eval(f"{partfunc}()")
    typer.echo(result)


def main() -> None:
    app()
