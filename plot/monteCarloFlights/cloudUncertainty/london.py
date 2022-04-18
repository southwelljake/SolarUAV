from src.processSensitivity import ProcessSensitivity
from src.probabilityForecast import ProbabilityForecast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines

p = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_random_200.txt')
p2 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_current_50.txt')
p3 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_random_200_2.txt')
p4 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_current_100_2.txt')

random_hour = []
random_percentage = []

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    random_hour.append(p.variables[result][0])
    random_percentage.append(p.outcome[result])
for result in range(0, p3.no_sims):
    random_hour.append(p3.variables[result][0])
    random_percentage.append(p3.outcome[result])

ax1.plot(random_hour, random_percentage, 'xC0')

for result in range(0, p2.no_sims):
    ax1.plot(p2.variables[result][0], p2.outcome[result], 'xr')
for result in range(0, p4.no_sims):
    ax1.plot(p4.variables[result][0], p4.outcome[result], 'xr')


ax1.set_xlabel('Start time (hrs)')
ax1.set_ylabel('Percentage Complete (%)')

true = mlines.Line2D([], [], color='C0', marker='x', markersize=5, label='Sampled Cloud Forecast')
false = mlines.Line2D([], [], color='red', marker='x', markersize=5, label='Initial Cloud Forecast')
ax1.legend(handles=[true, false])
ax1.set_title('London 3/4/22')
#
prob = ProbabilityForecast(file=[
    # Day 1
    pd.read_csv('../../../data/cloud_data/london_april/london_13_40_26.csv'),
    pd.read_csv('../../../data/cloud_data/london_april/london_19_40_34.csv'),
    # Day 2
    pd.read_csv('../../../data/cloud_data/london_april/london_01_40_44.csv'),
    pd.read_csv('../../../data/cloud_data/london_april/london_07_40_52.csv'),
    pd.read_csv('../../../data/cloud_data/london_april/london_13_41_01.csv'),
],
                        plot_results=True)
prob.generate_data()

# max_time = 120
# start_time = 0
# dt = 0.1
# intervals = int((max_time - start_time) / dt)
#
# p = []
#
# for i in range(0, intervals):
#     temp_p = []
#
#     for j in range(0, len(random_hour)):
#         if dt * i <= random_hour[j] < dt * (i + 1):
#             temp_p.append(random_percentage[j])
#
#     p.append(temp_p)
#
# mean = []
# sd = []
# time = []
#
# for k in range(0, len(p)):
#     if len(p[k]) > 0:
#         mean.append(np.mean(p[k]))
#         sd.append(np.sqrt(np.var(p[k])))
#         time.append(k * dt)
#
# fig, ax = plt.subplots()
# ax.plot(time, sd)
# # ax.plot([3 * i for i in range(0, len(prob.sd_total))], prob.sd_total)

plt.show()
