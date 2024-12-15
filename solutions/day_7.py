import numpy as np
import csv
import itertools


def test_part_1():
    ans = part_1("test_cases/day_7_test.txt")
    if ans == 3749:
        print("Part 1 test case success!")
    else:
        print(f"Part 1 failed test case, returned {ans}")


def test_part_2():
    ans = part_2("test_cases/day_7_test.txt")
    if ans == 11387:
        print("Part 2 test case success!")
    else:
        print(f"Part 2 failed test case, returned {ans}")


def do_op(op, num1, num2):
    if op == 0:
        return num1 + num2
    elif op == 1:
        return num1 * num2
    elif op == 2:
        return int(str(num1) + str(num2))
    else:
        return -1


def brute_force(test_val, nums, part=1):
    # takes about 15s for part 2
    op_cases = list(itertools.product(np.arange(part+1), repeat=len(nums)-1))
    for case in op_cases:
        out = nums[0]
        for i in range(1, len(nums)):
            out = do_op(case[i-1], out, nums[i])
        if out == test_val:
            return True
    return False


def get_valid_test_vals(case_list, part):
    valids = []
    for case in case_list:
        if brute_force(case[0], case[1:], part):
            valids.append(case[0])
    return valids


def part_1(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        cases = []
        for row in reader:
            nums = row[0].split(" ")
            nums[0] = nums[0][:-1]
            cases.append(list(map(int, nums)))
        valids = get_valid_test_vals(cases, part=1)
        return sum(valids)


def part_2(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        cases = []
        for row in reader:
            nums = row[0].split(" ")
            nums[0] = nums[0][:-1]
            cases.append(list(map(int, nums)))
        valids = get_valid_test_vals(cases, part=2)
        return sum(valids)


test_part_1()
test_part_2()

print(part_1("data/day_7_input.txt"))
print(part_2("data/day_7_input.txt"))