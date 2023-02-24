"""Treetop Tree House."""

import math

from advent_ipreston.helpers import inputs_generator


class Forest:
    """I'm a grid of trees and their heights."""

    def __init__(self, infile: str) -> None:
        """Load up the forest."""
        forest = [[int(x) for x in line] for line in inputs_generator(infile) if line]
        self.forest = forest
        self.forest_height = len(forest)
        self.forest_width = len(forest[0])

    def find_neighbours(self, y: int, x: int) -> list[list[int]]:
        """Find neighbouring trees to the edge of the forest.

        Parameters
        ----------
        x : int
            x coordinate of the tree
        y : int
            y coordinate of the tree

        Returns
        -------
        list[list[int]]
            List of the heights of neighbouring trees
        """
        left = self.forest[y][:x]
        right = self.forest[y][x + 1 :]
        above = [self.forest[i][x] for i in range(y)]
        below = [self.forest[i][x] for i in range(y + 1, self.forest_height)]
        return [left, right, above, below]

    def is_tallest_tree(self, y: int, x: int) -> bool:
        """Check if this is the tallest tree to at least one edge.

        Parameters
        ----------
        y : int
            y coordinate of the tree to check
        x : int
            x coordinate of the tree to check

        Returns
        -------
        bool
            if the tree is the tallest to at least one edge.
        """
        neighbours: list[list[int]] = self.find_neighbours(y, x)
        if any(len(neighbour) == 0 for neighbour in neighbours):
            return True  # we're at the edge of the forest
        treeheight: int = self.forest[y][x]
        return any(max(neighbour) < treeheight for neighbour in neighbours)

    def count_visible(self) -> int:
        """Count treehouse candidates in the forest.

        Returns
        -------
        int
            Number of treehouse candidates
        """
        visible = 0
        for y in range(self.forest_height):
            for x in range(self.forest_width):
                if self.is_tallest_tree(y, x):
                    visible += 1
        return visible

    def scenic_score(self, y: int, x: int) -> int:
        """Calculate the scenic score of a tree for part 2."""
        left, right, above, below = self.find_neighbours(y, x)
        treeheight: int = self.forest[y][x]
        # Make it so all lists start with the closest tree
        left.reverse()
        above.reverse()
        scores = []
        for neighbour in (left, right, above, below):
            score = 0
            if neighbour:
                for height in neighbour:
                    if height >= treeheight:
                        score += 1
                        break
                    else:
                        score += 1
            scores.append(score)
        return math.prod(scores)

    def max_scenic_score(self) -> int:
        """Find the max scenic score for part 2."""
        return max(
            self.scenic_score(y, x)
            for y in range(self.forest_height)
            for x in range(self.forest_width)
        )


def part1(infile: str) -> int:
    """Solve part 1."""
    return Forest(infile).count_visible()


def part2(infile: str) -> int:
    """Solve part 2."""
    return Forest(infile).max_scenic_score()
