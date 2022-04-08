from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
import numpy as np
import datetime
from src.generatePaths import GeneratePaths


path = GeneratePaths(
    points=np.array(([0, 0], [200000, 200000], [0, 300000],
                    [-200000, 200000], [0, 0])),
)

# London
latitude = 51.5072
longitude = 0.1276
time_zone = 'GMT'

start_hour = 1
duration = 2

# Recorded Cloud Data from London
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

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=file,
    path=path,
    mission_type='p2p',
    date=datetime.date(2022, 3, 12),
)

file_name = '../../../data/monte_carlo_results/percentageSuccess/london_percentage_success_longer_500.txt'
no_sims = 500

other_variables = [['flight_model.start_time', [0, 24], 'float']]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
