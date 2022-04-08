from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity('../../data/monte_carlo_results/sensitivityTests/mass_energy_sensitivity_500.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    if p.outcome[result]:
        ax1.plot(p.variables[result][0], p.variables[result][1], 'ob')
    else:
        ax1.plot(p.variables[result][0], p.variables[result][1], 'or')

ax1.set_xlabel(p.variable_names[0])
ax1.set_ylabel(p.variable_names[1])

true = mlines.Line2D([], [], color='blue', marker='o', markersize=5, label='Successful')
false = mlines.Line2D([], [], color='red', marker='o', markersize=5, label='Unsuccessful')
ax1.legend(handles=[true, false])

plt.show()
