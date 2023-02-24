"""Advent of code 2021 Day 16 puzzle."""
import math
from pathlib import Path
from typing import Iterator, List


def hex_yielder(infile: str) -> Iterator[str]:
    """Read hex numbers one by one from a file and yield them as binary."""
    inpath = Path(__file__).resolve().parent / infile
    with open(inpath, "r") as f:
        for line in f.readlines():
            for char in line.strip():
                yield char


def bit_yielder(infile: str) -> Iterator[str]:
    """Yield individual bits converted from a stream of hex numbers from a filename."""
    for byte in hex_yielder(infile):
        num = int(byte, 16)
        bytestr = f"{num:04b}"
        for c in bytestr:
            yield c


def subseq_yielder(subseq: List[str]) -> Iterator[str]:
    for c in subseq:
        yield c


def bitseq_to_int(bitseq: List[str]) -> int:
    return int("".join(c for c in bitseq), 2)


def parse_typeid(bitseq: List[str]) -> str:
    typenum = bitseq_to_int(bitseq)
    typedict = {
        0: "sum",
        1: "product",
        2: "minimum",
        3: "maximum",
        4: "literal",
        5: "greater than",
        6: "less than",
        7: "equal to",
    }
    return typedict[typenum]


def parse_literal(bitstream: Iterator[str]) -> int:
    bitseq = []
    # Start counting from the version and type headers
    bitlength = 6
    while True:
        checkbit = next(bitstream)
        for _ in range(4):
            bitseq.append(next(bitstream))
        bitlength += 5
        if checkbit != "1":
            break
    return bitseq_to_int(bitseq)


class Packet:
    def __init__(self, bitstream: Iterator[str]) -> None:
        self.bitstream = bitstream
        self.subpackets = []
        self.version = bitseq_to_int([next(self.bitstream) for _ in range(3)])
        self.typeid = parse_typeid([next(self.bitstream) for _ in range(3)])
        self.literal = None
        self.parse()

    def _parse_subop(self) -> None:
        """
        An operator packet contains one or more packets. To indicate which subsequent
        binary data represents its sub-packets, an operator packet can use one of two
        modes indicated by the bit immediately after the packet header; this is called
        the length type ID

        If the length type ID is 0, then the next 15 bits are a number that represents
        the total length in bits of the sub-packets contained by this packet.
        If the length type ID is 1, then the next 11 bits are a number that represents
        the number of sub-packets immediately contained by this packet.
        """
        lengthid = next(self.bitstream)
        if lengthid == "0":
            length = bitseq_to_int([next(self.bitstream) for _ in range(15)])
            subseq = [next(self.bitstream) for _ in range(length)]
            substream = subseq_yielder(subseq)
            self.subpackets = build_packets(substream)
        else:
            length = bitseq_to_int([next(self.bitstream) for _ in range(11)])
            for _ in range(length):
                try:
                    self.subpackets.append(Packet(self.bitstream))
                except StopIteration:
                    raise RuntimeError("Ran out of data while processing subpacket")

    def parse(self) -> None:
        if self.typeid == "literal":
            self.literal = parse_literal(self.bitstream)
        else:
            self._parse_subop()

    @property
    def version_sum(self) -> int:
        if not self.subpackets:
            return self.version
        else:
            return self.version + sum(sp.version_sum for sp in self.subpackets)

    @property
    def value(self) -> int:
        if self.typeid == "sum":
            val = sum(sp.value for sp in self.subpackets)
        elif self.typeid == "product":
            val = math.prod(sp.value for sp in self.subpackets)
        elif self.typeid == "minimum":
            val = min(sp.value for sp in self.subpackets)
        elif self.typeid == "maximum":
            val = max(sp.value for sp in self.subpackets)
        elif self.typeid == "literal":
            val = self.literal
        elif self.typeid == "greater than":
            if len(self.subpackets) != 2:
                raise RuntimeError(f"GT typeid with {len(self.subpackets)} subpackets")
            else:
                val = int(self.subpackets[0].value > self.subpackets[1].value)
        elif self.typeid == "less than":
            if len(self.subpackets) != 2:
                raise RuntimeError(f"LT typeid with {len(self.subpackets)} subpackets")
            else:
                val = int(self.subpackets[0].value < self.subpackets[1].value)
        elif self.typeid == "equal to":
            if len(self.subpackets) != 2:
                raise RuntimeError(f"ET typeid with {len(self.subpackets)} subpackets")
            else:
                val = int(self.subpackets[0].value == self.subpackets[1].value)
        else:
            raise RuntimeError(f"Unknown typeid {self.typeid}")
        return val


def build_packets(bitstream: Iterator[str]) -> List[Packet]:
    packets = []
    while True:
        try:
            packets.append(Packet(bitstream))
        except StopIteration:
            break
    return packets


def part1(infile: str):
    bitstream = bit_yielder(infile)
    packets = build_packets(bitstream)
    return sum(p.version_sum for p in packets)


def part2(infile: str):
    bitstream = bit_yielder(infile)
    packets = build_packets(bitstream)
    if len(packets) != 1:
        raise RuntimeError(f"Should only have one base packet, found {len(packets)}")
    return packets[0].value


if __name__ == "__main__":
    egs = (
        ("eg1.txt", 16),
        ("eg2.txt", 12),
        ("eg3.txt", 23),
        ("eg4.txt", 31),
    )
    for fname, answer in egs:
        eg = part1(fname)
        if eg != answer:
            raise RuntimeError(f"{fname}: expected {answer}, got {eg}.")
    a1 = part1("input.txt")
    print(f"Part 1: {a1}")
    egs2 = (
        ("eg5.txt", 3),
        ("eg6.txt", 54),
        ("eg7.txt", 7),
        ("eg8.txt", 9),
        ("eg9.txt", 1),
        ("eg10.txt", 0),
        ("eg11.txt", 0),
        ("eg12.txt", 1),
    )
    for fname, answer in egs2:
        eg = part2(fname)
        if eg != answer:
            raise RuntimeError(f"{fname}: expected {answer}, got {eg}.")
    a2 = part2("input.txt")
    print(f"Part 2: {a2}")
