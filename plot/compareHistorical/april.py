import pandas as pd
import matplotlib.pyplot as plt

historical = pd.read_csv('../../data/cloud_data/london_april/London 2022-04-03 to 2022-04-09.csv')
current = pd.read_csv('../../data/cloud_data/london_april/london_13_40_26.csv')

h_cc = historical['cloudcover']
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

historical = pd.read_csv('../../data/cloud_data/melbourne_april/Melbourne 2022-04-03 to 2022-04-09.csv')
current = pd.read_csv('../../data/cloud_data/melbourne_april/melbourne_13_40_37.csv')

h_cc = historical['cloudcover']
h_hrs = [i for i in range(0, len(h_cc))]

c_cc = current['total_clouds']
c_hrs = [3 * i for i in range(0, len(c_cc))]

fig2, ax2 = plt.subplots(ncols=2)

ax2[0].plot(h_hrs, h_cc, label='Historical')
ax2[1].plot(c_hrs, c_cc, label='Current')

ax2[0].set_title('Historical Data 11/03/21')
ax2[0].set_xlabel('Time (hrs)')
ax2[0].set_ylabel('Cloud Cover (%)')
ax2[1].set_title('Forecast Data 11/03/22')
ax2[1].set_xlabel('Time (hrs)')
ax2[1].set_ylabel('Cloud Cover (%)')


plt.show()