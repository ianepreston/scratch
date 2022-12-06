# Day 5: Solution

Input parsing was definitely the trickiest part of this. I had a good idea of how to do
it but got caught on lots of dumb little things like forgetting that `" "` returns
`true` when filtering things for which indices had tower items. All in all I like
how I used pop and the way lists were generated to manage the inputs and the tower.
The double pop I did for the part two solution might have been cleaner as reversing a
list or taking the last `n` elements out of the existing list, but oh well, it
worked well and was fast to write in.

## Code docs

```{eval-rst}
.. automodule:: advent_ipreston.year_2022.day05.puzzle
   :members:
```
