import numpy as np
import csv
import re
import math
from collections import defaultdict


def test_part_1():
    ans = part_1("test_cases/day_14_test.txt", 11, 7)
    if ans == 12:
        print("Part 1 test case success!")
    else:
        print(f"Part 1 failed test case, returned {ans}")


def calc_pos(robots, steps, xdim, ydim):
    for r in robots:
        r[0] = (r[0] + r[2] * steps) % xdim
        r[1] = (r[1] + r[3] * steps) % ydim
    return robots


def calc_q_counts(robots, xdim, ydim):
    qc = [0] * 4
    xmid = int((xdim + 1)/2) - 1
    ymid = int((ydim + 1)/2) - 1
    for r in robots:
        # moving clockwise in quadrants
        if r[0] < xmid and r[1] < ymid:
            qc[0] += 1
        elif r[0] > xmid and r[1] < ymid:
            qc[1] += 1
        elif r[0] > xmid and r[1] > ymid:
            qc[2] += 1
        elif r[0] < xmid and r[1] > ymid:
            qc[3] += 1
    return qc


def draw_robots(robots, xdim, ydim):
    map = np.zeros([ydim, xdim])
    for r in robots:
        map[r[1]][r[0]] += 1
    map = np.array([[str(int(el)) for el in sub] for sub in map])
    map[map == '0'] = '.'
    return map


def part_1(file, x_dim, y_dim):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        robots = []
        for row in reader:
            r = ' '.join(row)
            nums = re.findall(r'(-?\d+)', r)
            robots.append(list(map(int, nums)))
    
    # print(draw_robots(robots, x_dim, y_dim))

    steps = 100
    robots = calc_pos(robots, steps, x_dim, y_dim)

    q_counts = calc_q_counts(robots, x_dim, y_dim)
    print(q_counts)

    # print(draw_robots(robots, x_dim, y_dim))

    return math.prod(q_counts)


def coordstr(coords):
    return str(coords[0]).zfill(3)+str(coords[1]).zfill(3)


def any_stacked_robots(robots):
    d = defaultdict(int)
    for r in robots:
        c = coordstr([r[0], r[1]])
        d[c] += 1
    for k, v in d.items():
        if v > 1:
            return True
    return False


def part_2(file, x_dim, y_dim):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        robots = []
        for row in reader:
            r = ' '.join(row)
            nums = re.findall(r'(-?\d+)', r)
            robots.append(list(map(int, nums)))
    
    steps = 10000
    for i in range(steps):
        robots = calc_pos(robots, 1, x_dim, y_dim)
        # initial assumption was equal numbers of robots in horizontal quadrants, didn't work
        # next assumption was that a pattern would be composed of individual robots (not stacked), worked
        if not any_stacked_robots(robots):
            print(i+1)
            r = draw_robots(robots, x_dim, y_dim)
            with open(f"outputs/day_14/robots_{i+1}.txt", "w") as txt_file:
                for line in r:
                    txt_file.write(" ".join(line) + "\n")
            
    


test_part_1()

# print(part_1("data/day_14_input.txt", 101, 103))
print(part_2("data/day_14_input.txt", 101, 103))