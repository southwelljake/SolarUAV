from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity(file_path='../../../data/monte_carlo_results/scanArea/spiral_north_A2500.txt')
p2 = ProcessSensitivity(file_path='../../../data/monte_carlo_results/scanArea/spiral_north_A5000.txt')
p3 = ProcessSensitivity(file_path='../../../data/monte_carlo_results/scanArea/spiral_north_A7500.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    ax1.plot(p.variables[result][0] ** 2 / (2500*10**6), p.outcome[result], 'xC0')

for result in range(0, p2.no_sims):
    ax1.plot(p2.variables[result][0] ** 2 / (5000*10**6), p2.outcome[result], 'xC1')

for result in range(0, p3.no_sims):
    ax1.plot(p3.variables[result][0] ** 2 / (7500*10**6), p3.outcome[result], 'xC2')

ax1.set_xlabel('Width/Length of scan area')
ax1.set_ylabel('Percentage completed (%)')
ax1.set_title('Spiral North')

one = mlines.Line2D([], [], color='C0', marker='x', markersize=5, label='Area = 2500km$^2$')
two = mlines.Line2D([], [], color='C1', marker='x', markersize=5, label='Area = 5000km$^2$')
three = mlines.Line2D([], [], color='C2', marker='x', markersize=5, label='Area = 7500km$^2$')
ax1.legend(handles=[one, two, three])

plt.show()