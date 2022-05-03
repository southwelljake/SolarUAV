from src.probabilityForecast import ProbabilityForecast
import matplotlib.pyplot as plt
import pandas as pd

low = ProbabilityForecast(file=[
    pd.read_csv('../../data/general_cloud_data/low_cloud_data.csv'),
    pd.read_csv('../../data/general_cloud_data/lowmed_cloud_data.csv'),
    pd.read_csv('../../data/general_cloud_data/med_cloud_data.csv')
])
low.generate_data()
high = ProbabilityForecast(file=[
    pd.read_csv('../../data/general_cloud_data/med_cloud_data.csv'),
    pd.read_csv('../../data/general_cloud_data/medhigh_cloud_data.csv'),
    pd.read_csv('../../data/general_cloud_data/high_cloud_data.csv')
])
high.generate_data()

fig, ax = plt.subplots(nrows=2)

ax[0].plot(low.cloud_cover[:, 0], low.cloud_cover[:, 1], 'C0', label='Low Cloud')
ax[0].plot([0, 165], [30, 30], '--r', label='Mean')
ax[0].set_ylabel('Cloud Cover (%)')
ax[0].legend()
ax[0].set_ylim([-5, 105])
ax[1].plot(high.cloud_cover[:, 0], high.cloud_cover[:, 1], 'C1', label='High Cloud')
ax[1].plot([0, 165], [75, 75], '--r', label='Mean')
ax[1].set_xlabel('Time (hrs)')
ax[1].set_ylabel('Cloud Cover (%)')
ax[1].legend(loc='lower right')
ax[1].set_ylim([-5, 105])

plt.show()
