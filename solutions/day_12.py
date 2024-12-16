import numpy as np
from anytree import Node, LevelOrderIter, RenderTree, AsciiStyle
import csv
from collections import defaultdict


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
    ans = part_2("test_cases/day_12_test_e.txt")
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
    # print(f"New tree generated, type {plot_type}:\n {RenderTree(plot, style=AsciiStyle()).by_attr()}")
    return plot


def coordstr(coords):
    # IMPORTANT that this uses 3, was 2 before and caused failure due to coord lookup issues
    return str(coords[0]).zfill(3)+str(coords[1]).zfill(3)


def coord_from_coordstr(coordstr):
    clen = int(len(coordstr)/2)
    return [int(coordstr[:clen]), int(coordstr[clen:])]


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


def get_fencing_directional(coords, plot_type, map, mapsize):
    # UP/RIGHT/DOWN/LEFT (clockwise)
    moves = [[-1,0],[0,1],[1,0],[0,-1]]

    fences = []
    # search 4 edges
    for idx, m in enumerate(moves):
        new_coords = coords + m
        if min(new_coords) < 0 or max(new_coords) == mapsize:
            fences.append(idx)
        elif map[new_coords[0]][new_coords[1]] != plot_type:
            fences.append(idx)
    return fences


def plotfind_edges(node, plot_root, plot_type, coords, map, mapsize):
    nc = next_coords(coords, plot_type, map, mapsize)
    # print(f"Plot status: \n{RenderTree(plot_root, style=AsciiStyle()).by_attr()}")
    # print(f"Searching for plot areas adjacent to {coords}. Plot areas already in tree: {found_plot}\n Possible next areas: {nc}")
    for c in nc:
        # only add to plot tree if not already in tree
        # need to recalculate this list for each new coord due to possible plot growth between iterations
        found_plot = [node.name for node in LevelOrderIter(plot_root)]
        if coordstr(c) not in found_plot:
            n = Node(coordstr(c), parent=node, fencing=get_fencing_directional(c, plot_type, map, mapsize))
            n = plotfind_edges(n, plot_root, plot_type, c, map, mapsize)
    return node
    

def generate_plot_with_edges(start_coords, map, mapsize):
    # recursive path search
    plot_type = map[start_coords[0]][start_coords[1]]
    plot = Node(coordstr(start_coords), fencing=get_fencing_directional(start_coords, plot_type, map, mapsize))
    plot = plotfind_edges(plot, plot, plot_type, start_coords, map, mapsize)
    # print(f"New tree generated, type {plot_type}:\n {RenderTree(plot, style=AsciiStyle()).by_attr()}")
    return plot


def get_total_cost_edges(plots, map):
    total_cost = 0
    for p in plots:
        area = 0
        area_edge_dict = {}
        for node in LevelOrderIter(p):
            area += 1
            if node.fencing:
                area_edge_dict[node.name] = node.fencing
        # print(f"\nFinding edges, plot type: {map[int(p.name[:3])][int(p.name[3:])]}")
        # print(area_edge_dict)

        # invert area_edge_dict for easier edgefinding
        edge_area_dict = defaultdict(list)
        for area_coords, edgelist in area_edge_dict.items():
            for edge in edgelist:
                edge_area_dict[edge].append(area_coords)
        # print(dict(edge_area_dict))

        # track all individual edges covered
        covered_area_edges = defaultdict(list)
        # track all full edges
        plot_edges = []

        for area_coords in area_edge_dict.keys():
            for e in area_edge_dict[area_coords]:
                # if already covered, skip
                if e in covered_area_edges[area_coords]:
                    continue

                # otherwise, build edge
                current_edge = [area_coords]
                covered_area_edges[area_coords].append(e)

                # up/down edge (i.e. horizontal edge)
                if e in [0,2]:
                    move = np.array([0,1])
                # left/right edge (i.e. vertical edge)
                else:
                    move = np.array([1,0])

                coords = coord_from_coordstr(area_coords)

                # search for adjacent edges in edge_area_dict
                # print(f"Current edge direction: {e}")
                # print(f"Current edge starting coords: {current_edge}")

                # search in both directions
                for direction in [1, -1]:
                    additive_move = direction * move.copy()
                    while coordstr(coords + additive_move) in edge_area_dict[e]:
                        # add to current edge
                        current_edge.append(coordstr(coords + additive_move))
                        # add to covered edges
                        covered_area_edges[coordstr(coords + additive_move)].append(e)

                        # print(coords)
                        # print(additive_move)
                        # print(f"Edge coord added: {coords + additive_move}")

                        # next move
                        additive_move += direction * move


                # add completed edge to list of edges
                # print(f"Finished edge: {current_edge}")
                plot_edges.append(current_edge)

        # print(f"Plot type: {map[int(p.name[:3])][int(p.name[3:])]}, Edges: {len(plot_edges)}")

        total_cost += area * len(plot_edges)

    return total_cost


def part_2(file):
    # this is going to be inefficient
    with open(file, 'r') as file:
        reader = csv.reader(file)
        map = []
        for row in reader:
            map.extend(row)
        
        plots = []
        covered_coords = []
        for y in range(len(map)):
            for x in range(len(map)):
                # print(f"Looking at coords {y}, {x}")
                # print(f"Coords covered so far: {covered_coords}")
                if coordstr([y, x]) not in covered_coords:
                    p = generate_plot_with_edges(np.array([y, x]), map, len(map))
                    plots.append(p)
                    covered_coords.extend([node.name for node in LevelOrderIter(p)])

        cost = get_total_cost_edges(plots, map)

        return cost


test_part_1()
test_part_2()

print(part_1("data/day_12_input.txt"))
print(part_2("data/day_12_input.txt"))