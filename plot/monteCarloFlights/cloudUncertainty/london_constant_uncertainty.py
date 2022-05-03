from src.processSensitivity import ProcessSensitivity
from src.probabilityForecast import ProbabilityForecast
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_0p1_250.txt')
p2 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_0p05_250.txt')
p3 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_current_50.txt')
p4 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_current_100_2.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    ax1.plot(p.variables[result][0], p.outcome[result], 'xC0')
for result in range(0, p2.no_sims):
    ax1.plot(p2.variables[result][0], p2.outcome[result], 'xC1')

for result in range(0, p3.no_sims):
    ax1.plot(p3.variables[result][0], p3.outcome[result], 'xC2')
for result in range(0, p4.no_sims):
    ax1.plot(p4.variables[result][0], p4.outcome[result], 'xC2')


ax1.set_xlabel('Start time (hrs)')
ax1.set_ylabel('Percentage Complete (%)')

blue = mlines.Line2D([], [], color='C0', marker='x', markersize=5, label='$\sigma$=0.1')
green = mlines.Line2D([], [], color='C1', marker='x', markersize=5, label='$\sigma$=0.05')
red = mlines.Line2D([], [], color='C2', marker='x', markersize=5, label='$\sigma$=0')
ax1.legend(handles=[blue, green, red])
ax1.set_title('London 3/4/22')

p = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_0p1_24_30.txt')
p2 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_0p05_24_30.txt')
p3 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_current_24_30.txt')

# Plot results
fig2, ax2 = plt.subplots()

for result in range(0, p.no_sims):
    ax2.plot(p.variables[result][0], p.outcome[result], 'xC0')
for result in range(0, p2.no_sims):
    ax2.plot(p2.variables[result][0], p2.outcome[result], 'xC1')

for result in range(0, p3.no_sims):
    ax2.plot(p3.variables[result][0], p3.outcome[result], 'xC2')

ax2.set_xlabel('Start time (hrs)')
ax2.set_ylabel('Percentage Complete (%)')

blue = mlines.Line2D([], [], color='C0', marker='x', markersize=5, label='$\sigma$=0.1')
green = mlines.Line2D([], [], color='C1', marker='x', markersize=5, label='$\sigma$=0.05')
red = mlines.Line2D([], [], color='C2', marker='x', markersize=5, label='$\sigma$=0')
ax2.legend(handles=[blue, green, red])
ax2.set_title('London 3/4/22')

plt.show()