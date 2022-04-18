from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines


p = ProcessSensitivity('../../../data/monte_carlo_results/timeOnTarget/london_target_distance_300.txt')
p2 = ProcessSensitivity('../../../data/monte_carlo_results/timeOnTarget/melbourne_target_distance_300.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    ax1.plot(float(p.variables[result][0]/1000), float(p.outcome[result]), 'xb')
for result in range(0, p2.no_sims):
    ax1.plot(float(p2.variables[result][0]/1000), float(p2.outcome[result]), 'xg')

ax1.set_title('3/4/22, 2km Radius')
ax1.set_xlabel('Target Distance (km)')
ax1.set_ylabel('Time on target (hrs)')
ax1.legend()

plt.show()
