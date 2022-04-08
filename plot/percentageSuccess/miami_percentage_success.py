from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity('../../data/monte_carlo_results/percentageSuccess/miami_percentage_success_500.txt')
p2 = ProcessSensitivity(
    '../../data/monte_carlo_results/percentageSuccess/miami_percentage_success_initial_250.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    ax1.plot(p.variables[result][0], p.outcome[result], 'xb')

for result in range(0, p2.no_sims):
    ax1.plot(p2.variables[result][0] - 24, p2.outcome[result], 'xr')

ax1.set_xlabel('Start time (hrs)')
ax1.set_ylabel('Percentage Complete (%)')

true = mlines.Line2D([], [], color='blue', marker='x', markersize=5, label='Sampled Cloud Forecast')
false = mlines.Line2D([], [], color='red', marker='x', markersize=5, label='Initial Cloud Forecast')
ax1.legend(handles=[true, false])
ax1.set_title('Miami 17/3/22')

plt.show()