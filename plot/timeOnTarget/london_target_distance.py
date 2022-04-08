from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity('../../data/monte_carlo_results/timeOnTarget/london_target_distance_r2_200.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    ax1.plot(float(p.variables[result][0]/1000), float(p.outcome[result]), 'xb')

ax1.set_xlabel('Target Distance (km)')
ax1.set_ylabel('Time on target (hrs)')

plt.show()
