""" gb-collect-station-ids.py
Author: Kevin Dick
Date: 2019-09-09
---
Perform a HEAD request to check for response.
Append results to file iteratively for restarts.

"""
import requests
import os, sys
import random
import string
from time import sleep
from selenium import webdriver

BASE_QUERY = 'https://www.gasbuddy.com/Station/'
LAST_ID    = 1000000
OUT_FILE   = '../data/station-coords/gb-coords.csv'
SLEEP      = 3
VERBOSE    = False
HEADLESS   = True

# Selenium Class Element Identifiers
name_sel  = 'header__header2___1p5Ig header__header___1zII0 header__evergreen___2DD39 header__snug___lRSNK StationInfoBox__header___2cjCS' # The parent of Station Name
addr_sel  = 'StationInfoBox__ellipsisNoWrap___1-lh5'
tel_sel   = 'StationInfoBox__phoneLink___2LtAk'
gas_sel   = 'text__xl___2MXGo text__bold___1C6Z_ text__left___1iOw3 FuelTypePriceDisplay__price___3iizb'

def selenium_based_check(url):
        """ selenium_based_check
            Input:  <str> url, iterated GB station website
            Output: <list>, [0] <bool> if page exists
                            [1] <int> station id
                            [2] <str> station webpage
                            [3] <str> station name
                            [4] <str> station address
                            [5] <str> station telephone number
                            [6] <str> regular gas price
                            [7] <str> midrange gas price
                            [8] <str> premium gas price
                            [9] <str> diesel gas price
        """
        # Setup the ChromeDriver depending on the context...
        driver = None
        if HEADLESS: # Used with dna-26
            options = webdriver.ChromeOptions()
            options.binary_location = '/usr/bin/google-chrome'
            options.add_argument('headless')
            driver = webdriver.Chrome('../drivers/chromedriver', chrome_options=options) 
        else: driver = webdriver.Chrome() # MacOS

        # Begin the query...
        driver.get(url)
	html_source = driver.page_source

	#	 [T/F, 'Name', 'Address', 'Tel.', 'Reg.$', 'Mid.$', 'Pre.$', 'Die.$']
	result = [False, '', '', '', '', '', '', ''] 
	if 'Oops...' in html_source: 
		if VERBOSE: print('Fail')
	else: 
		if VERBOSE: print('Exists!')

		# Extract Station Name, Address, Phone Number, Reg/Mid/Pre Price
		station_name = driver.find_elements_by_xpath("//h2[contains(@class,'{}')]/span".format(name_sel))[0].text # Get the first child only...

		station_addr = driver.find_elements_by_xpath("//div[contains(@class,'{}')]/span/span".format(addr_sel))[0].text.replace(',', ' ') + ' ' + driver.find_elements_by_xpath("//div[contains(@class,'{}')]/span/span".format(addr_sel))[2].text.replace(',', ' ')
		station_tel  = driver.find_elements_by_xpath("//a[contains(@class,'{}')]".format(tel_sel))[0].text.replace(',', ' ') 

		station_gas = [x.text.encode('ascii', 'ignore') for x in driver.find_elements_by_xpath("//span[contains(@class,'{}')]".format(gas_sel))]
		while len(station_gas) < 4: station_gas.append('NA')

		# Need to use latin1 decoding to deal with cent symbols in some Canadian gas pricings...
		if VERBOSE: print('Station Name: {}\nStation Addr: {}\nStation Tel: {}\nStationn Prices: {}'.format(station_name, station_addr, station_tel, ','.join(station_gas)))
		result = [True, station_name, station_addr, station_tel] +  station_gas
	driver.quit()
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
	query_results = selenium_based_check(query)
	if query_results[0]: 
		station_data = [str(cur_id), query] + query_results[1:]
		f = open(OUT_FILE, 'a')
		f.write("{}\n".format(','.join(station_data)))
		f.close()
