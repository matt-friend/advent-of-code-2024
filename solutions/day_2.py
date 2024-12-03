import csv
import numpy as np

def is_safe(data):
    if data[1] > data[0]:
        for i in range(len(data)-1):
            if not (1 <= data[i+1] - data[i] <= 3):
                return False
        return True
    elif data[1] < data[0]:
        for i in range(len(data)-1):
            if not (1 <= data[i] - data[i+1] <= 3):
                return False
        return True
    else:
        return False
    
def is_safe_after_damping(data):
    if not is_safe(data):
        for i in range(len(data)):
            d = np.delete(data, i)
            if is_safe(d):
                return True
        return False
    return True

n_safe = 0

with open("data/day_2_input.txt", newline='') as f:
  reader = csv.reader(f)
  for row in reader:
    row_data = np.array(list(map(int, row[0].split(" "))))
    n_safe += int(is_safe_after_damping(row_data))

print(n_safe)