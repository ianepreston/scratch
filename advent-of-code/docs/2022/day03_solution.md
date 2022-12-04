# Day 3: Solution

Most of the challenge of this one came from figuring out the generator of generators.
I'm still not sure my checking on the length of the tuple I get from the first generator
is the right way to go. If I didn't do it I got runtime errors when I ran out of items,
although it seemed to go through all elements first, so I'm not sure why the generator
wasn't exhausted. From some googling it seems like `while` and generators aren't the
best of friends and they expect `for` loops so maybe this solution was ok.

## Code docs

```{eval-rst}
.. automodule:: advent_ipreston.year_2022.day03.puzzle
   :members:
```
