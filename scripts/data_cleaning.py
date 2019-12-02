import os
import pandas as pd
import csv

CURRPATH = os.path.abspath(os.path.dirname(__file__))
IN_PATH = os.path.join(CURRPATH, '../data/station-coords/allgas-geocode.csv')
OUT_FILE = os.path.join(CURRPATH, '../data/station-coords/allgas-geocode-success.csv')
STATES = os.path.join(CURRPATH, '../data/states.csv')

def clean_df(df):
    # filter to geocoded addresses and group by state
    df = df[df.failed == False]
    df = df[df['address'].apply(lambda x: len(x.split()) > 1)]
    df['state'] = df.address.apply(lambda x: x.split()[-2])

    with open(STATES, encoding='utf8') as file:
        state_list = file.readlines()

    # remove entries with invalid states
    state_list = [x.strip() for x in state_list]
    df = df[df['state'].apply(lambda x: x in state_list)]

    df = df.drop(columns=['failed'])

    return df

station_data = pd.read_csv(IN_PATH, header=None, names=['address', 'lat', 'lon', 'failed'])
station_data = clean_df(station_data)

print(station_data.head())
print(station_data.shape)

station_data.to_csv(path_or_buf=OUT_FILE, mode='w', index=False, header=False)