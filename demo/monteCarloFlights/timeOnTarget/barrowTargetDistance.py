from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
from src.generatePaths import GeneratePaths
import pandas as pd
import numpy as np
import datetime

# barrow
latitude = 70
longitude = -155
time_zone = 'America/Anchorage'

cloud_data = [
    pd.read_csv('../../../data/cloud_data/barrow_april/barrow_13_40_24.csv'),
]

start_hour = 48
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

file_name = '../../../data/monte_carlo_results/timeOnTarget/barrow_target_distance_300.txt'
no_sims = 300

other_variables = [['flight_model.yaw.path.points[0][1]', [1000, 300000], 'float']]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
