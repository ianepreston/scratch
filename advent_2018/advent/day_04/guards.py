import datetime as dt
from collections import namedtuple, Counter

InputLine = namedtuple("InputLine", ["date", "entry"])

file = "input.txt"
with open(file, "r") as f:
    lines = []
    for line in f.readlines():
        cleaned = line.split("] ")
        date_str = cleaned[0].replace("[", "")
        date = dt.datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        text = cleaned[1]
        entry = InputLine(date, text)
        lines.append(entry)

lines.sort()

for index, line in enumerate(lines):
    if line.entry.startswith("Guard") & index != 0:
        assert lines[index -1].entry.startswith("wakes")
print("our assumption is correct!")

