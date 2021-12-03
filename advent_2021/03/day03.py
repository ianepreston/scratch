"""Day 3 of 2021 advent of code."""
from collections import defaultdict
from pathlib import Path
from typing import Dict, Generator, List, Callable


def read_inputs(infile: str) -> Generator[str, None, None]:
    """Read in each binary sequence.

    Parameters
    ----------
    infile: str
        The file to read in (example or puzzle input)

    Yields
    ------
    str
    """
    base_path = Path(__file__).resolve().parent
    in_path = base_path / infile
    with open(in_path, "r") as f:
        for line in f.readlines():
            yield line.strip()


def count_binary(infile: str) -> Dict[int, Dict[int, int]]:
    counter_factory = lambda: defaultdict(int)
    binary_counter = defaultdict(counter_factory)
    for line in read_inputs(infile):
        for position, value in enumerate(line):
            binary_counter[position][int(value)] += 1
    return binary_counter


def get_gamma(infile: str) -> List[int]:
    binary_counter = count_binary(infile)
    cleaned_list = [None for _ in range(len(binary_counter))]
    for key, value in binary_counter.items():
        if value[0] > value[1]:
            cleaned_list[key] = 0
        else:
            cleaned_list[key] = 1
    if any(x is None for x in cleaned_list):
        raise ValueError("You screwed up your cleaned list")
    return cleaned_list


def get_epsilon(gamma_list: List[int]) -> List[int]:
    return [int(x == 0) for x in gamma_list]


def binary_list_to_int(binary_list: List[int]) -> int:
    bin_str = "".join(str(x) for x in binary_list)
    return int(bin_str, 2)


def part1(infile: str) -> int:
    gl = get_gamma(infile)
    el = get_epsilon(gl)
    gamma = binary_list_to_int(gl)
    epsilon = binary_list_to_int(el)
    return gamma * epsilon


def read_in_p2(infile: str) -> List[List[int]]:
    inputs = list()
    for line in read_inputs(infile):
        inputs.append([int(char) for char in line])
    return inputs


def find_most_common(checklist: List[int]) -> int:
    counter = defaultdict(int)
    for i in checklist:
        counter[i] += 1
    if counter[1] >= counter[0]:
        return 1
    else:
        return 0


def find_least_common(checklist: List[int]) -> int:
    counter = defaultdict(int)
    for i in checklist:
        counter[i] += 1
    if counter[0] <= counter[1]:
        return 0
    else:
        return 1


def _recursive_solver(
    list_o_lists: List[List[int]], commonfunc: Callable, position: int = 0
) -> List[int]:
    if len(list_o_lists) == 1:
        return list_o_lists[0]
    check_position = [x[position] for x in list_o_lists]
    keeper_digit = commonfunc(check_position)
    filtered_list = [x for x in list_o_lists if x[position] == keeper_digit]
    updated_position = position + 1
    return _recursive_solver(filtered_list, commonfunc, updated_position)


def oxygen_binlist(infile: str) -> List[int]:
    listolists = read_in_p2(infile)
    return _recursive_solver(listolists, find_most_common)


def co2scrubber_binlist(infile: str) -> List[int]:
    listolists = read_in_p2(infile)
    return _recursive_solver(listolists, find_least_common)


def part2(infile: str):
    oxygenbl = oxygen_binlist(infile)
    co2bl = co2scrubber_binlist(infile)
    oxygenint = binary_list_to_int(oxygenbl)
    co2int = binary_list_to_int(co2bl)
    return oxygenint * co2int


if __name__ == "__main__":
    eg1 = part1("example.txt")
    if eg1 != 198:
        raise ValueError(f"Example expected 198 got {eg1}")
    a1 = part1("input.txt")
    print(a1)
    eg2 = part2("example.txt")
    if eg2 != 230:
        raise ValueError(f"Example expected 230 got {eg2}")
    a2 = part2("input.txt")
    print(a2)
