import numpy as np
import csv
import itertools
from collections import defaultdict


def test_part_1():
    ans = part_1("test_cases/day_8_test.txt")
    if ans == 14:
        print("Part 1 test case success!")
    else:
        print(f"Part 1 failed test case, returned {ans}")


def test_part_2():
    ans = part_2("test_cases/day_8_test.txt")
    if ans == 34:
        print("Part 2 test case success!")
    else:
        print(f"Part 2 failed test case, returned {ans}")


def add_to_antenna_dict(d, i, j, item):
    if item != '.':
        if item in d:
            d[item].append((i,j))
        else:
            d[item] = [(i,j)]
    return d


def build_antenna_dict(map):
    antenna_dict = {}
    for i in np.arange(len(map)):
        for j in np.arange(len(map[0])):
            antenna_dict = add_to_antenna_dict(antenna_dict, i, j, map[i][j])
    return antenna_dict


def part_1(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        map = []
        for row in reader:
            map.extend(row)
        map_size = len(map)    
                
        ad = build_antenna_dict(map)

        antinode_counts = {}
        antinode_counts = defaultdict(lambda:0, antinode_counts)

        for key in ad.keys():
            if len(ad[key]) == 1:
                continue
            pairlist = itertools.combinations(np.arange(len(ad[key])), 2)
            for a1, a2 in pairlist:
                y1 = ad[key][a1][0]
                x1 = ad[key][a1][1]
                y2 = ad[key][a2][0]
                x2 = ad[key][a2][1]
                an1y = 2*y1 - y2
                an1x = 2*x1 - x2
                an2y = 2*y2 - y1
                an2x = 2*x2 - x1
                if 0 <= an1y <= map_size - 1 and 0 <= an1x <= map_size - 1:
                    antinode_counts[(an1y, an1x)] += 1
                if 0 <= an2y <= map_size - 1 and 0 <= an2x <= map_size - 1:
                    antinode_counts[(an2y, an2x)] += 1
        return len(antinode_counts.keys())
    

def find_valid_antinodes(mapsize, y1, x1, y2, x2):
    valids = [(y1, x1), (y2, x2)]

    ydiff = y2-y1
    xdiff = x2-x1

    newx = x1 - xdiff
    newy = y1 - ydiff

    while 0 <= newy <= mapsize - 1 and 0 <= newx <= mapsize - 1:
        valids.append((newy, newx))
        newx -= xdiff
        newy -= ydiff
    
    newx = x2 + xdiff
    newy = y2 + ydiff

    while 0 <= newy <= mapsize - 1 and 0 <= newx <= mapsize - 1:
        valids.append((newy, newx))
        newx += xdiff
        newy += ydiff

    return valids


def part_2(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        map = []
        for row in reader:
            map.extend(row)
        map_size = len(map)    
                
        ad = build_antenna_dict(map)

        antinode_counts = {}
        antinode_counts = defaultdict(lambda:0, antinode_counts)

        for key in ad.keys():
            if len(ad[key]) == 1:
                continue
            pairlist = itertools.combinations(np.arange(len(ad[key])), 2)
            for a1, a2 in pairlist:
                y1 = ad[key][a1][0]
                x1 = ad[key][a1][1]
                y2 = ad[key][a2][0]
                x2 = ad[key][a2][1]

                valid_antinodes = find_valid_antinodes(map_size, y1, x1, y2, x2)

                for an in valid_antinodes:
                    antinode_counts[an] += 1

        return len(antinode_counts.keys())


test_part_1()
test_part_2()

print(part_1("data/day_8_input.txt"))
print(part_2("data/day_8_input.txt"))