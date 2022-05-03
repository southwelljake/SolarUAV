from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity('../../../data/monte_carlo_results/timeOnTarget/london_target_distance_500.txt')
p2 = ProcessSensitivity('../../../data/monte_carlo_results/timeOnTarget/melbourne_target_distance_500.txt')
p3 = ProcessSensitivity('../../../data/monte_carlo_results/timeOnTarget/singapore_target_distance_500.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    ax1.plot(float(p.variables[result][0]/1000), float(p.outcome[result]), 'xC0')
#
for result in range(0, p2.no_sims):
    ax1.plot(float(p2.variables[result][0]/1000), float(p2.outcome[result]), 'xC1')

for result in range(0, p3.no_sims):
    ax1.plot(float(p3.variables[result][0]/1000), float(p3.outcome[result]), 'xC2')

ax1.set_xlabel('Target Distance (km)')
ax1.set_ylabel('Time on target (hrs)')
lon = mlines.Line2D([], [], color='C0', marker='x', markersize=5, label='London')
mel = mlines.Line2D([], [], color='C1', marker='x', markersize=5, label='Melbourne')
sin = mlines.Line2D([], [], color='C2', marker='x', markersize=5, label='Singapore')
ax1.legend(handles=[lon, mel, sin])

plt.show()
