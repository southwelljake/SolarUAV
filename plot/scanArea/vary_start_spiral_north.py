from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

p = ProcessSensitivity(file_path='../../data/monte_carlo_results/scanArea/start_spiral_north_250.txt')

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    ax1.plot(p.variables[result][1] / p.variables[result][0], p.outcome[result], 'xb')


ax1.set_xlabel('Start Distance/Length of scan area')
ax1.set_ylabel('Percentage completed (%)')
#
# true = mlines.Line2D([], [], color='blue', marker='o', markersize=5, label='Successful')
# false = mlines.Line2D([], [], color='red', marker='o', markersize=5, label='Unsuccessful')
# ax1.legend(handles=[true, false])

plt.show()