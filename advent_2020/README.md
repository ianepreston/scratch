# advent_2020
[Advent of code challenge 2020](https://adventofcode.com/)

## Installing

tldr: Install pyenv, poetry, and nox. Clone the repo. From within the repo:

```bash
pyenv local 3.9
poetry install
```

Longer answer: I based this on [hypermodern python](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/) so following that setup should help.

## Running

To test, lint etc run ```nox```

To get the answer for a specific day run ```poetry shell``` to get into the virtual environment and then run ```advent [day] [part]``` to get an answer. ```advent --help``` will give more details.

## Reminder for me

VS code won't detect the poetry env automatically. From console run ```poetry shell``` and then ```code .``` to get nice environment integration
