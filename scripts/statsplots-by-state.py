# Population Data source: http://worldpopulationreview.com/states/
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

df  = pd.read_csv('../data/station-coords/num-by-state.csv', names=['State Code', 'num_stations'])
pop = pd.read_csv('../data/usa-population/worldpopulationreview-data.csv')
df = pd.merge(df, pop, on='State Code')
#print(df)

corr_pop, _ = spearmanr(df['num_stations'], df['Pop'])
corr_den, _ = spearmanr(df['num_stations'], df['density'])
#print(f'Spearman Station vs. Population: {corr_pop}')
#print(f'Spearman Station vs. Density: {corr_den}')

grid = plt.GridSpec(2, 2, wspace=0.1, hspace=0.6)
ax1 = plt.subplot(grid[0, 0])
ax2 = plt.subplot(grid[0, 1])
ax3 = plt.subplot(grid[1, :2])

df.sort_values('num_stations', ascending=False).plot.bar(x='State Code', y='num_stations', rot=0, color='k', alpha=0.3, ax=ax3)
ax3.set_ylabel("Number of Mapped Gas Stations", fontsize=8)
ax3.set_title('Number of Mapped Gas Stations by State', fontsize=10)
for tick in ax3.get_xticklabels(): tick.set_rotation(90)
ax3.set_xlabel('State Code', fontsize=8)
ax3.get_legend().remove()
ax3.tick_params(labelsize=7)
#ax3.set_yticklabels(['0', '1K', '2K', '3K'])

df.sort_values('num_stations', ascending=False).plot.scatter(x='num_stations', y='Pop', color='k', alpha=0.3, ax=ax1)
ax1.set_title('Stations vs. Population', fontsize=10)
ax1.set_ylabel('Population in 2019', fontsize=8)
ax1.set_xlabel('Number of Mapped Gas Stations', fontsize=8)
ax1.set_xticklabels(['0', '0', '1K', '2K', '3K'])
ax1.set_yticklabels(['0', '0', '10M', '20M', '30M', '40M'])
ax1.annotate(f'Spearman Coeff: {round(corr_pop, 3)} ', xy=(20, 37000000), fontsize=8)
ax1.annotate('Idaho', xy=(2981, 1790182), xytext=(2600, 15000000), fontsize=6, arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))


df.sort_values('num_stations', ascending=False).plot.scatter(x='num_stations', y='density', color='k', alpha=0.3, ax=ax2)
ax2.set_title('Stations vs. Density', fontsize=10)
ax2.set_ylabel('Density in 2019', fontsize=8)
ax2.set_xlabel('Number of Mapped Gas Stations', fontsize=8)
ax2.yaxis.set_label_position("right")
ax2.yaxis.tick_right()
ax2.set_xticklabels(['0', '0', '1K', '2K', '3K'])
ax2.set_yticklabels(['0', '0', '5K', '10K'])
ax2.annotate(f'Spearman Coeff: {round(corr_den, 3)}', xy=(1300, 10800), fontsize=8)
ax2.annotate(f'Washington, DC', xy=(85, 11665), xytext=(90,7500), fontsize=6, arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))

plt.savefig('../publication/mapped-station-stats.pdf')
#plt.show()
