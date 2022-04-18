import matplotlib.pyplot as plt
import datetime
import numpy as np
from src.solarModel import SolarModel

location = ['Barrow', 'London', 'Los Angeles', 'Mexico City', 'Singapore', 'Brisbane', 'Melbourne', 'Ushuaia']
latitude = [70, 50, 35, 20, 0, -25, -40, -55]
longitude = [-155, 0, -120, -100, 105, 155, 145, -70]
time_zone = ['America/Anchorage', 'GMT', 'America/Los_Angeles', 'America/Mexico_City', 'Singapore',
             'Australia/Brisbane', 'Australia/Melbourne', 'America/Argentina/Ushuaia']


itude = ['70', '50', '35', '20', '0', '-25', '-40', '-55']

fig, ax = plt.subplots(nrows=4, ncols=2)

col = 0
row = 0
for i in range(0, 8):

    hrs = []
    irr = []

    months = [i for i in range(1, 13)]
    for month in months:
        solar = SolarModel(latitude=latitude[i],
                           longitude=longitude[i],
                           time_zone=time_zone[i],
                           date=datetime.date(2021, month, 1),
                           days=1)
        solar.generate_data()

        total = 0
        for hour in range(0, 24):
            if solar.slr_irr[hour, 1] > 0:
                total += 1
        hrs.append(total)
        irr.append(np.mean(solar.slr_irr[:, 1]))

    ax[row, col].plot(months, hrs, label='Hrs Sunlight per Day')
    ax[row, col].set_ylim([-5, 30])
    ax2 = ax[row, col].twinx()
    ax2.plot(months, irr, 'C1', label='Avg Solar Irradiance')
    if col == 1:
        ax2.set_ylabel('Solar Irradiance (W/m^2)')
        ax2.legend(loc='upper right')
    else:
        ax[row, col].legend(loc='upper left')
    ax2.set_ylim([-50, 500])
    ax[row, col].set_title(location[i] + ', Latitude: ' + str(latitude[i]))

    row += 1
    if row == 4:
        col += 1
        row = 0

ax[0, 0].set_ylabel('Sunlight per day (hrs)')
ax[1, 0].set_ylabel('Sunlight per day (hrs)')
ax[2, 0].set_ylabel('Sunlight per day (hrs)')
ax[3, 0].set_ylabel('Sunlight per day (hrs)')
ax[3, 0].set_xlabel('Month')
ax[3, 1].set_xlabel('Month')

plt.subplots_adjust(left=0.075, right=0.925, top=0.95, bottom=0.075, wspace=0.25, hspace=0.275)

plt.show()
