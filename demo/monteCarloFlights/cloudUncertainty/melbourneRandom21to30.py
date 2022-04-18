from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
import numpy as np
import datetime
from src.generatePaths import GeneratePaths


path = GeneratePaths(
    points=np.array(([0, 0], [250000, 200000], [0, 300000],
                    [-250000, 200000], [0, 0])),
)

# Melbourne
latitude = -40
longitude = 145
time_zone = 'Australia/Melbourne'

start_hour = 21
duration = 7

# Recorded Cloud Data from Melbourne
file = [
        # Day 1
        pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_13_40_37.csv'),
        pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_19_40_48.csv'),
        # Day 2
        pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_01_40_58.csv'),
        pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_07_41_06.csv'),
        pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_13_41_15.csv'),
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
    abort_mission=False,
    date=datetime.date(2022, 4, 4),
)

file_name = '../../../data/monte_carlo_results/cloudUncertainty/melbourne_random_21to30_200.txt'
no_sims = 200

other_variables = [['flight_model.start_time', [21, 30], 'float']]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
