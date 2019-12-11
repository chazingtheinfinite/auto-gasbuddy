import os, sys
import random

num_select = 1000

# For Replicability of results...
random.seed(42)

file_in   = '../data/station-coords/mturk-all-seed-urls.txt'
file_pre  = '../data/station-coords/mturk-prequal-urls.txt'
file_post = '../data/station-coords/mturk-postqual-urls.txt'

with open(file_in, 'r') as fin, open(file_pre, 'w') as fpre, open(file_post, 'w') as fpost:
        all_urls = fin.readlines()
	random.shuffle(all_urls)
	# Write out top selection and remainder to post-qualification file...
	for i in range(num_select):          fpre.write(all_urls[i])
	for j in range(i+1, len(all_urls)): fpost.write(all_urls[j])
