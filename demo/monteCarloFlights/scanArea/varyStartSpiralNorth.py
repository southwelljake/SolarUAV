from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
from src.generatePaths import GeneratePaths
import datetime

path = GeneratePaths(
    shape='s',
    start_point=[0, 50000],
    scanning_range=1000,
    scanning_width=50000,
    direction='n',
)

# London
latitude = 51.5072
longitude = 0.1276
time_zone = 'GMT'

start_hour = 26
duration = 2

# Recorded Cloud Data from London
file = [
        # Day 1
        pd.read_csv('../../../data/cloud_data/cloud_data_london/cloud_cover_16_04_31.csv'),
        # pd.read_csv('../../data/cloud_data_london/cloud_cover_22_04_39.csv'),
        # # Day 2
        # pd.read_csv('../../data/cloud_data_london/cloud_cover_04_04_47.csv'),
        # pd.read_csv('../../data/cloud_data_london/cloud_cover_10_04_55.csv'),
        # pd.read_csv('../../data/cloud_data_london/cloud_cover_16_05_03.csv'),
        # pd.read_csv('../../data/cloud_data_london/cloud_cover_22_05_11.csv'),
]

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    date=datetime.date(2022, 3, 12),
    mission_type='p2p',
    cloud_data=file,
    path=path,
)

file_name = '../../../data/monte_carlo_results/scanArea/start_spiral_north_250.txt'
no_sims = 250

other_variables = [['flight_model.yaw.path.width', [5000, 100000], 'int'],
                   ['flight_model.yaw.path.start_point[1]', [5000, 100000], 'int']]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
