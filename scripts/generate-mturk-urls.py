import os, sys
file_in  = '../data/station-coords/allgas-geocode-success.csv'
file_out = '../data/station-coords/mturk-all-seed-urls.txt'

with open(file_in, 'r') as fin, open(file_out, 'w') as fout:
	for addr in list(set(fin.readlines())):	# Duplicate removal by going through a set data structure...
		fout.write("https://www.instantstreetview.com/@{},{},0.0h,0.0p,1.0z\n".format(addr.split(',')[1], addr.split(',')[2]))
