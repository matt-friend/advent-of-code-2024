import csv

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

n_safe = 0

with open("data/day_2_input.txt", newline='') as f:
  reader = csv.reader(f)
  for row in reader:
    print(row)
    row_data = list(map(int, row[0].split(" ")))
    n_safe += int(is_safe(row_data))

print(n_safe)