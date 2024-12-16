import numpy as np
from anytree import Node, LevelOrderGroupIter, RenderTree, AsciiStyle


def test_part_1():
    ans = part_1("test_cases/day_10_test_a.txt")
    if ans == 1:
        print("Part 1 test case (a) success!")
    else:
        print(f"Part 1 failed test case (a), returned {ans}")
    ans = part_1("test_cases/day_10_test_b.txt")
    if ans == 36:
        print("Part 1 test case (b) success!")
    else:
        print(f"Part 1 failed test case (b), returned {ans}")


def test_part_2():
    ans = part_2("test_cases/day_10_test_b.txt")
    if ans == 81:
        print("Part 2 test case success!")
    else:
        print(f"Part 2 failed test case, returned {ans}")


def next_coords(coords, map, mapsize):
    # current height
    h = map[coords[0]][coords[1]]
    moves = [[-1,0],[1,0],[0,-1],[0,1]]

    next_coords = []
    # search 4 edges
    for m in moves:
        new_coords = coords + m
        if min(new_coords) < 0 or max(new_coords) == mapsize:
            continue
        elif map[new_coords[0]][new_coords[1]] != h + 1:
            continue
        else:
            next_coords.append(new_coords)

    return next_coords


def pathfind(node, coords, map, mapsize):
    nc = next_coords(coords, map, mapsize)
    for c in nc:
        n = Node(coordstr(c), parent=node)
        n = pathfind(n, c, map, mapsize)
    return node
    

def get_valid_paths(start_coords, map, mapsize, distinct):
    # recursive path search
    path_tree = Node("trailhead")
    path_tree = pathfind(path_tree, start_coords, map, mapsize)
    # print(RenderTree(path_tree, style=AsciiStyle()).by_attr())
    path_ends = [[node.name for node in children] for children in LevelOrderGroupIter(path_tree)][9]
    if distinct:
        return len(path_ends)
    else:
        return len(set(path_ends))


def coordstr(coords):
    return str(coords[0]).zfill(2)+str(coords[1]).zfill(2)


def part_1(file):
    map = np.genfromtxt(file, dtype=int, delimiter=1)
    # coordinates of all starting points
    trailheads = np.transpose((map == 0).nonzero())
    th_count = len(trailheads)
    th_path_total = 0

    for th in trailheads:
        paths = get_valid_paths(th, map, len(map), distinct=False)
        th_path_total += paths
    
    return th_path_total


def part_2(file):
    map = np.genfromtxt(file, dtype=int, delimiter=1)
    # coordinates of all starting points
    trailheads = np.transpose((map == 0).nonzero())
    th_count = len(trailheads)
    th_path_total = 0

    for th in trailheads:
        paths = get_valid_paths(th, map, len(map), distinct=True)
        th_path_total += paths
    
    return th_path_total


test_part_1()
test_part_2()

print(part_1("data/day_10_input.txt"))
print(part_2("data/day_10_input.txt"))