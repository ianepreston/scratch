EX = (0, 2, 7, 0)
IN = (5, 1, 10, 0, 1, 7, 13, 14, 3, 12, 8, 10, 7, 12, 0, 6)


def ind_max(iter):
    max_num = max(iter)
    for i, num in enumerate(iter):
        if num == max_num:
            return i, max_num


def distribute(iter):
    size = len(iter)
    i, max_num = ind_max(iter)
    even = max_num // size
    odd = max_num % size
    iter = list(iter)
    iter[i] = 0
    iter = [num + even for num in iter]
    for _ in range(odd):
        if i == size - 1:
            i = 0
        else:
            i += 1
        iter[i] += 1
    return tuple(iter)


def part1(iter):
    steps = 0
    banks = set()
    while True:
        if iter not in banks:
            banks.add(iter)
            iter = distribute(iter)
            steps += 1
        else:
            return steps, iter


step, bank = part1(EX)
assert step == 5
assert bank == (2, 4, 1, 2)
step, state = part1(IN)
print(step)
step2, state2 = part1(state)
print(step2)

