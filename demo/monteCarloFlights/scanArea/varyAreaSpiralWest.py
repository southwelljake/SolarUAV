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
    scanning_area=2500*10**6,
    direction='w',
)

# London
latitude = 50
longitude = 0
time_zone = 'GMT'

start_hour = 0
duration = 3

# Recorded Cloud Data from London
file = [
        # Day 1
        pd.read_csv('../../../data/cloud_data/london_april/london_13_40_26.csv'),
]

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    date=datetime.date(2022, 4, 4),
    mission_type='p2p',
    cloud_data=file,
    path=path,
)

file_name = '../../../data/monte_carlo_results/scanArea/spiralWest_50km.txt'
no_sims = 100

other_variables = [['flight_model.yaw.path.width', [5000, 100000], 'int']]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
