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

# London
latitude = 50
longitude = 0
time_zone = 'GMT'

start_hour = 0
duration = 7

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
    cloud_data=file,
    cloud_sd=0.1,
    path=path,
    mission_type='p2p',
    abort_mission=False,
    date=datetime.date(2022, 4, 4),
)

file_name = '../../../data/monte_carlo_results/cloudUncertainty/london_constant_0p1_24_30.txt'
no_sims = 50

other_variables = [['flight_model.start_time', [24, 30], 'float']]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
