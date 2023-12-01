"""Trebuchet."""
import re
from typing import Dict
from typing import List
from typing import Optional

from advent_ipreston.helpers import inputs_generator


def filter_numbers(instr: str) -> Optional[List[int]]:
	"""Use regular expressions to filter numeric characters.
	
	Parameters
	----------
	instr: str
		A string containing letters and numbers
	
	Returns
	-------
	List[int]
		A list of integers from the input string
	
	Raises
    ------
    ValueError
        If no numbers are found in the input string
	"""
	result = re.findall(r"\d", instr)
	if not result:
		raise ValueError("No numbers found in input string")
	else:
		return result

def part1(infile: str) -> int:
	"""Solve part 1 of the puzzle."""
	result = 0
	for line in inputs_generator(infile):
		numbers = filter_numbers(line)
		result += int(numbers[0] + numbers[-1])
	return result

def word_to_numbers(instr: str) -> str:
	"""Convert a string containing spelled out numbers to a string with the word replaced with a number."""
	word_to_num: Dict[str, str] = {
		"one": "1",
		"two": "2",
		"three": "3",
		"four": "4",
		"five": "5",
		"six": "6",
		"seven": "7",
		"eight": "8",
		"nine": "9",
	}
	nums = list()
	for i in range(len(instr)):
		if instr[i].isnumeric():
			nums.append(instr[i])
		for key in word_to_num.keys():
			if instr[i:i+len(key)] == key:
				nums.append(word_to_num[key])
				break
	return int(nums[0] + nums[-1])

def part2(infile: str) -> int:
	"""Solve part 2 of the puzzle."""
	return sum([word_to_numbers(line) for line in inputs_generator(infile)])


if __name__ == "__main__":  # pragma: no cover
    print(f"Part 1: {part1('puzzle.txt')}")
    print(f"Part 2: {part2('puzzle.txt')}")
