from src.processSensitivity import ProcessSensitivity
from src.probabilityForecast import ProbabilityForecast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines

p = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_random_46to56_200.txt')
p2 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_current_46_56.txt')

random_hour = []
random_percentage = []
current_hour = []
current_percentage = []

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    random_hour.append(p.variables[result][0])
    random_percentage.append(p.outcome[result])

for result in range(0, p2.no_sims):
    current_hour.append(p2.variables[result][0])
    current_percentage.append(p2.outcome[result])

ax1.plot(random_hour, random_percentage, 'xC0', label='Sampled Forecast')
ax1.plot(current_hour, current_percentage, 'xr', label='Initial Forecast')

ax1.set_xlabel('Start time (hrs)')
ax1.set_ylabel('Percentage Complete (%)')
ax1.legend()
#
# true = mlines.Line2D([], [], color='blue', marker='x', markersize=5, label='Sampled Cloud Forecast')
# false = mlines.Line2D([], [], color='red', marker='x', markersize=5, label='Initial Cloud Forecast')
# ax1.legend(handles=[true, false])
ax1.set_title('London 3/4/22')

plt.show()
