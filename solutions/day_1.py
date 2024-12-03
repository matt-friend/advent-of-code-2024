import numpy as np
from bisect import bisect_left, bisect_right


def part_1(d):
    d = np.sort(d)
    return np.sum(abs(d[0]-d[1]))

def count(arr, target):
    n = len(arr)
    left = bisect_left(arr, target, 0, n)
    right = bisect_right(arr, target, left, n)  # use left as a lower bound
    return right - left

def similarity_score(d):
    d = np.sort(d)
    sim_score = 0
    for num in d[0]:
        sim_score += num * count(d[1], num)
    return sim_score


data = np.genfromtxt("data/day_1_input.txt", dtype=int)
data = data.T
print(similarity_score(data))


