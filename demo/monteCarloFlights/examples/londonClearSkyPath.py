from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
import numpy as np


# Script to assess random cloud distributions for an ideal flight path in Miami for clear skies

# London
latitude = 51.5072
longitude = 0.1276
time_zone = 'GMT'

start_hour = 0
duration = 2

# Recorded Cloud Data from Miami
file = [
        # Day 1
        pd.read_csv('../../../data/cloud_data/cloud_data_london/cloud_cover_16_04_31.csv'),
        pd.read_csv('../../../data/cloud_data/cloud_data_london/cloud_cover_22_04_39.csv'),
        # Day 2
        pd.read_csv('../../../data/cloud_data/cloud_data_london/cloud_cover_04_04_47.csv'),
        pd.read_csv('../../../data/cloud_data/cloud_data_london/cloud_cover_10_04_55.csv'),
        pd.read_csv('../../../data/cloud_data/cloud_data_london/cloud_cover_16_05_03.csv'),
        pd.read_csv('../../../data/cloud_data/cloud_data_london/cloud_cover_22_05_11.csv'),
]

# Ideal flight path for clear skies in London
points = np.array(([200000, 175000], [0, 250000],
                   [-200000, 175000], [0, 0]))

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=file,
    points=points,
)

file_name = '../../../data/monte_carlo_results/examples/london_clear_sky_200_percentage.txt'
no_sims = 200

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
)

monte_carlo.run()
