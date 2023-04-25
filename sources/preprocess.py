# --------------------------------------------------------------------
# Preprocess the coordinates data and then analyze them using XFOIL
# 
# by @alfiyandyhr
# --------------------------------------------------------------------

import numpy as np

# Read airfoil names
with open('airfoil_names.txt', 'r') as f:
	names_list = f.readlines()

for i in range(len(names_list)):
	names_list[i] = names_list[i][:-1]

for ind in range(len(names_list)):
	print(f'{ind+1}. Preprocessing {names_list[ind]} ...')

	# Loading raw coordinates with various formats
	try:
		coord = np.genfromtxt(f'coordinate_data/{names_list[ind]}')
	except ValueError:
		try:
			coord = np.genfromtxt(f'coordinate_data/{names_list[ind]}', skip_header=1)
		except ValueError:
			try:
				coord = np.genfromtxt(f'coordinate_data/{names_list[ind]}', skip_header=2)
			except ValueError:
				try:
					coord = np.genfromtxt(f'coordinate_data/{names_list[ind]}', skip_header=3)
				except ValueError:
					coord = np.genfromtxt(f'coordinate_data/{names_list[ind]}', skip_header=3, skip_footer=1)
	
	# Remove nan
	if np.isnan(coord[0, 0]):
		coord = coord[1:]

	# Remove number of points
	if coord[0, 0] > 1.0:
		coord = coord[1:]

	# Make the XFOIL format
	if coord[0, 0] < 0.1: # Is the point LE?
		for i in range(len(coord)): # Sweeping to find break point
			if i != len(coord)-1:
				if coord[i, 0] > coord[i+1, 0]:
					coord_n = np.concatenate((coord[:i+1][::-1], coord[i+1:]), axis=0)
	else:
		coord_n = coord.copy()

	# Saving processed coordinates
	np.savetxt(f'processed_coordinates/{names_list[ind]}', coord_n)