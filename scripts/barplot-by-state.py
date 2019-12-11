import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('../data/station-coords/num-by-state.csv', names=['state', 'num_stations'])

ax = df.sort_values('num_stations', ascending=False).plot.bar(x='state', y='num_stations', rot=0, color='k', alpha=0.3)
plt.xticks(rotation=90)
ax.tick_params(axis="x", labelsize=8)
ax.get_legend().remove()
plt.title('Number of Gas Stations by State')
plt.ylabel('Number of Gas Stations')
plt.xlabel('State Code')
plt.show()
