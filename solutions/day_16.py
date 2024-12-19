import numpy as np
from anytree import Node, LevelOrderIter, RenderTree, AsciiStyle
import csv
from collections import defaultdict
import sys
import time

# print(sys.getrecursionlimit())

# sys.setrecursionlimit(2501)


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


def pathfind(node, coords, current_direction, map, mapsize, cheapest_path):
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
        if new_node_name not in current_path and len(current_path) < 2500:
            if is_end(new_coords, map):
                n = Node(new_node_name, parent=node, cost=cost, end=True)
                if cost < cheapest_path:
                    cheapest_path = cost
                    print(cheapest_path)
            else:
                if cost < cheapest_path:
                    n = Node(new_node_name, parent=node, cost=cost, end=False)
                    n, new_cheapest_path = pathfind(n, new_coords, new_direction, map, mapsize, cheapest_path)
                    if new_cheapest_path < cheapest_path:
                        cheapest_path = new_cheapest_path
                        print(cheapest_path)
    return node, cheapest_path
    

def generate_paths(start_coords, map, mapsize):
    start_direction = '>'
    cheapest_path = 1e7
    # recursive path search
    paths = Node(coordstr(start_coords), cost = 0, end=False)
    paths, cheapest_path = pathfind(paths, start_coords, start_direction, map, mapsize, cheapest_path)
    # print(f"New tree generated, type {plot_type}:\n {RenderTree(plot, style=AsciiStyle()).by_attr()}")
    return paths


def create_adjacency_dict(map):
    adjacency_dict = defaultdict(list)
    directions = MOVE_MAP.keys()
    for i in range(1, len(map)-1):
        for j in range(1, len(map)-1):
            if is_wall([i,j], map):
                continue
            for d in directions:
                key = coordstr([i,j]) + d
                nm = next_moves([i,j], d, map)
                for m, nc in nm.items():
                    cost = 1
                    if m != d:
                        cost += 1000
                    next_key = coordstr(nc) + m
                    adjacency_dict[key].append((next_key ,cost))
    return adjacency_dict
                    

def djikstra(map, start_pos):
    adjacency_dict = create_adjacency_dict(map)
    start = coordstr(start_pos) + '>'
    dist = {}
    prev = {}
    unvisited = {}
    for pos in adjacency_dict.keys():
        dist[pos] = np.inf
        prev[pos] = -1
        unvisited[pos] = True

    print(adjacency_dict['139001>'])
    
    dist[start] = 0

    while len(unvisited) > 0:
        unvisited_dist = dict((pos, dist[pos]) for pos in unvisited.keys())
        current_node = sorted(unvisited_dist.items(), key=lambda kv: kv[1])[0][0]
        
        del unvisited[current_node]

        neighbours = adjacency_dict[current_node]
        for n in [v for v in neighbours if v[0] in unvisited]:
            temp_dist = dist[current_node] + n[1]
            if temp_dist < dist[n[0]]:
                dist[n[0]] = temp_dist
                prev[n[0]] = current_node

    return dist, prev


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
            
def find_end(map):
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == 'E':
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
        
        print(map.shape)
        print_map(map)

        reindeer_pos = find_reindeer(map)
        print(reindeer_pos)

        t = time.time()

        # paths = generate_paths(reindeer_pos, map, len(map))

        cost, _ = djikstra(map, reindeer_pos)
        end = find_end(map)
        min_cost = np.inf
        for d in MOVE_MAP.keys():
            c = coordstr(end) + d
            if cost[c] < min_cost:
                min_cost = cost[c]

        print(f"Time taken to generate paths: {time.time() - t}")
        # print(f"Distinct paths found: {len([n.cost for n in LevelOrderIter(paths) if n.end == True])}")

        return min_cost



def part_2(file):
    pass


test_part_1()
# test_part_2()

print(part_1("data/day_16_input.txt"))
# print(part_2("data/day_16_input.txt"))