""" gb-collect-station-ids.py
Author: Kevin Dick
Date: 2019-09-09
---
Perform a HEAD request to check for response.
Append results to file iteratively for restarts.

"""
import requests
import os
import random
import string
from time import sleep
from selenium import webdriver
from selenium import webdriver


BASE_QUERY = 'https://www.gasbuddy.com/Station/'
LAST_ID    = 1000000
OUT_FILE   = '../data/station-coords/gb-coords.csv'
SLEEP      = 3
VERBOSE    = True

def selenium_based_check(url):
	DRIVER     = webdriver.Chrome()
	DRIVER.get(url)
	html_source = DRIVER.page_source
	result = None
	if 'Oops...' in html_source: 
		print('Fail')
		result = False
	else: 
		print('Exists!')
		result = True
	DRIVER.quit()
	return result

# Set current id; jump ahead if some already processed...
cur_id = 0
if os.path.exists(OUT_FILE): 
	cur_id = int(open(OUT_FILE, 'r').readlines()[-1].split(',')[0])
else:
	os.system('touch {}'.format(OUT_FILE))

while cur_id <= LAST_ID:
	cur_id += 1
	query = BASE_QUERY + str(cur_id)
	if VERBOSE: print('querying {}: {}'.format(cur_id, query))
	#sleep(SLEEP)

	# Make the query adn save to file if station nexists...
	if selenium_based_check(query): 
		f = open(OUT_FILE, 'a')
		f.write("{},{}\n".format(cur_id, query))
		f.close()
