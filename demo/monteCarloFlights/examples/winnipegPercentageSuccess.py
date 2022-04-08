from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
import numpy as np
import datetime


# Script to assess random cloud distributions for an ideal flight path in Miami for clear skies

# Central Canada
latitude = 55
longitude = -100
time_zone = 'America/Winnipeg'

start_hour = 4
duration = 2

# Recorded Cloud Data from Miami
cloud_data = [
    # Day 1
    pd.read_csv('../../../data/cloud_data/cloud_data_winnipeg/cloud_cover_11_22_13.csv'),
    pd.read_csv('../../../data/cloud_data/cloud_data_winnipeg/cloud_cover_17_22_22.csv'),
    pd.read_csv('../../../data/cloud_data/cloud_data_winnipeg/cloud_cover_23_22_37.csv'),
    # Day 2
    pd.read_csv('../../../data/cloud_data/cloud_data_winnipeg/cloud_cover_05_22_45.csv'),
    pd.read_csv('../../../data/cloud_data/cloud_data_winnipeg/cloud_cover_11_23_00.csv'),
]

points = np.array(([0, 0], [150000, 150000], [0, 250000],
                   [-150000, 150000], [0, 0]))

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=cloud_data,
    points=points,
    mission_type='p2p',
    date=datetime.date(2022, 3, 12),
)

file_name = '../../../data/monte_carlo_results/examples/winnipeg_percentage_success_200.txt'
no_sims = 200

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
)

monte_carlo.run()
