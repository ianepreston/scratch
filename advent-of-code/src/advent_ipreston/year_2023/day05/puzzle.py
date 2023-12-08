"""If you give a seed a fertilizer"""
from dataclasses import dataclass
from typing import List
from typing import NamedTuple
from typing import Optional
from typing import Tuple

from advent_ipreston.helpers import inputs_generator


@dataclass
class Map:
    dest_start: int
    source_start: int
    range_length: int

    @property
    def source_end(self) -> int:
        return self.source_start + self.range_length - 1

    @property
    def dest_end(self) -> int:
        return self.dest_start + self.range_length - 1

    def translate(
        self, othermap: "Map"
    ) -> Tuple[Optional["Map"], Optional[List["Map"]]]:
        """Take the destination of one map and translate it to the destination of this map."""
        in_start = othermap.dest_start
        in_end = othermap.dest_end
        # other is fully in this map
        if in_start >= self.source_start and in_end <= self.source_end:
            out_start = self.dest_start + in_start - self.source_start
            return Map(out_start, in_start, othermap.range_length), None
        # other is fully outside this map
        elif in_end < self.source_start or in_start > self.source_end:
            return None, [othermap]
        # Other starts before this map but ends in it
        elif in_start < self.source_start and in_end <= self.source_end:
            unchanged_range = self.source_start - in_start
            changed_range = in_end - self.source_start + 1
            unchanged_map = Map(in_start, othermap.source_start, unchanged_range)
            changed_map = Map(self.dest_start, othermap.dest_start, changed_range)
            assert (
                changed_map.range_length + unchanged_map.range_length
                == othermap.range_length
            )
            return changed_map, [unchanged_map]
        # Other starts in this map but ends after it
        elif in_start >= self.source_start and in_end > self.source_end:
            unchanged_start = self.source_end + 1
            unchanged_range = in_end - unchanged_start + 1
            changed_range = self.source_end - in_start + 1
            unchanged_map = Map(unchanged_start, othermap.source_start, unchanged_range)
            changed_map = Map(
                self.dest_start + (in_start - self.source_start),
                othermap.dest_start,
                changed_range,
            )
            assert (
                changed_map.range_length + unchanged_map.range_length
                == othermap.range_length
            )
            return changed_map, [unchanged_map]
        # Other starts before this map and ends after it
        else:
            changed_map = Map(self.dest_start, self.source_start, self.range_length)
            pre_range = self.source_start - in_start
            post_range = in_end - (self.source_end)
            pre_map = Map(othermap.dest_start, othermap.source_start, pre_range)
            post_map = Map(self.source_end + 1, othermap.source_start, post_range)
            assert (
                pre_map.range_length + changed_map.range_length + post_map.range_length
                == othermap.range_length
            )
            return changed_map, [pre_map, post_map]


class MapList(NamedTuple):
    sourcename: str
    destname: str
    maps: List[Map]

    def source_to_target(self, othermap: Map) -> List[Map]:
        translated_maps = []
        untranslated_maps = [othermap]
        for map in self.maps:
            still_untranslated_maps = []
            for input_untranslated_map in untranslated_maps:
                translated_map, untranslated_map = map.translate(input_untranslated_map)
                if translated_map:
                    translated_maps.append(translated_map)
                if untranslated_map:
                    still_untranslated_maps.extend(untranslated_map)
            untranslated_maps = still_untranslated_maps
        translated_maps.extend(untranslated_maps)
        return translated_maps


class Input(NamedTuple):
    seeds: List[Map]
    maps: List[MapList]


def parse_seeds(seeds: List[int], part_1: bool = True) -> List[Map]:
    """Parse the seeds into a list of maps."""
    if part_1:
        maps = [Map(seed, 0, 1) for seed in seeds]
    else:
        maps = [
            Map(start, 0, seedrange)
            for start, seedrange in zip(seeds[::2], seeds[1::2])
        ]
    return maps


def parse_inputs(infile: str, part_1: bool = True) -> Input:
    reader = inputs_generator(infile)
    firstline = reader.__next__()
    seeds = parse_seeds(
        [int(i) for i in firstline.replace("seeds: ", "").split()], part_1
    )
    _ = reader.__next__()
    source: str = ""
    dest: str = ""
    maps: List[Map] = []
    maplist: List[MapList] = []
    for line in reader:
        if not line:
            maplist.append(MapList(source, dest, maps))
            source = dest = ""
            maps = []
        elif line[0].isnumeric():
            dest_start, source_start, range_length = [int(i) for i in line.split()]
            maps.append(Map(dest_start, source_start, range_length))
        else:
            cleanline = line.replace("map:", "").strip()
            source, dest = cleanline.split("-to-")
    maplist.append(MapList(source, dest, maps))
    return Input(seeds, maplist)


def part1(input_file: str) -> int:
    """Part 1."""
    inputs = parse_inputs(input_file)
    seeds = inputs.seeds
    for maplist in inputs.maps:
        seeds = [map_ for seed in seeds for map_ in maplist.source_to_target(seed)]
    return min(seed.dest_start for seed in seeds)


def part2(input_file: str) -> int:
    """Part 1."""
    inputs = parse_inputs(input_file, part_1=False)
    seeds = inputs.seeds
    for maplist in inputs.maps:
        seeds = [map_ for seed in seeds for map_ in maplist.source_to_target(seed)]
    return min(seed.dest_start for seed in seeds)


if __name__ == "__main__":  # pragma: no cover
    print(f"Part 1: {part1('puzzle.txt')}")
    print(f"Part 2: {part2('puzzle.txt')}")
