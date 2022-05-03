from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
from src.generatePaths import GeneratePaths
import pandas as pd
import numpy as np
import datetime

# Singapore
latitude = 0
longitude = 105
time_zone = 'Singapore'

cloud_data = [
    pd.read_csv('../../../data/cloud_data/singapore_april/singapore_13_40_33.csv'),
]

start_hour = 24
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

file_name = '../../../data/monte_carlo_results/timeOnTarget/singapore_target_distance_500.txt'
no_sims = 500

other_variables = [['flight_model.yaw.path.points[0][1]', [1000, 550000], 'float']]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
