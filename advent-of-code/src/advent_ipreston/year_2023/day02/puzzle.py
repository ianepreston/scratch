"""Cube Conundrum."""
from dataclasses import dataclass
from math import prod
from typing import List

from advent_ipreston.helpers import inputs_generator


@dataclass
class ColorDraw:
    blue: int
    green: int
    red: int

    def is_valid(self, reference: "ColorDraw") -> bool:
        """Compare against a reference ColorDraw object to see if it is valid."""
        return all((self.blue <= reference.blue, self.green <= reference.green, self.red <= reference.red))


REFERENCE_DRAW = ColorDraw(blue=14, green=13, red=12)


@dataclass
class Game:
    number: int
    draws: List[ColorDraw]

    def is_valid(self) -> bool:
        """Check if the game is valid."""
        for draw in self.draws:
            if not draw.is_valid(REFERENCE_DRAW):
                return False
        return True
    
    def min_cubes_power(self) -> int:
        """Return the minimum number of cubes needed to play the game."""
        min_green = max(draw.green for draw in self.draws)
        min_red = max(draw.red for draw in self.draws)
        min_blue = max(draw.blue for draw in self.draws)
        return min_green * min_red * min_blue


def parse_draw(indraw: str) -> ColorDraw:
    """Parse a draw."""
    blues = 0
    greens = 0
    reds = 0
    for pull in indraw.split(","):
        pull = pull.strip()
        num = int(pull.split(" ")[0])
        color = pull.split(" ")[1]
        if color.startswith("b"):
            blues += num
        elif color.startswith("g"):
            greens += num
        elif color.startswith("r"):
            reds += num
    return ColorDraw(blue=blues, green=greens, red=reds)


def parse_game(ingame: str) -> Game:
    """Parse a game."""
    game = Game(number=int(ingame.split(":")[0].replace("Game ", "")), draws=[])
    for indraw in ingame.split(":")[1].split(";"):
        game.draws.append(parse_draw(indraw))
    return game

def part1(infile: str) -> int:
    """Solve part 1 of the puzzle."""
    valid_games = 0
    for ingame in inputs_generator(infile):
        game = parse_game(ingame)
        if game.is_valid():
            valid_games += game.number
    return valid_games

def part2(infile: str) -> int:
    """Solve part 2 of the puzzle."""
    return sum(parse_game(game).min_cubes_power() for game in inputs_generator(infile))


if __name__ == "__main__":  # pragma: no cover
    print(f"Part 1: {part1('puzzle.txt')}")
    print(f"Part 2: {part2('puzzle.txt')}")
