from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity(file_path='../../../data/monte_carlo_results/scanArea/zigzag_north_A5000.txt')
p2 = ProcessSensitivity(file_path='../../../data/monte_carlo_results/scanArea/spiral_north_A5000.txt')
p3 = ProcessSensitivity(file_path='../../../data/monte_carlo_results/scanArea/zigzag_north_A2500.txt')
p4 = ProcessSensitivity(file_path='../../../data/monte_carlo_results/scanArea/spiral_north_A2500.txt')
# Plot results
fig1, ax1 = plt.subplots(ncols=2)

for result in range(0, p.no_sims):
    ax1[0].plot(p.variables[result][0] ** 2 / (5000*10**6), p.outcome[result], 'xC0')

for result in range(0, p2.no_sims):
    ax1[0].plot(p2.variables[result][0] ** 2 / (5000*10**6), p2.outcome[result], 'xC1')

for result in range(0, p3.no_sims):
    ax1[1].plot(p3.variables[result][0] ** 2 / (2500*10**6), p3.outcome[result], 'xC0')

for result in range(0, p4.no_sims):
    ax1[1].plot(p4.variables[result][0] ** 2 / (2500*10**6), p4.outcome[result], 'xC1')

ax1[0].set_xlabel('Width/Length of scan area')
ax1[1].set_xlabel('Width/Length of scan area')
ax1[0].set_ylabel('Percentage completed (%)')
ax1[1].set_ylabel('Percentage completed (%)')
ax1[0].set_title('Area 5000km$^2$')
ax1[1].set_title('Area 2500km$^2$')

one = mlines.Line2D([], [], color='C0', marker='x', markersize=5, label='Up and Down')
two = mlines.Line2D([], [], color='C1', marker='x', markersize=5, label='Spiral')
ax1[0].legend(handles=[one, two])
ax1[1].legend(handles=[one, two])

plt.show()