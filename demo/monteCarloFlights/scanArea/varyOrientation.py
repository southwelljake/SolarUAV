import timeit
from src.simulation import Simulation
import matplotlib.pyplot as plt
import datetime
import pandas as pd
from src.generatePaths import GeneratePaths

start_time = timeit.default_timer()

# London
latitude = 51.5072
longitude = 0.1276
time_zone = 'GMT'

start_hour = 2
duration = 2

cloud_data = [
    pd.read_csv('../../../data/cloud_data/cloud_data_london/cloud_cover_16_04_31.csv'),
]

# Path 1
path_1 = GeneratePaths(
    shape='s',
    start_point=[30000, 40000],
    scanning_range=1000,
    scanning_width=20000,
    scanning_length=20000,
    direction='n',
)

# Sim 1
sim_1 = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=cloud_data,
    path=path_1,
    mission_type='p2p',
    date=datetime.date(2021, 7, 1),
)

flight_model_1 = sim_1.generate()
flight_model_1.sim_flight()

# Path 2
path_2 = GeneratePaths(
    shape='s',
    start_point=[30000, 40000],
    scanning_range=1000,
    scanning_width=20000,
    scanning_length=20000,
    direction='e',
)

# Sim 2
sim_2 = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=cloud_data,
    path=path_2,
    mission_type='p2p',
    date=datetime.date(2021, 7, 1),
)

flight_model_2 = sim_2.generate()
flight_model_2.sim_flight()

# Path 3
path_3 = GeneratePaths(
    shape='s',
    start_point=[30000, 40000],
    scanning_range=1000,
    scanning_width=20000,
    scanning_length=20000,
    direction='w',
)

# Sim 3
sim_3 = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=cloud_data,
    path=path_3,
    mission_type='p2p',
    date=datetime.date(2021, 7, 1),
)

flight_model_3 = sim_3.generate()
flight_model_3.sim_flight()

# Path 4
path_4 = GeneratePaths(
    shape='s',
    start_point=[30000, 40000],
    scanning_range=1000,
    scanning_width=20000,
    scanning_length=20000,
    direction='s',
)

# Sim 4
sim_4 = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=cloud_data,
    path=path_4,
    mission_type='p2p',
    date=datetime.date(2021, 7, 1),
)

flight_model_4 = sim_4.generate()
flight_model_4.sim_flight()

end_time = timeit.default_timer()
print("--- %s seconds ---" % (end_time - start_time))

fig2, ax2 = plt.subplots()

ax2.plot(flight_model_1.state_var[0, :] / 1000, flight_model_1.state_var[1, :] / 1000, label='North')
ax2.plot(flight_model_2.state_var[0, :] / 1000, flight_model_2.state_var[1, :] / 1000, label='East')
ax2.plot(flight_model_4.state_var[0, :] / 1000, flight_model_4.state_var[1, :] / 1000, label='South')
ax2.plot(flight_model_3.state_var[0, :] / 1000, flight_model_3.state_var[1, :] / 1000, label='West')
ax2.legend()
ax2.set_xlabel('X Distance (km)')
ax2.set_ylabel('Y Distance (km)')

plt.show()
