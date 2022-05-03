from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
from src.generatePaths import GeneratePaths
import pandas as pd
import numpy as np
import datetime

# melbourne
latitude = -40
longitude = 145
time_zone = 'Australia/Melbourne'

cloud_data = [
    pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_13_40_37.csv'),
]

start_hour = 25
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
    mission_type='target',
    path=path,
    date=datetime.date(2022, 4, 3),
)

file_name = '../../../data/monte_carlo_results/timeOnTarget/melbourne_target_distance_500.txt'
no_sims = 500

other_variables = [['flight_model.yaw.path.points[0][1]', [1000, 550000], 'float']]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
