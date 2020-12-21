"""Day 21 of the advent of code challenge."""
from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
from typing import Any, DefaultDict, Dict, List, NamedTuple, Optional, Set, Tuple


class Recipe(NamedTuple):
    """Ingredient list and known allergens."""

    ingredients: Tuple[str, ...]
    allergens: Tuple[str, ...]


def parse_line(line: str) -> Recipe:
    """Turn text into a recipe.

    Parameters
    ----------
    line: str
        The input line from the puzzle
    
    Returns
    -------
    Recipe
        The recipe
    """
    rgx = re.compile(r"(^.+)\s\(contains\s(.+)\)")
    match: Optional[re.Match[str]] = rgx.match(line)
    if match is None:
        raise ValueError(f"cannot parse {line} into recipes")
    ingredient_str, allergen_str = match.groups()
    ingredients = tuple(ingredient_str.split())
    allergens = tuple(allergen_str.split(", "))
    return Recipe(ingredients, allergens)


def read_input(filename: str) -> List[Recipe]:
    """Load the recipes.

    Parameters
    ----------
    filename: str
        input.txt or example.txt
    
    Returns
    -------
    List[Recipe]
        All the recipes in the puzzle input
    """
    file: Path = Path(__file__).resolve().parent / filename
    with open(file, "r") as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def allergen_to_ingredients(recipes: List[Recipe]) -> Dict[str, str]:
    """Find which ingredients correspond to which allergen.
    
    Parameters
    ----------
    recipes: List[Recipe]
        All the recipes
    
    Returns
    -------
    Dict[str, str]
        A mapping of allergen -> ingredient
    """
    # each allergen gets a list of tuples of all its potential source ingredients
    allergens: DefaultDict[str, Any[List[Set[str]], Set[str]]] = defaultdict(list)
    for recipe in recipes:
        for allergen in recipe.allergens:
            allergens[allergen].append(set(recipe.ingredients))
    # Narrow down to the candidates to ingredients listed in all recipes that list
    # the allergen
    for allergen, candidates in allergens.items():
        allergens[allergen] = set.intersection(*candidates)
    # Use process of elimination to uniquely map each allergen to an ingredient
    num_ambiguous = sum(len(candidates) > 1 for candidates in allergens.values())
    while num_ambiguous:
        unambiguous = [
            allergen for allergen in allergens.keys() if len(allergens[allergen]) == 1
        ]
        for known_allergen in unambiguous:
            known_ingredient = list(allergens[known_allergen])[0]
            for allergen in allergens.keys():
                if allergen == known_allergen:
                    pass
                else:
                    if known_ingredient in allergens[allergen]:
                        allergens[allergen].remove(known_ingredient)
        num_ambiguous = sum(len(candidates) > 1 for candidates in allergens.values())
    # Now just turn the 1 item sets into strings for easier future management
    clean_allergens = {key: value.pop() for key, value in allergens.items()}
    return clean_allergens


def part1(filename: str = "input.txt") -> int:
    """Solve part 1 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    int:
        The answer to part 1
    """
    recipes = read_input(filename)
    allergen_mapper = allergen_to_ingredients(recipes)
    allergen_ingredients = [ingredient for ingredient in allergen_mapper.values()]
    safe_ingredients = 0
    for recipe in recipes:
        for ingredient in recipe.ingredients:
            if ingredient not in allergen_ingredients:
                safe_ingredients += 1
    return safe_ingredients


class AllergenIngredient(NamedTuple):
    """I map an allergen to its associated ingredient."""

    allergen: str
    ingredient: str


def part2(filename: str = "input.txt") -> str:
    """Solve part 2 of the puzzle.

    Parameters
    ----------
    filename: str
        The name of the file in this directory to load

    Returns
    -------
    str:
        The answer to part 2
    """
    recipes = read_input(filename)
    allergen_mapper = allergen_to_ingredients(recipes)

    allergen_tups = sorted(
        [
            AllergenIngredient(allergen, ingredient)
            for allergen, ingredient in allergen_mapper.items()
        ],
        key=lambda x: x.allergen,
    )
    canonical_list = ",".join(ai.ingredient for ai in allergen_tups)
    return canonical_list


if __name__ == "__main__":
    print(part2("example.txt"))
