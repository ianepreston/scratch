from dataclasses import dataclass
from collections import Counter

@dataclass
class ElfSquares:
    id: int
    inches_from_left: int
    inches_from_top: int
    width: int
    height: int

    @property
    def start_point(self):
        return (self.inches_from_top + 1, self.inches_from_left + 1)
    
    @property
    def end_point(self):
        return (self.inches_from_top + self.height, self.inches_from_left + self.width)
    
    @property
    def coordinates_list(self):
        coordinates = []
        for x in range(self.start_point[0], self.end_point[0] + 1):
            for y in range(self.start_point[1], self.end_point[1] +1):
                coordinates.append((x, y))
        return coordinates


def read_elf_square(input_claim):
    clean_str = (
        input_claim
        .replace("#", "")
        .replace(" @ ", " ")
        .replace(",", " ")
        .replace(": ", " ")
        .replace("x", " ")
    )
    int_list = [int(c) for c in clean_str.split()]
    elf_square = ElfSquares(*int_list)
    return elf_square

def read_all_elf_squares():
    with open("input.txt", "r") as elf_file:
        elf_squares = [read_elf_square(claim) for claim in elf_file.readlines()]
    return elf_squares 

def count_coordinates(return_counter=False):
    claim_list = read_all_elf_squares()
    counter = Counter()
    for claim in claim_list:
        for elf_square in claim.coordinates_list:
            counter[elf_square] += 1
    if return_counter:
        return counter
    elf_conflicts = 0
    for square_count in counter.values():
        if square_count > 1:
            elf_conflicts += 1
    return elf_conflicts

print(count_coordinates())

def conflict_free_elf_claim():
    conflict_free_elves = []
    elf_claims = read_all_elf_squares()
    coordinates = count_coordinates(return_counter=True)
    for elf_claim in elf_claims:
        coord_list = [coordinates[coord] == 1 for coord in elf_claim.coordinates_list]
        if all(coord_list):
            conflict_free_elves.append(elf_claim)
    assert len(conflict_free_elves) == 1
    return conflict_free_elves[0].id

print(conflict_free_elf_claim())

