import numpy as np
from anytree import Node, LevelOrderIter, RenderTree, AsciiStyle
import csv
from collections import defaultdict

MOVE_MAP = {
        '>': np.array([0, 1]),
        '<': np.array([0, -1]),
        '^': np.array([-1, 0]),
        'v': np.array([1, 0])
    }


def test_part_1():
    ans = part_1("test_cases/day_15_test_a.txt")
    if ans == 2028:
        print("Part 1 test case (a) success!")
    else:
        print(f"Part 1 failed test case (a), returned {ans}")
    ans = part_1("test_cases/day_15_test_b.txt")
    if ans == 10092:
        print("Part 1 test case (b) success!")
    else:
        print(f"Part 1 failed test case (b), returned {ans}")


def test_part_2():
    ans = part_2("test_cases/day_15_test_b.txt")
    if ans == 9021:
        print("Part 2 test case success!")
    else:
        print(f"Part 2 failed test case, returned {ans}")


def print_map(map):
    strmap = [''.join(r) for r in map]
    for idx, r in enumerate(strmap):
        print(f"{str(idx).zfill(3)}: {r}")


def find_robot(map):
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == '@':
                return [y, x]


def get_new_pos(pos, move):
    return np.array(pos) + MOVE_MAP[move]


def is_wall(pos, map):
    return map[pos[0]][pos[1]] == '#'


def is_empty(pos, map):
    return map[pos[0]][pos[1]] == '.'


def is_box(pos, map):
    return map[pos[0]][pos[1]] == 'O' or is_box_2(pos, map)


def move_robot_from_to(old_pos, new_pos, map):
    map[old_pos[0]][old_pos[1]] == '.'
    map[new_pos[0]][new_pos[1]] == '@'
    return map


def swap_map_items(map, p1, p2):
    p1_item = map[p1[0]][p1[1]]
    p2_item = map[p2[0]][p2[1]]

    # m2 = map.copy()

    map[p1[0]][p1[1]] = p2_item
    map[p2[0]][p2[1]] = p1_item

    return map


def box_interaction(old_pos, new_pos, map, move):
    direction_to_check = MOVE_MAP[move]
    end_of_box_coords = np.array(new_pos)
    interaction_coords = [np.array(new_pos)]
    while is_box(end_of_box_coords, map):
        end_of_box_coords += direction_to_check
        interaction_coords.append(end_of_box_coords.copy())
    if is_wall(end_of_box_coords, map):
        return old_pos, map
    else:
        # move all boxes
        for i in range(len(interaction_coords) - 1, 0, -1):
            map = swap_map_items(map, interaction_coords[i], interaction_coords[i-1])
        # move robot
        map = swap_map_items(map, old_pos, new_pos)
        return new_pos, map


def do_move(pos, map, move):
    new_pos = get_new_pos(pos, move)
    if is_wall(new_pos, map):
        new_pos = pos
    elif is_empty(new_pos, map):
        map = swap_map_items(map, pos, new_pos)
    elif is_box(new_pos, map):
        new_pos, map = box_interaction(pos, new_pos, map, move)
    return new_pos, map
        

def find_all_boxes(map):
    boxes = []
    for i in range(len(map)):
        for j in range(len(map)):
            if is_box([i,j], map):
                boxes.append([i,j])
    return boxes


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
        
        r_pos = find_robot(map)

        for move in instructions:
            r_pos, map = do_move(r_pos, map, move)

        print_map(map)

        gps_sum = 0
        boxes = find_all_boxes(map)
        for b in boxes:
            gps_sum += b[0] * 100 + b[1]
        return gps_sum
    

def get_other_box_coords(pos, map):
    if map[pos[0]][pos[1]] == '[':
        return [pos[0], pos[1] + 1]
    return [pos[0], pos[1] - 1]


def is_visited(coords, interaction_dict):
    for k, v in interaction_dict.items():
        # inefficient type conversion here
        if np.any(np.all(coords == np.array(interaction_dict[k]), axis=1)):
            return True
    return False


def coordstr(coords):
    # IMPORTANT that this uses 3, was 2 before and caused failure due to coord lookup issues
    return str(coords[0]).zfill(3)+str(coords[1]).zfill(3)


