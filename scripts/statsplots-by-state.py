# Population Data source: http://worldpopulationreview.com/states/
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
import geopandas as gpd
import matplotlib.gridspec as gridspec
from shapely.geometry import Point

CURRPATH = os.path.abspath(os.path.dirname(__file__))
MAP_PATH = os.path.join(CURRPATH, '../data/tl_2017_us_state/tl_2017_us_state.shp')
IN_PATH = os.path.join(CURRPATH, '../data/station-coords/allgas-geocode-success.csv')
STATES = os.path.join(CURRPATH, '../data/states.csv')

# read files and convert to gpd
us_map = gpd.read_file(MAP_PATH)
station_data = pd.read_csv(IN_PATH, error_bad_lines=False, names = ['address', 'lat', 'lon', 'state'])

geom = [Point(xy) for xy in zip(station_data['lon'], station_data['lat'])]
crs = {'init': 'epsg4326'}
station_data = gpd.GeoDataFrame(station_data, crs=crs, geometry=geom)
#print(station_data.head())

df  = pd.read_csv('../data/station-coords/num-by-state.csv', names=['State Code', 'num_stations'])
pop = pd.read_csv('../data/usa-population/worldpopulationreview-data.csv')
df = pd.merge(df, pop, on='State Code')
#print(df)

corr_pop, _ = spearmanr(df['num_stations'], df['Pop'])
corr_den, _ = spearmanr(df['num_stations'], df['density'])
#print(f'Spearman Station vs. Population: {corr_pop}')
#print(f'Spearman Station vs. Density: {corr_den}')

fig = plt.figure(figsize=(7,9), tight_layout=True)
grid = plt.GridSpec(5, 2, wspace=0.15, hspace=0.9)
ax1 = plt.subplot(grid[0:2, 0])
ax2 = plt.subplot(grid[0:2, 1])
ax3 = plt.subplot(grid[2,   :])
ax4 = plt.subplot(grid[3:5, :])

# Population Figure
df.sort_values('num_stations', ascending=False).plot.scatter(x='num_stations', y='Pop', color='k', alpha=0.3, ax=ax1)
ax1.set_title('A: Stations vs. Population', fontsize=10)
ax1.set_xlim([0, 3300])
ax1.set_ylim([0, 40600000])
ax1.set_ylabel('Population in 2019', fontsize=8)
ax1.set_xlabel('Num. Mapped Gas Stations', fontsize=8)
ax1.set_xticklabels(['0', '1K', '2K', '3K'])
ax1.set_yticklabels(['0', '10M', '20M', '30M', '40M'])
ax1.annotate(f'Spearman Coeff: {round(corr_pop, 3)} ', xy=(150, 35000000), fontsize=8)
ax1.annotate('Idaho', xy=(2981, 1790182), xytext=(2600, 15000000), fontsize=6, arrowprops=dict(arrowstyle="->", linestyle='dotted', connectionstyle="arc3"))

# Density Figure
df.sort_values('num_stations', ascending=False).plot.scatter(x='num_stations', y='density', color='k', alpha=0.3, ax=ax2)
ax2.set_title('B: Stations vs. Density', fontsize=10)
ax2.set_ylabel('Density in 2019', fontsize=8)
ax2.set_xlabel('Num. Mapped Gas Stations', fontsize=8)
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
ax2.set_xticklabels(['0', '0', '1K', '2K', '3K'])
ax2.set_yticklabels(['0', '0', '2K', '4K', '6K', '8K', '10K', '12K'])
ax2.annotate(f'Spearman Coeff: {round(corr_den, 3)}', xy=(1300, 10800), fontsize=8)
ax2.annotate(f'Washington, DC', xy=(85, 11665), xytext=(90,7500), fontsize=6, arrowprops=dict(arrowstyle="->", linestyle='dotted', connectionstyle="arc3"))

# State Bar Figure
df.sort_values('num_stations', ascending=False).plot.bar(x='State Code', y='num_stations', rot=0, color='k', alpha=0.3, ax=ax3)
ax3.set_ylabel("Num. Mapped Gas Stations", fontsize=8)
ax3.set_title('C: Number of Mapped Gas Stations by State', fontsize=10)
for tick in ax3.get_xticklabels(): tick.set_rotation(90)
ax3.set_xlabel('State Code', fontsize=8)
ax3.set_yticklabels(['0', '1K', '2K', '3K'])
ax3.get_legend().remove()
ax3.tick_params(labelsize=7)
#ax3.set_yticklabels(['0', '1K', '2K', '3K'])

# The US Map
ax4.set_xlim([-130, -60])
ax4.set_ylim([20, 50])
ax4.axis('off')
ax4.set_title('D: Mapped Gas Station Locations in US', fontsize=10)
us_map.plot(ax=ax4, color='white', edgecolor='black')
station_data.plot(ax=ax4, markersize=1, color='#111111', marker = 'o', alpha=0.1)

plt.savefig('../publication/mapped-station-stats-with-map.pdf', bbox_inches='tight',pad_inches=0)
#plt.show()
