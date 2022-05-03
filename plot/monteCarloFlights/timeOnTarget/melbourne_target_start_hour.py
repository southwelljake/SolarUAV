from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt

p = ProcessSensitivity('../../../data/monte_carlo_results/timeOnTarget/melbourne_target_start_hour_200.txt')

# Plot results
fig1, ax1 = plt.subplots()

# for result in range(0, p.no_sims):
#     ax1.bar(p.variables[result][0], p.outcome[result], width=1, color='blue')

for result in range(0, p.no_sims):
    ax1.plot(float(p.variables[result][0]), float(p.outcome[result]), 'xC0')

ax1.set_xlabel('Start time (hrs)')
ax1.set_ylabel('Time on target (hrs)')

plt.show()
