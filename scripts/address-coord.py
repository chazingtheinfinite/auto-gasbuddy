import csv
import os
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# modify IN_PATH to desired input file
VERBOSE = True
CURRPATH = os.path.abspath(os.path.dirname(__file__))
IN_PATH = os.path.join(CURRPATH, '../data/station-coords/allgas-coords.csv')
OUT_FILE = os.path.join(CURRPATH, '../data/station-coords/gasBuddy-geocode.csv')

def geocode_addr(in_path, type, start, geo_coords):    
    """ geocode_addr
        Input:  
            <str>   in_path, relative path to data file
            <str>   type, "AG" for allGas, otherwise gasBuddy
            <int> start, line number of data file to start reading from
            <df> geo_coords, geocode of gas stations in format: 
                address <str> lat <str> lon <str> failed <bool> 
        Output: 
            <df> geo_coords, geocode of gas stations in format: 
                address <str> lat <str> lon <str> failed <bool> 
    """
    with open(in_path) as file:
        addressFile = list(csv.reader(file))

    geolocator = Nominatim(user_agent='autoGasBuddy')
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
    index = 1 if type == 'AG' else 3

    for line in range(start, len(addressFile)):
        address = addressFile[line][index]
        failed = False
        
        # attempt delayed requests using geocode
        location = geocode(addressFile[line][index])

        if location != None:
            lat, lon = location.raw['lat'], location.raw['lon']
            
            if VERBOSE: 
                print("Current Location: {}".format(location))
                print("Lat, Long: {}, {}".format(lat, lon))
        # log failed attempts
        else:
            lat = lon = np.NaN
            failed = True

            if VERBOSE:
                print("Failed on {}, {}, {}".format(type, line, address))
        
        geo_coords = geo_coords.append({'address': address,
                                        'lat':     lat,
                                        'lon':     lon,
                                        'failed':  failed},
                                        ignore_index = True)
    return geo_coords
                    
if os.path.exists(OUT_FILE):
    if VERBOSE: print("Appending...") 
else:
    if VERBOSE: print("Generating file...")
    os.system('touch {}'.format(OUT_FILE))

geo_coords = pd.DataFrame(columns=['address', 'lat', 'lon', 'failed'])

# convert addresses to geocode
geo_coords = geocode_addr(IN_PATH, "GB", 0, geo_coords)
geo_coords.to_csv(path_or_buf=OUT_FILE, mode='a', index=False)


