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


def test_part_2():
    ans = part_2("test_cases/day_16_test_a.txt")
    if ans == 45:
        print("Part 2 test case (a) success!")
    else:
        print(f"Part 2 failed test case (a), returned {ans}")
    ans = part_2("test_cases/day_16_test_b.txt")
    if ans == 64:
        print("Part 2 test case (b) success!")
    else:
        print(f"Part 2 failed test case (b), returned {ans}")


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
        prev[pos] = []
        unvisited[pos] = True
    
    dist[start] = 0

    while len(unvisited) > 0:
        unvisited_dist = dict((pos, dist[pos]) for pos in unvisited.keys())
        current_node = sorted(unvisited_dist.items(), key=lambda kv: kv[1])[0][0]
        
        del unvisited[current_node]

        neighbours = adjacency_dict[current_node]
        for n in [v for v in neighbours if v[0] in unvisited]:
            temp_dist = dist[current_node] + n[1]
            # added this to account for multiple paths of same cost
            if temp_dist == dist[n[0]]:
                prev[n[0]].append(current_node)
            if temp_dist < dist[n[0]]:
                dist[n[0]] = temp_dist
                prev[n[0]] = [current_node]

    return dist, prev


def coordstr(coords):
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

        cost, _ = djikstra(map, reindeer_pos)
        end = find_end(map)
        min_cost = np.inf
        for d in MOVE_MAP.keys():
            c = coordstr(end) + d
            if cost[c] < min_cost:
                min_cost = cost[c]

        print(f"Time taken for search: {time.time() - t}")

        return min_cost
    

def is_start(pos, map):
    return map[pos[0]][pos[1]] == 'S'


def get_next_els(prevs, cost, coord, map):
    path_els = [coord]
    if is_start(coord_from_coordstr(coord[:-1]), map):
        return path_els
    for el in prevs[coord]:
        path_els.extend(get_next_els(prevs, cost, el, map))
    return path_els


def find_path_els(prevs, cost, end_coord, map):
    print(prevs[end_coord])
    on_path = [end_coord]
    for el in prevs[end_coord]:
        on_path.extend(get_next_els(prevs, cost, el, map))
    return on_path


def part_2(file):
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

        cost, prevs = djikstra(map, reindeer_pos)
        end = find_end(map)
        end_pos = []

        min_cost = np.inf
        for d in MOVE_MAP.keys():
            c = coordstr(end) + d
            if cost[c] <= min_cost:
                min_cost = cost[c]

        for d in MOVE_MAP.keys():
            c = coordstr(end) + d
            if cost[c] == min_cost:
                end_pos.append(c)

        on_min_path = []
        for pos in end_pos:
            on_path = find_path_els(prevs, cost, pos, map)
            on_min_path.extend(on_path)

        on_min_path = set([x[:-1] for x in on_min_path])

        for el in on_min_path:
            c = coord_from_coordstr(el)
            map[c[0]][c[1]] = '0'
        
        print_map(map)
        print(f"Time taken for search: {time.time() - t}")

        return len(on_min_path)


test_part_1()
test_part_2()

# part 1/2 takes ~5m to run for my laptop
print(part_1("data/day_16_input.txt"))
print(part_2("data/day_16_input.txt"))