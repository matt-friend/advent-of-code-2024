import numpy as np
import csv
import itertools
from collections import defaultdict


def test_part_1():
    ans = part_1("test_cases/day_9_test.txt")
    if ans == 1928:
        print("Part 1 test case success!")
    else:
        print(f"Part 1 failed test case, returned {ans}")


def test_part_2a():
    ans = part_2("test_cases/day_9_test.txt")
    if ans == 2858:
        print("Part 2 test case (a) success!")
    else:
        print(f"Part 2 failed test case (a), returned {ans}")

def test_part_2b():
    ans = part_2("test_cases/day_9_test_2.txt")
    if ans == 3462:
        print("Part 2 test case (b) success!")
    else:
        print(f"Part 2 failed test case (b), returned {ans}")


def part_1(file):
    with open(file, 'r') as file:
        disk_map = file.read().replace('\n', '')
        disk_map = list(map(int, disk_map))
        checksum = 0
        disk_data_pointer = 0
        disk_map_bkwd_pntr = len(disk_map) - 1
        for disk_map_fwd_pntr in range(len(disk_map)):
            val = disk_map[disk_map_fwd_pntr]

            if disk_map_fwd_pntr % 2 == 0:
                file_id = int(disk_map_fwd_pntr / 2)
                checksum += sum([file_id * x for x in range(disk_data_pointer, disk_data_pointer + val)])
                disk_data_pointer += val
            else:
                # fill up space working backwards
                gap_space = val
                while gap_space > 0:
                    gap_space -= disk_map[disk_map_bkwd_pntr]
                    file_id = int(disk_map_bkwd_pntr / 2)
                    if gap_space >= 0:
                        checksum += sum([file_id * x for x in range(disk_data_pointer, disk_data_pointer + disk_map[disk_map_bkwd_pntr])])
                        disk_data_pointer += disk_map[disk_map_bkwd_pntr]
                        disk_map_bkwd_pntr -= 2
                    else:
                        remaining_space = disk_map[disk_map_bkwd_pntr] + gap_space
                        checksum += sum([file_id * x for x in range(disk_data_pointer, disk_data_pointer + remaining_space)])
                        disk_data_pointer += remaining_space
                        disk_map[disk_map_bkwd_pntr] -= remaining_space
            # feel like I haven't dealt with an edge case here but it works for part 1 so
            if disk_map_fwd_pntr >= disk_map_bkwd_pntr:
                break

        return checksum
    

def init_gap_table(disk_map):
    gap_pntrs = [-1] * 9

    disk_data_pntr = disk_map[0]
    disk_map_pntr = 1

    while min(gap_pntrs) == -1 and disk_map_pntr < len(disk_map):
        gap = disk_map[disk_map_pntr]    
        for i in range(9):
            if gap > i and gap_pntrs[i] == -1:
                gap_pntrs[i] = disk_data_pntr
        disk_data_pntr += sum(disk_map[disk_map_pntr:disk_map_pntr+2])
        disk_map_pntr += 2
    return gap_pntrs


def find_leftmost_gap_for_size(actual_data, start_pntr, filesize):
    dd_pntr = start_pntr
    current_gap_size = 0
    largest_gap_size = 0
    largest_gap_pntr = 0

    while largest_gap_size < filesize and dd_pntr < len(actual_data):
        # print(f"dd_pntr: {dd_pntr}")
        # print(f"current_gap_size: {current_gap_size}")
        # print(f"largest_gap_size: {largest_gap_size}")
        # print(actual_data[dd_pntr])

        if actual_data[dd_pntr] == '.':
            current_gap_size += 1
        else:
            if largest_gap_size < current_gap_size:
                largest_gap_size = current_gap_size
                largest_gap_pntr = dd_pntr - largest_gap_size
            current_gap_size = 0
        dd_pntr += 1

    if largest_gap_size < filesize:
        return -1, -1
    else:
        return largest_gap_size, largest_gap_pntr
            

