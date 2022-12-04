"""Advent of code helper functions."""

import traceback
from pathlib import Path
from typing import Generator


def inputs_generator(infile: str) -> Generator[str, None, None]:
    """Yield puzzle inputs line by line.

    Parameters
    ----------
    infile: str
         The name of the input file, should be in the same folder as the calling function

    Returns
    -------
    Generator(str)
         Yields one line of the input at a time

    Raises
    ------
    FileNotFoundError
         If you pass in an input name that does not exist.


    Puzzle inputs must be in the same folder as their puzzle's code.

    This module uses traceback to find the path of the function that called this
    function. We're assuming that whatever called it is a module in a particular
    puzzle day's folder and that puzzle inputs will be in that same folder. This is
    pretty hacky, but it works nicely for this use case, with the minor exception that
    it breaks typeguard, so I guess I don't get runtime type checking.
    """
    stack = traceback.extract_stack()
    basepath = Path(stack[-2].filename).parent
    inpath = basepath / infile
    with open(inpath) as f:
        for line in f.readlines():
            yield line.rstrip()
