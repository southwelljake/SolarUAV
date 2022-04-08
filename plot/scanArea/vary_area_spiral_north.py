from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity(file_path='../../data/monte_carlo_results/scanArea/spiralNorth_75.txt')
p2 = ProcessSensitivity(file_path='../../data/monte_carlo_results/scanArea/spiralNorth_50.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    ax1.plot(p.variables[result][0] / 1000, p.outcome[result], 'xb')

for result in range(0, p2.no_sims):
    ax1.plot(p2.variables[result][0] / 1000, p2.outcome[result], 'xg')


ax1.set_xlabel('Width & Length of scan area (km)')
ax1.set_ylabel('Percentage completed (%)')

true = mlines.Line2D([], [], color='blue', marker='x', markersize=5, label='50 km Start')
false = mlines.Line2D([], [], color='green', marker='x', markersize=5, label='75 km Start')
ax1.legend(handles=[true, false])

plt.show()