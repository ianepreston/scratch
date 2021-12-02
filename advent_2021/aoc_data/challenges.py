import datetime as dt
from os import getenv
from pathlib import Path
from aocd.get import get_data

today = dt.date.today()
year = 2021
max_day = today.day + 1

session = getenv("AOC_SESSION")
base = Path("/data")
for day in range(1, max_day):
    input_path = base / f"{day}".zfill(2)
    input_path.mkdir(parents=True, exist_ok=True)
    input_file = input_path / "input.txt"
    if not input_file.exists():
        print(f"Getting input for year {year}, day {day}")
        puzzle_input = get_data(session=session, day=day, year=year)
        with open(input_file, "w") as file:
            file.write(puzzle_input)
