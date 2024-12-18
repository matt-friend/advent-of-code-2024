import numpy as np
from anytree import Node, LevelOrderIter, RenderTree, AsciiStyle
import csv
from collections import defaultdict
import sys
import time

print(sys.getrecursionlimit())

sys.setrecursionlimit(2000)


MOVE_MAP = {
        '>': np.array([0, 1]),
        '<': np.array([0, -1]),
        '^': np.array([-1, 0]),
        'v': np.array([1, 0])
    }


def test_part_1():
    ans = part_1("test_cases/day_16_test_a.txt")
    if ans == 7036:
        print("Part 1 test case (a) success!")
    else:
        print(f"Part 1 failed test case (a), returned {ans}")
    ans = part_1("test_cases/day_16_test_b.txt")
    if ans == 11048:
        print("Part 1 test case (b) success!")
    else:
        print(f"Part 1 failed test case (b), returned {ans}")


# def test_part_2():
#     ans = part_2("test_cases/day_12_test_a.txt")
#     if ans == 80:
#         print("Part 2 test case (a) success!")
#     else:
#         print(f"Part 2 failed test case (a), returned {ans}")
#     ans = part_2("test_cases/day_12_test_b.txt")
#     if ans == 436:
#         print("Part 2 test case (b) success!")
#     else:
#         print(f"Part 2 failed test case (b), returned {ans}")
#     ans = part_2("test_cases/day_12_test_c.txt")
#     if ans == 1206:
#         print("Part 2 test case (c) success!")
#     else:
#         print(f"Part 2 failed test case (c), returned {ans}")
#     ans = part_2("test_cases/day_12_test_d.txt")
#     if ans == 236:
#         print("Part 2 test case (d) success!")
#     else:
#         print(f"Part 2 failed test case (d), returned {ans}")
#     ans = part_2("test_cases/day_12_test_e.txt")
#     if ans == 368:
#         print("Part 2 test case (e) success!")
#     else:
#         print(f"Part 2 failed test case (e), returned {ans}")


def is_wall(pos, map):
    return map[pos[0]][pos[1]] == '#'


def is_end(pos, map):
    return map[pos[0]][pos[1]] == 'E'


def next_moves(coords, direction, map):
    next_moves = {}
    for m, c in MOVE_MAP.items():
        new_coords = coords + c
        if is_wall(new_coords, map):
            continue
        # can't turn around
        elif (MOVE_MAP[m] == -MOVE_MAP[direction]).all():
            continue
        else:
            next_moves[m] = new_coords
    return next_moves


def pathfind(node, coords, current_direction, map, mapsize):
    nm = next_moves(coords, current_direction, map)
    map[coords[0]][coords[1]] = current_direction
    for new_direction, new_coords in nm.items():
        cost = node.cost + 1
        if new_direction != current_direction:
            cost += 1000
        # check if new coords not already in path from root
        new_node_name = coordstr(new_coords)
        current_path = [n.name for n in list(node.path)]
        # print(new_node_name, current_path)
        if new_node_name not in current_path:
            if is_end(new_coords, map):
                n = Node(new_node_name, parent=node, cost=cost, cheapest_path=cost, end=True)
                if cost < node.cheapest_path:
                    node.cheapest_path = cost
            else:
                if cost < node.cheapest_path:
                    n = Node(new_node_name, parent=node, cost=cost, cheapest_path=node.cheapest_path, end=False)
                    n = pathfind(n, new_coords, new_direction, map, mapsize)
    return node
    

def generate_paths(start_coords, map, mapsize):
    start_direction = '>'
    # recursive path search
    paths = Node(coordstr(start_coords), cost = 0, cheapest_path = 1e10, end=False)
    paths = pathfind(paths, start_coords, start_direction, map, mapsize)
    # print(f"New tree generated, type {plot_type}:\n {RenderTree(plot, style=AsciiStyle()).by_attr()}")
    return paths


def coordstr(coords):
    # IMPORTANT that this uses 3, was 2 before and caused failure due to coord lookup issues
    return str(coords[0]).zfill(3)+str(coords[1]).zfill(3)


def coord_from_coordstr(coordstr):
    clen = int(len(coordstr)/2)
    return [int(coordstr[:clen]), int(coordstr[clen:])]


def find_reindeer(map):
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == 'S':
                return [y, x]


def get_cheapest_path_cost(paths):
    return min([n.cost for n in LevelOrderIter(paths) if n.end == True])


def print_map(map):
    strmap = [''.join(r) for r in map]
    for idx, r in enumerate(strmap):
        print(f"{str(idx).zfill(3)}: {r}")


def part_1(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        map = []
        instructions = ""
        mapdone = False
        for row in reader:
            if not row:
                mapdone = True
                continue
            if mapdone:
                instructions =  instructions + row[0]
            else:
                map.extend(row)
      
        map = np.array([list(r) for r in map])
        
        print_map(map)

        reindeer_pos = find_reindeer(map)

        t = time.time()

        paths = generate_paths(reindeer_pos, map, len(map))

        print(f"Time taken to generate paths: {time.time() - t}")
        print(f"Distinct paths found: {len([n.cost for n in LevelOrderIter(paths) if n.end == True])}")

        return get_cheapest_path_cost(paths)



def part_2(file):
    pass


# test_part_1()
# test_part_2()

print(part_1("data/day_16_input.txt"))
# print(part_2("data/day_16_input.txt"))