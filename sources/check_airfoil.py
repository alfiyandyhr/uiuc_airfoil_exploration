import numpy as np

# Read
with open('airfoil_names.txt', 'r') as f:
	names_list = f.readlines()

for i in range(len(names_list)):
	names_list[i] = names_list[i][:-1]

print(names_list[967])