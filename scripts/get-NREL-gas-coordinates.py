""" get-NREL-gas-coordinates.py
Author: Kevin Dick
Date: 2019-09-09
---
Uses the Nnational Renewable Energy Laboratory (NREL)
Developer API service to request a JSON object contnaining
all lat/lon coordinates of fueling stations.

API Documentation: 
https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/all/
https://developer.nrel.gov/docs/api-key/
"""
import json
import os

# Parameters
GAS_TYPE = 'all'
API_KEY  = None
FORMAT   = 'csv'
OUT_FILE = '../data/station-coords/NREL-coords.csv'

# Load the NREL API key...
with open('../api-keys.txt') as ak: API_KEY =  json.loads(ak.read())['NREL-kevin']

# Assemble the query...
query ='https://developer.nrel.gov/api/alt-fuel-stations/v1.{}?fuel_type={}&api_key={}'.format(FORMAT, GAS_TYPE, API_KEY)

# API request the CSV file and write it to file...
os.system('curl "{}" > {}'.format(query, OUT_FILE))
