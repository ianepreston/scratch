def read_passphrases():
    with open("day_04/input.txt", "r") as f:
        return [line.split() for line in f.readlines()]


def part1():
    return sum(len(phrase) == len(set(phrase)) for phrase in read_passphrases())


print(part1())


def anagram(passphrase):
    return len(passphrase) == len(set("".join(sorted(phrase)) for phrase in passphrase))


def part2():
    return sum(anagram(phrase) for phrase in read_passphrases())


print(part2())
