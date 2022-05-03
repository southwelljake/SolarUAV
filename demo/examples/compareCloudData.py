import pandas as pd
from src.probabilityForecast import ProbabilityForecast

"""
Demo of reading cloud data and generating a sample.
"""

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

p = ProbabilityForecast(file=file, plot_results=True)
p.generate_data()
