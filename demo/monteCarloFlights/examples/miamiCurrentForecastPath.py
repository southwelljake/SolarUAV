from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
import numpy as np

# Script to assess performance of random cloud samples against path ideal for current forecast

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
points = np.array(([205000, 200000], [0, 300000],
                   [-205000, 200000], [0, 0]))

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=file,
    points=points,
)

file_name = '../../../data/monte_carlo_results/examples/miami_current_forecast_200.txt'
no_sims = 200

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
)

monte_carlo.run()
