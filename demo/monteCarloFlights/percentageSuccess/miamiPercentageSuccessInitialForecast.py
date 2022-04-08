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

# Miami
latitude = 25.7617
longitude = 80.1918
time_zone = 'EST'

start_hour = 6
duration = 2

# Recorded Cloud Data from Miami
file = [
        # Day 1
        pd.read_csv('../../../data/cloud_data/cloud_data_miami/cloud_cover_11_18_29.csv'),
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
    date=datetime.date(2022, 3, 17),
)

file_name = '../../../data/monte_carlo_results/percentageSuccess/miami_percentage_success_initial_250.txt'
no_sims = 250

other_variables = [['flight_model.start_time', [24, 48], 'float']]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
