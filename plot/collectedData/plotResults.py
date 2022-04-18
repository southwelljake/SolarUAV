from src.probabilityForecast import ProbabilityForecast
import pandas as pd

p = ProbabilityForecast(file=[
    # # Day 1
    # pd.read_csv('../../data/cloud_data/london_april/london_13_40_26.csv'),
    # pd.read_csv('../../data/cloud_data/london_april/london_19_40_34.csv'),
    # # Day 2
    # pd.read_csv('../../data/cloud_data/london_april/london_01_40_44.csv'),
    # pd.read_csv('../../data/cloud_data/london_april/london_07_40_52.csv'),
    # pd.read_csv('../../data/cloud_data/london_april/london_13_41_01.csv'),
    # Day 1
    pd.read_csv('../../data/cloud_data/melbourne_april/melbourne_13_40_37.csv'),
    pd.read_csv('../../data/cloud_data/melbourne_april/melbourne_19_40_48.csv'),
    # Day 2
    pd.read_csv('../../data/cloud_data/melbourne_april/melbourne_01_40_58.csv'),
    pd.read_csv('../../data/cloud_data/melbourne_april/melbourne_07_41_06.csv'),
    pd.read_csv('../../data/cloud_data/melbourne_april/melbourne_13_41_15.csv'),
],
                        plot_results=True)
p.generate_data()