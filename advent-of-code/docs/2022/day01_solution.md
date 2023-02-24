# Day 1: Solution

The simpler way to do this one would have been to read the whole input in as a list
of lists, use a list comprehension to sum the inner lists, and then sort it and return
the last (part 1) or sum of last 3 (part 2) elements. For this size of list that would
have worked no problem. In theory if this were a really big list you could run into
memory problems. Instead for my solution I tracked the biggest (or biggest 3) values
I'd seen so far, and updated them whenever I saw a bigger one. It took a little more
coding and it might actually be slower on a list this size, but it was fun to think
about how to work that through.

## Code docs

```{eval-rst}
.. automodule:: advent_ipreston.year_2022.day01.puzzle
   :members:
```
