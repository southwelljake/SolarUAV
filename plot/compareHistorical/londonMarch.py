import pandas as pd
import matplotlib.pyplot as plt

historical = pd.read_csv('../../data/cloud_data/cloud_data_london/London 2021-03-11 to 2021-03-18.csv')
current = pd.read_csv('../../data/cloud_data/cloud_data_london/cloud_cover_10_04_55.csv')

h_cc = historical['cloudcover'] * 100
h_hrs = [i for i in range(0, len(h_cc))]

c_cc = current['total_clouds']
c_hrs = [3 * i for i in range(0, len(c_cc))]

fig, ax = plt.subplots(ncols=2)

ax[0].plot(h_hrs, h_cc, label='Historical')
ax[1].plot(c_hrs, c_cc, label='Current')

ax[0].set_title('Historical Data 11/03/21')
ax[0].set_xlabel('Time (hrs)')
ax[0].set_ylabel('Cloud Cover (%)')
ax[1].set_title('Forecast Data 11/03/22')
ax[1].set_xlabel('Time (hrs)')
ax[1].set_ylabel('Cloud Cover (%)')

plt.show()