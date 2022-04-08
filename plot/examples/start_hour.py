from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity('../../data/monte_carlo_results/examples/start_hour_sensitivity_200.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    if p.outcome[result]:
        ax1.bar(p.variables[result][0], [1], width=0.05, color='blue')
    else:
        ax1.bar(p.variables[result][0], [0.1], width=0.05, color='red')

ax1.set_xlabel('Start hour')
ax1.axes.yaxis.set_visible(False)

true = mlines.Line2D([], [], color='blue', marker='o', markersize=5, label='Successful')
false = mlines.Line2D([], [], color='red', marker='o', markersize=5, label='Unsuccessful')
ax1.legend(handles=[true, false])

plt.show()
