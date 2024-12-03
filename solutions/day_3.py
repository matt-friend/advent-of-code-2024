import re

def mul_match_result(mul_str):
    nums = mul_str[4:-1].split(",")
    return int(nums[0]) * int(nums[1])

def find_muls_in_str(s):
    return re.findall(r'mul\(\d{1,3},\d{1,3}\)', s)


def mul_total_from_mul_str_list(mul_str_list):
    mul_total = 0
    for m in mul_str_list:
        mul_total += mul_match_result(m)
    return mul_total

def part_1():
    with open("data/day_3_input.txt", 'r') as file:
        data_str = file.read().replace('\n', '')
        matches = find_muls_in_str(data_str)
        mul_total = mul_total_from_mul_str_list(matches)
        print(mul_total)


def part_2():
    with open("data/day_3_input.txt", 'r') as file:
        data_str = file.read().replace('\n', '')
        do_strs = re.split(r'do\(\)', data_str)
        valid_muls = []
        for d in do_strs:
            valid_muls_str = re.split(r'don\'t\(\)', d)[0]
            valid_muls.extend(find_muls_in_str(valid_muls_str))
        valid_mul_total = mul_total_from_mul_str_list(valid_muls)
        print(valid_mul_total)
        
part_1()
part_2()
