"""Day 07 of the advent of code challenge."""
from __future__ import annotations

from pathlib import Path
import re
from typing import Dict, List, Optional, Tuple


class Bag:
    """A bag and the rules about its contents."""

    def __init__(self, adjective: str, colour: str) -> None:
        """Make a bag.

        Parameters
        ----------
        adjective: str
            Modifier on the colour, e.g. shiny
        colour: str
            The actual colour, e.g. gold
        """
        self.adjective: str = adjective
        self.colour: str = colour
        self.directly_contains: List[Tuple[Bag, int]] = list()

    @property
    def name(self: Bag) -> str:
        """Concatenation of adjective and colour.

        Returns
        -------
        str
            the name in <adjective>_<colour> format
        """
        return f"{self.adjective}_{self.colour}"

    def __repr__(self) -> str:
        """Concatenation of adjective and colour.

        Returns
        -------
        str
            the name in <adjective>_<colour> format
        """
        return self.name

    def __str__(self) -> str:
        """Concatenation of adjective and colour.

        Returns
        -------
        str
            the name in <adjective>_<colour> format
        """
        return self.name

    def subcontains(self, name: str) -> bool:
        """Check if the bag contains another bag, directly or indirectly.

        Parameters
        ----------
        name: str
            The name of the bag we're looking for
        
        Returns
        -------
        bool:
            Whether that bag will be somewhere in this bag
        """
        if len(self.directly_contains) == 0:
            return False
        elif any(bag.name == name for bag, _ in self.directly_contains):
            return True
        else:
            return any(bag.subcontains(name) for bag, _ in self.directly_contains)

    def contain_count(self) -> int:
        """Find how many bags you have to put in this bag.

        Returns
        -------
        int:
            How many bags the weird rules make you put in this bag
        """
        if len(self.directly_contains) == 0:
            return 0
        else:
            return sum(
                count + (count * bag.contain_count())
                for bag, count in self.directly_contains
            )


def split_contains_txt(split_contains_txt: str) -> Tuple[int, str, str]:
    """Parse one of the container clauses for a rule.

    Parameters
    ----------
    split_contains_txt: str
        Something like "2 dark red"
    
    Returns
    -------
    int, str, str
        The count, adjective, and colour of the bag
    """
    rgx: re.Pattern = re.compile(r"(\d+) (\w+) (\w+)")
    match: Optional[re.Match] = rgx.match(split_contains_txt)
    if match is None:
        raise ValueError(f"cannot parse contained bags for {split_contains_txt}")
    count_str: str
    adjective: str
    colour: str
    count_str, adjective, colour = match.groups()
    count: int = int(count_str)
    return count, adjective, colour


def split_line(line: str) -> Tuple[str, str, List[Tuple[int, str, str]]]:
    """Take a rule line and break it up.

    Parameters
    ----------
    line: str
        The fully expressed rule for a bag
    
    Returns
    -------
    str, str [(int, str, str)]
        the adjective and colour of the bag, and a list of the count and colour
        of bags it contains
    """
    rgx: re.Pattern = re.compile(r"^(\w+) (\w+) bags contain (.*)$")
    match: Optional[re.Match] = rgx.match(line)
    if match is None:
        raise ValueError(f"rule could not be parsed for {line}")
    adjective: str
    colour: str
    contains: str
    adjective, colour, contains = match.groups()
    contain_rgx: re.Pattern = re.compile(r"(\d+ \w+ \w+) bags?")
    contains_txt_list: List[str] = contain_rgx.findall(contains)
    contains_clean_list: List[Tuple[int, str, str]] = [
        split_contains_txt(contains) for contains in contains_txt_list
    ]
    return adjective, colour, contains_clean_list


def read_inputs(filename: str = "input.txt") -> Dict[str, Bag]:
    """Read in and parse a text file of inputs.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    dict:
        A dictionary of all bags
    """
    bag_dict: Dict[str, Bag] = dict()
    here: Path = Path(__file__).resolve().parent
    in_path: Path = here / filename
    with open(in_path, "r") as f:
        for line in f.readlines():
            adjective: str
            colour: str
            contains: List[Tuple[int, str, str]]
            adjective, colour, contains = split_line(line.strip())
            name_key: str = f"{adjective}_{colour}"
            if name_key not in bag_dict:
                bag_dict[name_key] = Bag(adjective, colour)
            for contained in contains:
                contained_key: str = f"{contained[1]}_{contained[2]}"
                if contained_key not in bag_dict:
                    bag_dict[contained_key] = Bag(contained[1], contained[2])
                bag_dict[name_key].directly_contains.append(
                    (bag_dict[contained_key], contained[0])
                )
    return bag_dict


def part1(filename: str = "input.txt") -> int:
    """Solve part 1 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The number of bags that contain the shiny gold bag
    """
    bag_dict = read_inputs(filename)
    # return bag_dict
    return sum(bag.subcontains("shiny_gold") for bag in bag_dict.values())


def part2(filename: str = "input.txt") -> int:
    """Solve part 2 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The number of bags that the shiny gold bag contains
    """
    bag_dict = read_inputs(filename)
    shiny_gold: Bag = bag_dict["shiny_gold"]
    return shiny_gold.contain_count()
