from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
import numpy as np


# Central Canada
# latitude = 55
# longitude = -100
# time_zone = 'America/Winnipeg'

# London
# latitude = 51.5072
# longitude = 0.1276
# time_zone = 'GMT'

# Miami
latitude = 25.7617
longitude = 80.1918
time_zone = 'EST'

start_hour = 12
duration = 2

# Ideal flight path for clear skies in Miami
points = np.array(([205000, 200000], [0, 300000],
                   [-205000, 200000], [0, 0]))

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    points=points,
)

file_name = '../../../data/monte_carlo_results/examples/start_hour_sensitivity_200.txt'
no_sims = 200

other_variables = [['flight_model.start_time', [0, 24]]]

monte_carlo = MonteCarlo(
    simulation=sim,
    samples=no_sims,
    file_path=file_name,
    other_variables=other_variables,
)

monte_carlo.run()
