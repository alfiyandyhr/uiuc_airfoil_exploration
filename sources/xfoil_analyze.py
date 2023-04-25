# -------------------------------------------------------------------
# Runs an XFOIL analysis for a given airfoil and flow conditions
# by alfiyandyhr
# -------------------------------------------------------------------
import os
import subprocess
import numpy as np
import time

# Inputs

# Read
with open('airfoil_names.txt', 'r') as f:
	names_list = f.readlines()

for i in range(len(names_list)):
	names_list[i] = names_list[i][:-1]

t_init = time.time()

for ind in range(len(names_list)):
	print(f'Analyzing {names_list[ind]} ...')

	airfoil_name = names_list[ind]
	alpha_i = 0
	alpha_f = 10
	alpha_step = 0.5
	Re = 3.5e6
	Mach = 0.117
	n_iter = 100

	# XFOIL Input
	if os.path.exists(f'polar_data/{names_list[ind]}'):
		os.remove(f'polar_data/{names_list[ind]}')

	with open('input_file.in', "w") as f:
		f.write(f'LOAD processed_coordinates/{airfoil_name}\n')
		f.write(f'{airfoil_name}\n')
		f.write('PANE\n')
		f.write('OPER\n')
		f.write(f'Visc {Re}\n')
		f.write(f'Mach {Mach}\n')
		f.write('PACC\n')
		f.write(f'polar_data/{names_list[ind]}\n\n')
		f.write(f'Iter {n_iter}\n')
		f.write(f'ASeq {alpha_i} {alpha_f} {alpha_step}\n')
		f.write('\n')
		f.write('quit\n')

	subprocess.call('xfoil < input_file.in', shell=True)

t_final = time.time()
np.savetxt('analysis_time.dat', [t_final-t_init])