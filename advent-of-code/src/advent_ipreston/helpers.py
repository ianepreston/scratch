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


    Puzzle inputs should be in the same folder as their puzzle's code, so traceback
    finds the path where that is and then loads the file.
    """
    stack = traceback.extract_stack()
    basepath = Path(stack[-2].filename).parent
    inpath = basepath / infile
    with open(inpath, "r") as f:
        for line in f.readlines():
            yield line
