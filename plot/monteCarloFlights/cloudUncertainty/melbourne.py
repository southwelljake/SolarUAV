from src.processSensitivity import ProcessSensitivity
from src.probabilityForecast import ProbabilityForecast
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_random_200.txt')
p2 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_current_50.txt')
p3 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_random_200_2.txt')
p4 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_current_100_2.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    ax1.plot(p.variables[result][0], p.outcome[result], 'xC0')

for result in range(0, p3.no_sims):
    ax1.plot(p3.variables[result][0], p3.outcome[result], 'xC0')

for result in range(0, p2.no_sims):
    ax1.plot(p2.variables[result][0], p2.outcome[result], 'xr')

for result in range(0, p4.no_sims):
    ax1.plot(p4.variables[result][0], p4.outcome[result], 'xr')

ax1.set_xlabel('Start time (hrs)')
ax1.set_ylabel('Percentage Complete (%)')

true = mlines.Line2D([], [], color='C0', marker='x', markersize=5, label='Sampled Cloud Forecast')
false = mlines.Line2D([], [], color='red', marker='x', markersize=5, label='Initial Cloud Forecast')
ax1.legend(handles=[true, false])
ax1.set_title('Melbourne 3/4/22')

p = ProbabilityForecast(file=[
    # Day 1
    pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_13_40_37.csv'),
    pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_19_40_48.csv'),
    # Day 2
    pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_01_40_58.csv'),
    pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_07_41_06.csv'),
    pd.read_csv('../../../data/cloud_data/melbourne_april/melbourne_13_41_15.csv'),
],
                        plot_results=True)
p.generate_data()

plt.show()