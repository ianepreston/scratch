# Day 7: Solution

This was the first one where my code passed the example but not the puzzle input. That's
always a fun milestone. The problem was that the unique identifier for a particular file
or directory is its full path, but I was only using its name as the dictionary key.

I probably didn't need the dictionary and could have set up breadth/depth first search
of all files from the root directory, but the dictionary doesn't take up much additional
space, and for troubleshooting it's really nice to be able to just look up any individual
file or directory by its name.

I got a warning from flake8 that my `build_filetree` function is too complex. I kind of
agree, but breaking out all those individual commands into functions would have meant a
lot more variable passing and typing. There's a fair bit of branching logic and the
function is long, but the branches aren't that crazy and you can follow it fairly easily
from top to bottom so I'm ok with it.

I made a dumb mistake on part 2 where I left the `else` clause in the `min` function as
0 from part 1, which obviously returned 0 every time. After fixing that there were no
real issues with part 2, which is always gratifying as I take it as a sign that I
designed my part 1 solution well.

## Code docs

```{eval-rst}
.. automodule:: advent_ipreston.year_2022.day07.puzzle
   :members:
```
