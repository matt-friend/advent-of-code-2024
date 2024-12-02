import numpy as np

data = np.genfromtxt("data/day_1_input.txt", dtype=int)
data = np.sort(data.T)

print(np.sum(abs(data[0]-data[1])))


