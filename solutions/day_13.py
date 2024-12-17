import numpy as np
from anytree import Node, LevelOrderIter, RenderTree, AsciiStyle
import csv
from collections import defaultdict
import re
import math


def test_part_1():
    ans = part_1("test_cases/day_13_test.txt")
    if ans == 480:
        print("Part 1 test case success!")
    else:
        print(f"Part 1 failed test case, returned {ans}")


def part_1(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        games = []
        current_game_nums = []
        for idx, row in enumerate(reader):
            r = ''.join(row)
            nums = re.findall(r'[+=](\d+)', r)
            if idx % 4 < 3:
                current_game_nums.extend(nums)
            if idx % 4 == 2:
                games.append(list(map(int, current_game_nums)))
                current_game_nums = []

        cost = 0
        for g in games:
            A = np.array([[g[0], g[2]], [g[1], g[3]]])
            B = np.array([[g[4]], [g[5]]])
            X = np.matmul(np.linalg.inv(A), B)

            a_count = X[0][0]
            b_count = X[1][0]
            
            # print(f"\nNew game\nA: {a_count}, B: {b_count}")
            # print(math.isclose(a_count, round(a_count)), math.isclose(b_count, round(b_count)))

            if not math.isclose(a_count, round(a_count)) or not math.isclose(b_count, round(b_count)):
                continue
            if round(a_count) < 0 or round(a_count) > 100 or round(b_count) < 0 or round(b_count) > 100:
                continue
            else:
                # print(f"Good numbers: A: {round(a_count)}, B: {round(b_count)}")
                cost += round(a_count) * 3
                cost += round(b_count)
        return cost
            

def part_2(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        games = []
        current_game_nums = []
        for idx, row in enumerate(reader):
            r = ''.join(row)
            nums = re.findall(r'[+=](\d+)', r)
            if idx % 4 < 3:
                current_game_nums.extend(nums)
            if idx % 4 == 2:
                games.append(list(map(int, current_game_nums)))
                current_game_nums = []

        ERR_CONST = 10000000000000
        cost = 0
        for g in games:
            A = np.array([[g[0], g[2]], [g[1], g[3]]])
            B = np.array([[g[4] + ERR_CONST], [g[5] + ERR_CONST]])
            X = np.matmul(np.linalg.inv(A), B)

            a_count = X[0][0]
            b_count = X[1][0]
            
            # print(f"\nNew game\nA: {a_count}, B: {b_count}, Prize: {B[0][0], B[1][0]}")
            # print(math.isclose(a_count, round(a_count)), math.isclose(b_count, round(b_count)))

            if not math.isclose(a_count, round(a_count), rel_tol=1/ERR_CONST) or not math.isclose(b_count, round(b_count), rel_tol=1/ERR_CONST):
                continue
            if round(a_count) < 0 or round(b_count) < 0:
                continue
            else:
                # print(f"Good numbers: A: {round(a_count)}, B: {round(b_count)}")
                cost += round(a_count) * 3
                cost += round(b_count)
        return cost
    


test_part_1()

print(part_1("data/day_13_input.txt"))
print(part_2("data/day_13_input.txt"))