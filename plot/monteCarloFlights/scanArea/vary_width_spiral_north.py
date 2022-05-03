from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity(file_path='../../../data/monte_carlo_results/scanArea/spiralNorth_A5000.txt')
p2 = ProcessSensitivity(file_path='../../../data/monte_carlo_results/scanArea/zigzagNorth_A5000.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    ax1.plot(p.variables[result][0] ** 2 / (5000*10**6), p.outcome[result], 'xC0')

for result in range(0, p2.no_sims):
    ax1.plot(p2.variables[result][0] ** 2 / (5000*10**6), p2.outcome[result], 'xC1')

ax1.set_xlabel('Width/Length of scan area')
ax1.set_ylabel('Percentage completed (%)')

one = mlines.Line2D([], [], color='C0', marker='x', markersize=5, label='Spiral')
two = mlines.Line2D([], [], color='C1', marker='x', markersize=5, label='Up and Down')
ax1.legend(handles=[one, two])

plt.show()