import pandas as pd
from src.probabilityForecast import ProbabilityForecast

# Assume data is input in order recorded
file = [
    # Day 1
    pd.read_csv('../../data/cloud_data/cloud_data_miami/cloud_cover_11_18_29.csv'),
    pd.read_csv('../../data/cloud_data/cloud_data_miami/cloud_cover_17_18_37.csv'),
    pd.read_csv('../../data/cloud_data/cloud_data_miami/cloud_cover_23_18_46.csv'),
    # Day 2
    pd.read_csv('../../data/cloud_data/cloud_data_miami/cloud_cover_05_18_54.csv'),
    pd.read_csv('../../data/cloud_data/cloud_data_miami/cloud_cover_11_19_10.csv'),
]
#
# file = [
#     # Day 1
#     pd.read_csv('../data/cloud_data_winnipeg/cloud_cover_11_22_13.csv'),
#     pd.read_csv('../data/cloud_data_winnipeg/cloud_cover_17_22_22.csv'),
#     pd.read_csv('../data/cloud_data_winnipeg/cloud_cover_23_22_37.csv'),
#     # Day 2
#     pd.read_csv('../data/cloud_data_winnipeg/cloud_cover_05_22_45.csv'),
#     pd.read_csv('../data/cloud_data_winnipeg/cloud_cover_11_23_00.csv'),
# ]

# file = [
#     # Day 1
#     pd.read_csv('../data/cloud_data_london/cloud_cover_16_04_31.csv'),
#     pd.read_csv('../data/cloud_data_london/cloud_cover_22_04_39.csv'),
#     # Day 2
#     pd.read_csv('../data/cloud_data_london/cloud_cover_04_04_47.csv'),
#     pd.read_csv('../data/cloud_data_london/cloud_cover_10_04_55.csv'),
#     pd.read_csv('../data/cloud_data_london/cloud_cover_16_05_03.csv'),
#     pd.read_csv('../data/cloud_data_london/cloud_cover_22_05_11.csv'),
# ]

p = ProbabilityForecast(file=file, plot_results=True)
p.generate_data()