def update_gap_table(actual_data, gap_pntrs, fsize):
    # need to recalc all gaps smaller than size of gap fsize just inhabited (if necessary)

    changed_gap_pntr = gap_pntrs[fsize-1]
    gap_size_changed = max([x for x in range(len(gap_pntrs)) if gap_pntrs[x] == changed_gap_pntr]) + 1
    
    gap_pntr_idx = 0
    while gap_pntr_idx < gap_size_changed:
        # gap pntrs for gap <= gap_size_changed need to be re-searched if not already reassigned in prev loop
        if gap_pntrs[gap_pntr_idx] == changed_gap_pntr:
            # find next available gap for file size
            gap_size, gap_pntr = find_leftmost_gap_for_size(actual_data, gap_pntrs[gap_pntr_idx], gap_pntr_idx+1)

            if gap_size >= gap_pntr_idx + 1 and gap_size < 10:
                for j in range(gap_pntr_idx, gap_size):
                    if gap_pntrs[j] == changed_gap_pntr:
                        gap_pntrs[j] = gap_pntr
                    gap_pntr_idx += 1
            else:
                gap_pntrs[gap_pntr_idx] = -1
                gap_pntr_idx += 1
        else:
            gap_pntr_idx += 1
    return gap_pntrs


def sumcheck(data):
    check = 0
    for i in data:
            if i != '.':
                check += int(i)
    return check


def part_2(file):
    # x = '000000000877666...111111115555....222222244444..333333...................................'
    # checksum = 0
    # for i, el in enumerate(x):
    #     if el != '.':
    #         checksum += i * int(el)
    # return checksum
    with open(file, 'r') as file:
        disk_map = file.read().replace('\n', '')
        disk_map = list(map(int, disk_map))

        disk_data_pointer = sum(disk_map) - 1

        # bruteforcing the disk data this time instead of saving space like p1, sorry
        actual_data = []
        for i, el in enumerate(disk_map):
            if i % 2 == 0:
                actual_data.extend([int(i/2)]*el)
            else:
                actual_data.extend(['.']*el)
        
        with open("day_9_actual_data_input.txt", "w") as txt_file:
            txt_file.write(",".join([str(x) for x in actual_data]))

        # my own checksum (to check no data is missing at end of data shuffle)
        start_check = sumcheck(actual_data)
        
        # initialise gap pointers table
        disk_data_fwd_gap_pntrs = init_gap_table(disk_map)

        for disk_map_bkwd_pntr in range(len(disk_map) - 1, -1, -1):
            if disk_map_bkwd_pntr == 10536:
                print("here")
            #print(disk_map_bkwd_pntr)
            val = disk_map[disk_map_bkwd_pntr]
            # if gap, move to next file
            if disk_map_bkwd_pntr % 2 != 0:
                disk_data_pointer -= val
            else:
                file_id = int(disk_map_bkwd_pntr / 2)

                # no gaps left, leave as is
                if disk_data_fwd_gap_pntrs[val-1] == -1 or disk_data_fwd_gap_pntrs[val-1] > disk_data_pointer:
                    disk_data_pointer -= val
                # gap available
                else:
                    # find leftmost gap using gap table
                    gap_pointer = disk_data_fwd_gap_pntrs[val-1]
                    # fill in moved file
                    for i in range(val):
                        actual_data[gap_pointer + i] = file_id
                    disk_data_fwd_gap_pntrs = update_gap_table(actual_data, disk_data_fwd_gap_pntrs, val)
                    # "delete" file
                    for i in range(val):
                        actual_data[disk_data_pointer - i] = '.'
                    disk_data_pointer -= val
            c = sumcheck(actual_data)
            if c != start_check:
                print(f"Sumcheck not matching, value is {c} at pntr {disk_map_bkwd_pntr}")
                break
        
        with open("day_9_actual_data_output.txt", "w") as txt_file:
            txt_file.write(",".join([str(x) for x in actual_data]))

        endcheck = 0
        for i in actual_data:
            if i != '.':
                endcheck += int(i)
        print(start_check, endcheck)


        checksum = 0
        for i, el in enumerate(actual_data):
            if el != '.':
                checksum += i * int(el)
        return checksum


# test_part_1()
# test_part_2a()
test_part_2b()

# print(part_1("data/day_9_input.txt"))
print(part_2("data/day_9_input.txt"))