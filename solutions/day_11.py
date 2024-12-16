import numpy as np
from collections import defaultdict
import time

def test_part_1():
    ans = part_1("test_cases/day_11_test.txt")
    if ans == 55312:
        print("Part 1 test case success!")
    else:
        print(f"Part 1 failed test case, returned {ans}")


def test_part_2():
    ans = part_2("test_cases/day_11_test.txt")
    if ans == 55312:
        print("Part 2 test case success!")
    else:
        print(f"Part 2 failed test case, returned {ans}")

def update_stones(arr):
    # for part 1, doesn't matter where stones are placed
    new_arr = arr.copy()
    idxs_to_remove = []
    for idx, el in enumerate(arr):
        l = len(str(el))
        if el == 0:
            new_arr[idx] = 1
        elif l % 2 == 0:
            idxs_to_remove.append(idx)
            new_arr = np.append(new_arr, [int(str(el)[:int(l/2)]), int(str(el)[int(l/2):])])
        else:
            new_arr[idx] *= 2024
    new_arr = np.delete(new_arr, idxs_to_remove)
    return new_arr


def part_1(file):
    stones = np.genfromtxt(file, dtype=int)
    t = time.time()
    for i in range(25):
        ol = len(stones)
        stones = update_stones(stones)
        # print(f"Stones: {len(stones)}, Ratio: {len(stones)/ol:.3f}")
    print(f"Part 1 time: {time.time() - t}")
    return len(stones)


def update_stones_dict(stones):
    new_stones = stones.copy()
    for key, val in stones.items():
        stones[key] -= val
        new_stones[key] -= val
        l = len(str(key))
        if key == 0:
            new_stones[1] += val
        elif l % 2 == 0:
            key_l = int(str(key)[:int(l/2)])
            key_r = int(str(key)[int(l/2):])
            new_stones[key_l] += val
            new_stones[key_r] += val
        else:
            new_stones[key*2024] += val
    return new_stones


def part_2(file):
    stones = np.genfromtxt(file, dtype=int)
    # generation of stones over 75 steps would break pc, need compressed representation
    # LMAOO this is >100x faster to execute for 25 steps
    # More optimisation is >500x faster for 25 steps
    t = time.time()
    stones_dict = {}
    stones_dict = defaultdict(lambda: 0, stones_dict)
    for s in stones:
        stones_dict[s] = 1
    for i in range(75):
        stones_dict = update_stones_dict(stones_dict)
        print(f"Step {i+1}: {sum(stones_dict.values())} stones")
    print(f"Part 2 time: {time.time() - t}")
    return sum(stones_dict.values())


# test_part_1()
# test_part_2()

#print(part_1("data/day_11_input.txt"))
print(part_2("data/day_11_input.txt"))