import matplotlib.pyplot as plt
from src.solarModel import SolarModel
from src.cloudCover import CloudCover
import datetime
import numpy as np

# London
latitude = 50
longitude = 0
time_zone = 'GMT'
days = 4

cloud_cover = CloudCover(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    days=days,
)

cloud_cover.generate_data()
cloud_cover.process_data()

solar_model = SolarModel(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    days=days,
)

solar_model.generate_data()

data = cloud_cover.data

fig, ax = plt.subplots()
fig.autofmt_xdate(rotation=45)

ax.plot(data['total_clouds'], label='Total Clouds')
ax.plot(data['high_clouds'], label='High Clouds')
ax.plot(data['mid_clouds'], label='Mid Clouds')
ax.plot(data['low_clouds'], label='Low Clouds')
ax.legend(loc='upper right')
ax.set_xlabel('Date')
ax.set_ylabel('Cloud Cover (%)')
ax.set_title('GFS Forecast, Latitude: ' + str(latitude) +
             ' Longitude: ' + str(longitude) + ', ' + str(datetime.date.today()))

fig2, ax2 = plt.subplots()

t_pslr = np.arange(0, solar_model.days * 24)
P_slr = np.zeros(0)
P_slr_cc = np.zeros(0)
for ttt in t_pslr:
    P_slr = np.append(P_slr, solar_model.calculate_solar_power(
        ttt, 2.857, 0) * 0.2)
    P_slr_cc = np.append(P_slr_cc, solar_model.calculate_solar_power(
        ttt, 2.857, cloud_cover.cloud_cover[ttt, 1]) * 0.2)
ax2.plot(t_pslr, P_slr, '--', label=r'$P_{clear}$')
ax2.plot(t_pslr, P_slr_cc, '--', label=r'$P_{cloud}$')
ax2.legend(loc='upper left')
ax2.set_xlabel('Time (hrs)')
ax2.set_ylabel('Power (W)')

plt.show()

