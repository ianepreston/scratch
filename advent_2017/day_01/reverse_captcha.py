from itertools import tee


def file_iterator(file="input.txt"):
    with open(file, "r") as f:
        for line in f.readline():
            for char in line.rstrip():
                yield int(char)


def circular_sum(iterable):
    it1, it2 = tee(iterable)
    it_begin = next(it2, None)
    circular_sum = 0
    for first, second in zip(it1, it2):
        if first == second:
            circular_sum += first
    if it_begin == second:
        circular_sum += it_begin
    return circular_sum


assert circular_sum([1, 1, 2, 2]) == 3
assert circular_sum([1, 1, 1, 1]) == 4
assert circular_sum([1, 2, 3, 4]) == 0
assert circular_sum([9, 1, 2, 1, 2, 1, 2, 9]) == 9
print(circular_sum(file_iterator()))

print("Part 2, need to know the size so I can't be fancy with generators anymore")


def file_list(file="input.txt"):
    with open(file, "r") as f:
        return [int(char) for line in f.readlines() for char in line.rstrip()]


def circular_sum_sequel(num_list):
    circular_sum = 0
    list_len = len(num_list)
    assert list_len % 2 == 0
    mid_len = int(list_len / 2)
    for index, num in enumerate(num_list):
        if index + mid_len >= list_len:
            pointer = index + mid_len - list_len
        else:
            pointer = index + mid_len
        if num == num_list[pointer]:
            circular_sum += num
    return circular_sum


assert circular_sum_sequel([1, 2, 1, 2]) == 6
assert circular_sum_sequel([1, 2, 2, 1]) == 0
assert circular_sum_sequel([1, 2, 3, 4, 2, 5]) == 4
assert circular_sum_sequel([1, 2, 3, 1, 2, 3]) == 12
assert circular_sum_sequel([1, 2, 1, 3, 1, 4, 1, 5]) == 4


print(circular_sum_sequel(file_list()))
