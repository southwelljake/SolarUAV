from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
import numpy as np


# Central Canada
# latitude = 55
# longitude = -100
# time_zone = 'America/Winnipeg'

# London
# latitude = 51.5072
# longitude = 0.1276
# time_zone = 'GMT'

# Miami
latitude = 25.7617
longitude = 80.1918
time_zone = 'EST'

start_hour = 12
duration = 2

# Recorded Cloud Data from Miami
file = [
    # Day 1
    pd.read_csv('../../../data/cloud_data/cloud_data_miami/cloud_cover_11_18_29.csv'),
    pd.read_csv('../../../data/cloud_data/cloud_data_miami/cloud_cover_17_18_37.csv'),
    pd.read_csv('../../../data/cloud_data/cloud_data_miami/cloud_cover_23_18_46.csv'),
    # Day 2
    pd.read_csv('../../../data/cloud_data/cloud_data_miami/cloud_cover_05_18_54.csv'),
    pd.read_csv('../../../data/cloud_data/cloud_data_miami/cloud_cover_11_19_10.csv'),
]

# Ideal flight path for clear skies in Miami
points = np.array(([200000, 200000], [0, 300000],
                   [-200000, 200000], [0, 0]))

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=file,
    points=points,
)

file_name = '../../data/simulation_results/5_samples.txt'
no_sims = 5

other_variables = [['flight_model.aircraft.mass', [18, 18.5]],
                   ['flight_model.battery.capacity', [0.5 * 4590000, 1.5 * 4590000]]]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
