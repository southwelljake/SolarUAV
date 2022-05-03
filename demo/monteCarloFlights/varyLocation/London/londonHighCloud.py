from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
import numpy as np
import datetime
from src.generatePaths import GeneratePaths

# Location 2 - Latitude Band 65 to 50
# London, UK Lat: 50, Long: 0
# Test flight path for each month at low cloud
latitude = 50
longitude = 0
time_zone = 'Europe/London'

start_hour = 0
duration = 2

cloud_data = [
    pd.read_csv('../../../../data/general_cloud_data/med_cloud_data.csv'),
    pd.read_csv('../../../../data/general_cloud_data/medhigh_cloud_data.csv'),
    pd.read_csv('../../../../data/general_cloud_data/high_cloud_data.csv')
]

path = GeneratePaths(
    points=np.array(([0, 0], [250000, 200000], [0, 300000],
                    [-250000, 200000], [0, 0])),
)

months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

for m in months:

    sim = Simulation(
        latitude=latitude,
        longitude=longitude,
        time_zone=time_zone,
        start_hour=start_hour,
        duration=duration,
        cloud_data=cloud_data,
        path=path,
        mission_type='p2p',
        abort_mission=False,
        date=datetime.date(2021, m, 1),
    )

    file_name = '../../../../data/monte_carlo_results/varyLocation/London/london_high_cloud_' + str(m) + '.txt'
    no_sims = 25

    monte_carlo = MonteCarlo(
        simulation=sim,
        samples=no_sims,
        file_path=file_name,
    )

    monte_carlo.run()