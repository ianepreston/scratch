"""No space left on device."""
from dataclasses import dataclass
from dataclasses import field
from typing import Optional

from advent_ipreston.helpers import inputs_generator


@dataclass
class File:
    """I'm a file (in the Unix sense, so I might be a directory too)."""

    name: str
    children: list["File"] = field(default_factory=list)
    individual_size: int = 0
    parent: Optional["File"] = None

    @property
    def size(self) -> int:
        """Size of the file itself or all subfiles if it's a directory."""
        if self.children:
            return sum(child.size for child in self.children)
        else:
            return self.individual_size

    @property
    def fullpath(self) -> str:
        """Full path of the file up to the root dir."""
        if self.parent:
            return f"{self.parent.fullpath}/{self.name}"
        else:
            return self.name


def build_filetree(infile: str) -> dict[str, File]:  # noqa: C901
    """Map all the files we've discovered."""
    files: dict[str, File] = dict()
    cwd: File = File("/")
    files["/"] = cwd
    for line in inputs_generator(infile):
        if line.startswith("$"):
            if line.startswith("$ cd"):
                filename: str = line.replace("$ cd ", "").rstrip()
                if filename == "..":
                    if cwd.parent is None:
                        raise RuntimeError(
                            f"Trying to move up from {cwd.name} with no known parent"
                        )
                    else:
                        cwd = cwd.parent
                elif filename == "/":
                    cwd = files["/"]
                else:
                    new_file = File(filename, parent=cwd)
                    if new_file.fullpath not in files.keys():
                        files[new_file.fullpath] = new_file
                    cwd = files[new_file.fullpath]
        else:
            if line.startswith("dir "):
                filename = line.replace("dir ", "").rstrip()
                if filename not in [child.name for child in cwd.children]:
                    new_file = File(filename, parent=cwd)
                    cwd.children.append(new_file)
                    files[new_file.fullpath] = new_file
            else:
                size, filename = line.split()
                if filename not in [child.name for child in cwd.children]:
                    new_file = File(filename, individual_size=int(size), parent=cwd)
                    cwd.children.append(new_file)
                    files[new_file.fullpath] = new_file
    return files


def part1(infile: str) -> int:
    """Solve part 1."""
    files: dict[str, File] = build_filetree(infile)
    return sum(
        file.size if file.size <= 100_000 and file.children else 0
        for file in files.values()
    )


def part2(infile: str) -> int:
    """Solve part 2."""
    total_disk: int = 70_000_000
    target_free: int = 30_000_000
    files: dict[str, File] = build_filetree(infile)
    current_used: int = files["/"].size
    current_free = total_disk - current_used
    to_free = target_free - current_free
    return min(
        file.size if file.size >= to_free and file.children else total_disk
        for file in files.values()
    )
