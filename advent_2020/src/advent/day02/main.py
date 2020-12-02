"""Day 02 of the advent of code challenge."""
from pathlib import Path
import re
from typing import List, NamedTuple, Optional

Password = NamedTuple(
    "Password", [("lower", int), ("upper", int), ("character", str), ("password", str)]
)


def parse_line(line: str) -> Password:
    """Read a line from a text file and turn it into a Password tuple.

    Parameters
    ----------
    line: str
        The raw text

    Returns
    -------
    Password:
        A named tuple of the input
    """
    rgx: re.Pattern = re.compile(r"(\d*)-(\d*) (\w): (\w*)")
    match: Optional[re.Match] = rgx.match(line)
    if match is None:
        raise ValueError("line could not be parsed")
    lower: str
    upper: str
    character: str
    password: str
    lower, upper, character, password = match.groups()
    return Password(int(lower), int(upper), character, password)


def validate_password(password: Password) -> bool:
    """Check if a password meets its rules.

    Parameters
    ----------
    password: Password
        The password and its rules

    Returns
    -------
    Boolean:
        Whether the password is valid or not
    """
    return (
        password.lower <= password.password.count(password.character) <= password.upper
    )


def updated_validate_password(password: Password) -> bool:
    """Check if a password meets its rules updated for part 2.

    Parameters
    ----------
    password: Password
        The password and its rules

    Returns
    -------
    Boolean:
        Whether the password is valid or not
    """
    lower_index: int = password.lower - 1
    upper_index: int = password.upper - 1
    lower_match: int = int(password.password[lower_index] == password.character)
    upper_match: int = int(password.password[upper_index] == password.character)
    matches: int = lower_match + upper_match
    return matches == 1


def read_inputs(filename: str) -> List[Password]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    List[Password]
        list of formatted passwords
    """
    here: Path = Path(__file__).resolve().parent
    in_path: Path = here / filename
    with open(in_path, "r") as f:
        return [parse_line(line) for line in f.readlines()]


def part1(filename: str = "input.txt") -> int:
    """Solve part 1 of the challenge.

    Parameters
    ----------
    filename: str
        The name of the file to read in

    Returns
    -------
    int
        The number of valid passwords
    """
    return sum(validate_password(pwd) for pwd in read_inputs(filename))


def part2(filename: str = "input.txt") -> int:
    """Solve part 2 of the challenge.

    Parameters
    ----------
    filename: str
        The name of the file to read in

    Returns
    -------
    int
        The number of valid passwords
    """
    return sum(updated_validate_password(pwd) for pwd in read_inputs(filename))