def simple_box_interaction(new_pos, map, direction):
    end_of_box_coords = np.array(new_pos)
    interaction_coords = [np.array(new_pos)]
    while is_box(end_of_box_coords, map):
        end_of_box_coords += direction
        interaction_coords.append(end_of_box_coords.copy())
    if is_wall(end_of_box_coords, map):
        return interaction_coords, False
    else:
        return interaction_coords, True


def get_wide_box_interaction_chains_2(interaction_dict, this_chain, this_half_pos, map, direction):
    
    can_move = True
    
    # If new chain, get entire chain and movement status
    if not this_chain:
        this_chain, can_move = simple_box_interaction(this_half_pos, map, direction)
    
    if not can_move:
        return interaction_dict, False
    
    # append to interaction dict
    interaction_dict[coordstr(this_chain[0])] = this_chain

    # need to traverse chain to check for sister chains
    for coord in this_chain[:-1]:
        # if box, initiate chain for other box half if needed
        if is_box(coord, map):
            # get other half
            sister_coord = get_other_box_coords(coord, map)
            sister_can_move = True
            
            # only inititate sister chain if not visited
            if not is_visited(sister_coord, interaction_dict):
                interaction_dict, sister_can_move = get_wide_box_interaction_chains_2(interaction_dict, [], sister_coord, map, direction)
            
        if not sister_can_move:
            return interaction_dict, False      
    
    return interaction_dict, True


def wide_box_interaction(old_pos, new_pos, map, move):
    direction_to_check = MOVE_MAP[move]
    interaction_dict = {}
    interaction_coords = []
    # get all interaction chain coords (vertical slices of boxes)
    interaction_dict, can_move = get_wide_box_interaction_chains_2(interaction_dict, interaction_coords, new_pos, map, direction_to_check)

    if not can_move:
        return old_pos, map
    
    # print(interaction_dict)
    
    for k, interaction in interaction_dict.items():
        # move all boxes
        for i in range(len(interaction) - 1, 0, -1):
            map = swap_map_items(map, interaction[i], interaction[i-1])
        # move robot
    map = swap_map_items(map, old_pos, new_pos)
    return new_pos, map


def box_interaction_2_electric_boogaloo(old_pos, new_pos, map, move):
    if move in ['>', '<']:
        return box_interaction(old_pos, new_pos, map, move)
    else:
        return wide_box_interaction(old_pos, new_pos, map, move)


def is_box_2(pos, map):
    return map[pos[0]][pos[1]] == '[' or map[pos[0]][pos[1]] == ']'


def do_move_2(pos, map, move):
    new_pos = get_new_pos(pos, move)
    if is_wall(new_pos, map):
        new_pos = pos
    elif is_empty(new_pos, map):
        map = swap_map_items(map, pos, new_pos)
    elif is_box_2(new_pos, map):
        new_pos, map = box_interaction_2_electric_boogaloo(pos, new_pos, map, move)
    return new_pos, map


def find_all_boxes_2(map):
    boxes = []
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == '[':
                boxes.append([i,j])
    return boxes

def check_all_boxes_valid(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == '[' and map[i][j+1] != ']':
                return False
            if map[i][j] == ']' and map[i][j-1] != '[':
                return False
    return True


def part_2(file):
    # this took way too long
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

        # print_map(map)

        newmap = []
        for i in range(len(map)):
            new_row = ''
            for j in range(len(map)):
                if is_wall([i,j], map):
                    new_row = new_row + '##'
                elif is_box([i,j], map):
                    new_row = new_row + '[]'
                elif is_empty([i,j], map):
                    new_row = new_row + '..'
                else:
                    new_row = new_row + '@.'
            newmap.append(new_row)
        
        map = np.array([list(r) for r in newmap])

        print_map(map)
        
        r_pos = find_robot(map)

        for idx, move in enumerate(instructions):   
            # print(idx)
            # last_map = map.copy()         
            r_pos, map = do_move_2(r_pos, map, move)
            # if not check_all_boxes_valid(map):
            #     print_map(last_map)
            #     print(idx, move)
            #     break

        print_map(map)

        gps_sum = 0
        boxes = find_all_boxes_2(map)
        for b in boxes:
            gps_sum += b[0] * 100 + b[1]
        return gps_sum

# test_part_1()
# test_part_2()

# print(part_1("data/day_15_input.txt"))
print(part_2("data/day_15_input.txt"))