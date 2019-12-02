import os
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from shapely.geometry import Point

CURRPATH = os.path.abspath(os.path.dirname(__file__))
MAP_PATH = os.path.join(CURRPATH, '../data/tl_2017_us_state/tl_2017_us_state.shp')
IN_PATH = os.path.join(CURRPATH, '../data/station-coords/allgas-geocode-success.csv')
STATES = os.path.join(CURRPATH, '../data/states.csv')

# TODO: 
# Update US plot with smaller transparent GSV Man-colored points
# Update bar graph with uniform greyscale color

# read files and convert to gpd
us_map = gpd.read_file(MAP_PATH)
station_data = pd.read_csv(IN_PATH, error_bad_lines=False, 
                                    names = ['address', 'lat', 'lon', 'state'])

geom = [Point(xy) for xy in zip(station_data['lon'], station_data['lat'])]
crs = {'init': 'epsg4326'}
station_data = gpd.GeoDataFrame(station_data, crs=crs, geometry=geom)

print(station_data.head())

fig = plt.figure(tight_layout=True)
gs = gridspec.GridSpec(3,3)

ax1 = fig.add_subplot(gs[0:2, :])
ax1.set_xlim([-130, -60])
ax1.set_ylim([20, 50])
ax1.axis('off')
ax1.set_title('Gas Station Locations in US')
us_map.plot(ax=ax1, color='white', edgecolor='black')
station_data.plot(ax=ax1, markersize=5, color='red', marker = 'o')

ax2 = fig.add_subplot(gs[2, :])
ax2.set_title('Gas Station Location Bar Graph')
station_data['state'].value_counts().plot(kind='bar', ax=ax2)
plt.show()
