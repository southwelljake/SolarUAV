from src.simulation import Simulation
from src.monteCarlo import MonteCarlo
import pandas as pd
import numpy as np
import datetime
from src.generatePaths import GeneratePaths

# Location 7 - Latitude Band -35 to -55
# Melbourne Lat: -40, Long: 145
# Test flight path for each month at low cloud
latitude = -40
longitude = 145
time_zone = 'Australia/Melbourne'

start_hour = 0
duration = 2

cloud_data = [
    pd.read_csv('../../../../data/general_cloud_data/low_cloud_data.csv'),
    pd.read_csv('../../../../data/general_cloud_data/lowmed_cloud_data.csv'),
    pd.read_csv('../../../../data/general_cloud_data/med_cloud_data.csv')
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

    file_name = '../../../../data/monte_carlo_results/varyLocation/Melbourne/melbourne_low_cloud_' + str(m) + '.txt'
    no_sims = 10

    monte_carlo = MonteCarlo(
        simulation=sim,
        samples=no_sims,
        file_path=file_name,
    )

    monte_carlo.run()