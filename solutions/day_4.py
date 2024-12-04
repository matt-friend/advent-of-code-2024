import numpy as np
import csv
import re


def xmas_vh_search(grid):
    count = 0
    for row in grid:
        count += len(re.findall(r'XMAS', row))
        count += len(re.findall(r'SAMX', row)) 
    return count


def xmas_diag_search_b(grid):
    count = 0
    # top left -> bottom right diag, lower triangle
    for i in range(len(grid)):
        search_str = ""
        for j,k in zip(range(i, len(grid)), range(len(grid)-i)):
            search_str += (grid[j][k])
        count += len(re.findall(r'XMAS', search_str))
        count += len(re.findall(r'SAMX', search_str))
    # top left -> bottom right diag, upper triangle (not including main diagonal)
    for i in range(1, len(grid)):
        search_str = ""
        for j,k in zip(range(len(grid)-i), range(i, len(grid))):
            search_str += (grid[j][k])   
        count += len(re.findall(r'XMAS', search_str))
        count += len(re.findall(r'SAMX', search_str))
    return count


def is_grid_mas_x(grid):
    gridstr = ""
    for s in grid:
        gridstr += s
    possible = ["M.S.A.M.S",
                "M.M.A.S.S",
                "S.M.A.S.M",
                "S.S.A.M.M"]
    posmatch = [0,2,4,6,8]
    for p in possible:
        match = True
        for q in posmatch:
            if gridstr[q] != p[q]:
                match = False
        if match == True:
           return match
    return False


def find_mas_x_count(grid):
    count = 0
    for i in range(len(grid) - 2):
        for j in range(len(grid) - 2):
            mas_grid = []
            for k in range(3):
                mas_grid.append(grid[i+k][j:j+3])
            count += is_grid_mas_x(mas_grid)
    return count


def part_1():
    with open("data/day_4_input.txt", 'r') as file:
        count = 0
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.extend(row)
        data_rot = list(reversed([''.join(s) for s in zip(*data)]))
        for d in [data, data_rot]:
            count += xmas_vh_search(d)
            count += xmas_diag_search_b(d)
        print(count)
        

def part_2():
    with open("data/day_4_input.txt", 'r') as file:
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.extend(row)
        print(find_mas_x_count(data))
        
part_1()
part_2()
