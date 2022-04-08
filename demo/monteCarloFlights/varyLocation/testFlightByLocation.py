from src.probabilityForecast import ProbabilityForecast
import pandas as pd

# Location 1 - Latitude Band 85 to 70
# Barrow, Alaska Lat: 70, Long: -155

# Location 2 - Latitude Band 65 to 50
# London, UK Lat: 50, Long: 0

# Location 3 - Latitude Band 45 to 30
# Los Angeles Lat: 35, Long: -120

# Location 4 - Latitude Band 25 to 10
# Mexico City Lat: 20, Long: -100

# Location 5 - Latitude Band 5 to -10
# Singapore Lat: 0, Long: 105

# Location 6 - Latitude Band -15 to -30
# Brisbane Lat: -25, Long: 155

# Location 7 - Latitude Band -35 to -55
# Melbourne Lat: -40, Long: 145

# Location 8 - Latitude Band -35 to -55
# Ushuaia Lat: -55, Long: -70

p = ProbabilityForecast(
    file=[
        # pd.read_csv('../../../data/general_cloud_data/low_cloud_data.csv'),
        #   pd.read_csv('../../../data/general_cloud_data/lowmed_cloud_data.csv'),
        #   pd.read_csv('../../../data/general_cloud_data/med_cloud_data.csv')
          pd.read_csv('../../../data/general_cloud_data/med_cloud_data.csv'),
          pd.read_csv('../../../data/general_cloud_data/medhigh_cloud_data.csv'),
          pd.read_csv('../../../data/general_cloud_data/high_cloud_data.csv')
          ],
    plot_results=True,
)

p.generate_data()