from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
from src.generatePaths import GeneratePaths
import pandas as pd
import numpy as np
import datetime

# London
latitude = -40
longitude = 145
time_zone = 'Australia/Melbourne'

cloud_data = [
    pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_13_40_37.csv'),
]

start_hour = 0
duration = 2

path = GeneratePaths(
    points=np.array(([0, 50000], [0, 0])),
)

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    cloud_data=cloud_data,
    path=path,
    mission_type='target',
    date=datetime.date(2022, 4, 4),
)

file_name = '../../../data/monte_carlo_results/timeOnTarget/melbourne_target_start_hour_200.txt'
no_sims = 200

other_variables = [['flight_model.start_time', [0, 120], 'float']]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
