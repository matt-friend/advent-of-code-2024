import numpy as np
from anytree import Node, LevelOrderIter, RenderTree, AsciiStyle
import csv


def test_part_1():
    ans = part_1("test_cases/day_12_test_a.txt")
    if ans == 140:
        print("Part 1 test case (a) success!")
    else:
        print(f"Part 1 failed test case (a), returned {ans}")
    ans = part_1("test_cases/day_12_test_b.txt")
    if ans == 772:
        print("Part 1 test case (b) success!")
    else:
        print(f"Part 1 failed test case (b), returned {ans}")
    ans = part_1("test_cases/day_12_test_c.txt")
    if ans == 1930:
        print("Part 1 test case (c) success!")
    else:
        print(f"Part 1 failed test case (c), returned {ans}")


def test_part_2():
    ans = part_2("test_cases/day_12_test_a.txt")
    if ans == 80:
        print("Part 2 test case (a) success!")
    else:
        print(f"Part 2 failed test case (a), returned {ans}")
    ans = part_2("test_cases/day_12_test_b.txt")
    if ans == 436:
        print("Part 2 test case (b) success!")
    else:
        print(f"Part 2 failed test case (b), returned {ans}")
    ans = part_2("test_cases/day_12_test_c.txt")
    if ans == 1206:
        print("Part 2 test case (c) success!")
    else:
        print(f"Part 2 failed test case (c), returned {ans}")
    ans = part_2("test_cases/day_12_test_d.txt")
    if ans == 236:
        print("Part 2 test case (d) success!")
    else:
        print(f"Part 2 failed test case (d), returned {ans}")
    ans = part_2("test_cases/day_12_test_d.txt")
    if ans == 368:
        print("Part 2 test case (e) success!")
    else:
        print(f"Part 2 failed test case (e), returned {ans}")



def next_coords(coords, plot_type, map, mapsize):
    moves = [[-1,0],[1,0],[0,-1],[0,1]]

    next_coords = []
    # search 4 edges
    # print(f"Coords of current position: {coords}")
    for m in moves:
        new_coords = coords + m
        if min(new_coords) < 0 or max(new_coords) == mapsize:
            continue
        elif map[new_coords[0]][new_coords[1]] != plot_type:
            continue
        else:
            # print(f"Valid new area coordinates: {new_coords}")
            next_coords.append(new_coords)

    return next_coords


def get_fencing(coords, plot_type, map, mapsize):
    moves = [[-1,0],[1,0],[0,-1],[0,1]]
    possible_next_coords = [coords + m for m in moves]
    # print(f"Calculating fencing. Bordering coords: {possible_next_coords}")
    valid_moves = [m for m in moves if not (min(coords+m) < 0 or max(coords+m) == mapsize)]
    # print(f"Valid moves: {valid_moves}")

    fencing = 4 - len(valid_moves)
    for m in valid_moves:
        nc = coords + m
        # print(nc)

        if map[nc[0]][nc[1]] != plot_type:
            fencing += 1

    return fencing


def plotfind(node, plot_root, plot_type, coords, map, mapsize):
    nc = next_coords(coords, plot_type, map, mapsize)
    # print(f"Plot status: \n{RenderTree(plot_root, style=AsciiStyle()).by_attr()}")
    # print(f"Searching for plot areas adjacent to {coords}. Plot areas already in tree: {found_plot}\n Possible next areas: {nc}")
    for c in nc:
        # only add to plot tree if not already in tree
        # need to recalculate this list for each new coord due to possible plot growth between iterations
        found_plot = [node.name for node in LevelOrderIter(plot_root)]
        if coordstr(c) not in found_plot:
            n = Node(coordstr(c), parent=node, fencing=get_fencing(c, plot_type, map, mapsize))
            n = plotfind(n, plot_root, plot_type, c, map, mapsize)
    return node
    

def generate_plot(start_coords, map, mapsize):
    # recursive path search
    plot_type = map[start_coords[0]][start_coords[1]]
    plot = Node(coordstr(start_coords), fencing=get_fencing(start_coords, plot_type, map, mapsize))
    plot = plotfind(plot, plot, plot_type, start_coords, map, mapsize)
    print(f"New tree generated, type {plot_type}:\n {RenderTree(plot, style=AsciiStyle()).by_attr()}")
    return plot


def coordstr(coords):
    # IMPORTANT that this uses 3, was 2 before and caused failure due to coord lookup issues
    return str(coords[0]).zfill(3)+str(coords[1]).zfill(3)


def get_total_cost(plots, map):
    total_cost = 0
    for p in plots:
        area = 0
        fencing = 0
        for node in LevelOrderIter(p):
            area += 1
            fencing += node.fencing
        #print(f"Plot type: {map[int(p.name[:3])][int(p.name[3:])]}, Area: {area}, Fencing: {fencing}, Cost: {area*fencing}")
        total_cost += area * fencing
    return total_cost


def part_1(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        map = []
        for row in reader:
            map.extend(row)
        
        print(len(map), len(map[0]))

        plots = []
        covered_coords = []
        for y in range(len(map)):
            for x in range(len(map)):
                # print(f"Looking at coords {y}, {x}")
                # print(f"Coords covered so far: {covered_coords}")
                if coordstr([y, x]) not in covered_coords:
                    p = generate_plot(np.array([y, x]), map, len(map))
                    plots.append(p)
                    covered_coords.extend([node.name for node in LevelOrderIter(p)])
        
        cost = get_total_cost(plots, map)

        return cost


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
# test_part_2()

print(part_1("data/day_12_input.txt"))
# print(part_2("data/day_12_input.txt"))