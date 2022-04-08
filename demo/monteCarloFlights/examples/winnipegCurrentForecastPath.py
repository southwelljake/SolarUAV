from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
import numpy as np


# Script to assess random cloud distributions for an ideal flight path in Miami for clear skies

# Central Canada
latitude = 55
longitude = -100
time_zone = 'America/Winnipeg'

start_hour = 6
duration = 2

# Recorded Cloud Data from Miami
file = [
    # Day 1
    pd.read_csv('../../../data/cloud_data/cloud_data_winnipeg/cloud_cover_11_22_13.csv'),
    pd.read_csv('../../../data/cloud_data/cloud_data_winnipeg/cloud_cover_17_22_22.csv'),
    pd.read_csv('../../../data/cloud_data/cloud_data_winnipeg/cloud_cover_23_22_37.csv'),
    # Day 2
    pd.read_csv('../../../data/cloud_data/cloud_data_winnipeg/cloud_cover_05_22_45.csv'),
    pd.read_csv('../../../data/cloud_data/cloud_data_winnipeg/cloud_cover_11_23_00.csv'),
]

# Ideal flight path for clear skies in Miami
points = np.array(([115000, 115000], [0, 120000],
                   [-115000, 115000], [0, 0]))

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=file,
    points=points,
)

file_name = '../../../data/monte_carlo_results/examples/winnipeg_current_forecast_200.txt'
no_sims = 200

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
)

monte_carlo.run()
