import numpy as np
import csv


def travel_count(map):
    travelled = 0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'X':
                travelled += 1
    return travelled


def find_caret(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == '^':
                return i, j
            
    
def step(cur_y, cur_x, map):
    if cur_y - 1 < 0 or map[cur_y-1][cur_x] != '#':
        cur_y -= 1
    else:
        map = np.rot90(map)
        cur_y, cur_x = find_caret(map)
        cur_y -= 1
    map[cur_y][cur_x] = '^'
    map[cur_y+1][cur_x] = 'X'
    return cur_y, cur_x, map


def part_1():
    with open("data/day_6_input.txt", 'r') as file:
        reader = csv.reader(file)
        map = []
        for row in reader:
            map.extend(row)
        map = np.array([list(r) for r in map])
        
        ypos, xpos = find_caret(map)
        
        out = False
        while not out:
            ypos, xpos, map = step(ypos, xpos, map)
            if ypos < 0:
                out = True
        
        print(travel_count(map))
        

def step_2(rot_y, rot_x, map, map_orientation):
    # go forward
    if rot_y - 1 < 0 or map[rot_y-1][rot_x] != '#':
        rot_y -= 1
        oriented_turn_pos = ()
    # turn
    else:
        oriented_map = np.rot90(map, 4-map_orientation)
        oriented_y, oriented_x = find_caret(oriented_map)
        oriented_turn_pos = (oriented_y, oriented_x)
        map = np.rot90(map)
        rot_y, rot_x = find_caret(map)
        rot_y -= 1
    map[rot_y][rot_x] = '^'
    map[rot_y+1][rot_x] = 'X'
    return rot_y, rot_x, map, oriented_turn_pos


def loop_path(p1, p2, p3, p4):
    ymin = min(p1[0], p2[0], p3[0], p4[0])
    ymax = max(p1[0], p2[0], p3[0], p4[0])
    xmin = min(p1[1], p2[1], p3[1], p4[1])
    xmax = max(p1[1], p2[1], p3[1], p4[1])

    path_els = []
    path_els.extend([(ymin, x) for x in range(xmin, xmax+1)])
    path_els.extend([(ymax, x) for x in range(xmin, xmax+1)])
    path_els.extend([(y, xmin) for y in range(ymin, ymax+1)])
    path_els.extend([(y, xmax) for y in range(ymin, ymax+1)])

    return path_els


def is_obstacle_in_path(map, loop_path):
    is_obstacle = False
    for (y, x) in loop_path:
        if map[y][x] == '#':
            is_obstacle = True
            break
    return is_obstacle
    

def part_2(file):
    with open(file, 'r') as file:
        reader = csv.reader(file)
        map = []
        for row in reader:
            map.extend(row)
        map = np.array([list(r) for r in map])
        
        rot_ypos, rot_xpos = find_caret(map)

        initial_pos = (rot_ypos, rot_xpos)

        turn_pos_list = []
        
        out = False
        while not out:
            map_orientation = len(turn_pos_list) % 4
            rot_ypos, rot_xpos, map, turn_pos = step_2(rot_ypos, rot_xpos, map, map_orientation)
            if turn_pos:
                turn_pos_list.append(turn_pos)
            if rot_ypos < 0:
                out = True

        # re-orient map
        map_orientation = len(turn_pos_list) % 4
        map = np.rot90(map, 4-map_orientation)
        
        turn_pos_list = [initial_pos] + turn_pos_list

        loop_obstacle_list = []

        loop_path_elements = []

        for i in range(len(turn_pos_list) - 2):
            orientation = i % 4
            start = turn_pos_list[i]
            # special case, no final turn
            if i == len(turn_pos_list) - 3:
                # from the previous task we know orientation is 1, too lazy to generalise
                if start[0] > 0:
                    if not is_obstacle_in_path(map, loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (turn_pos_list[i+2][0], start[1]))):
                        loop_path_elements.append(loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (turn_pos_list[i+2][0], start[1])))
                        loop_obstacle_list.append((turn_pos_list[i+2][0], start[1]-1))
            else:
                end = turn_pos_list[i+3]
                print(orientation, start, turn_pos_list[i+1], turn_pos_list[i+2], end)
                if orientation == 0 and end[0] > start[0]:
                    if i != 0:
                        if not is_obstacle_in_path(map, loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (start[0], end[1]))):
                            loop_path_elements.append(loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (start[0], end[1])))
                            loop_obstacle_list.append((start[0]+1, end[1]))
                    # case where we can place obstacle on first set of turns, start point needs an obstacle to the left
                    else:
                        if map[start[0]][start[1]-1] == '#':
                            if not is_obstacle_in_path(map, loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (start[0], end[1]))):
                                loop_path_elements.append(loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (start[0], end[1])))
                                loop_obstacle_list.append((start[0]+1, end[1]))
                elif orientation == 1 and end[1] < start[1]:
                    if not is_obstacle_in_path(map, loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (end[0], start[1]))):
                        loop_path_elements.append(loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (end[0], start[1])))
                        loop_obstacle_list.append((end[0], start[1]-1))
                elif orientation == 2 and end[0] < start[0]:
                    if not is_obstacle_in_path(map, loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (start[0], end[1]))):
                        loop_path_elements.append(loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (start[0], end[1])))
                        loop_obstacle_list.append((start[0]-1, end[1]))
                elif orientation == 3 and end[1] > start[1]:
                    if not is_obstacle_in_path(map, loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (end[0], start[1]))):
                        loop_path_elements.append(loop_path(turn_pos_list[i], turn_pos_list[i+1], turn_pos_list[i+2], (end[0], start[1])))
                        loop_obstacle_list.append((end[0], start[1]+1))
                else:
                    print("nope")

        print(sorted(loop_obstacle_list))
        print(len(loop_obstacle_list))
        loop_obstacle_list = [x for x in loop_obstacle_list if x != initial_pos]
        print(len(loop_obstacle_list))
        loop_obstacle_list = set(loop_obstacle_list)
        print(len(loop_obstacle_list))

        for loop in loop_path_elements:
            for (y,x) in loop:
                map[y][x] = '/'
        
        for (y,x) in turn_pos_list:
            map[y][x] = '+'

        for (y,x) in loop_obstacle_list:
            map[y][x] = 'O'


        map[initial_pos[0]][initial_pos[1]] = '^'

        lmap = [''.join(row) for row in map]
        
        with open("output_test.txt", "w") as txt_file:
            for line in lmap:
                txt_file.write(" ".join(line) + "\n")
        



#part_1()
part_2("test_cases/day_6_test.txt")
#part_2("data/day_6_input.txt")