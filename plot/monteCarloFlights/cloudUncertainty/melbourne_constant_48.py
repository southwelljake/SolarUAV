from src.processSensitivity import ProcessSensitivity
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

p = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_0.txt')
p1 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_1.txt')
p2 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_2.txt')
p3 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_3.txt')
p4 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_4.txt')
p5 = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_5.txt')

# Plot results
fig1, ax1 = plt.subplots()

outcome = []
outcome1 = []
outcome2 = []
outcome3 = []
outcome4 = []
outcome5 = []


for result in range(0, p.no_sims):
    outcome.append(p.outcome[result])
for result in range(0, p1.no_sims):
    outcome1.append(p1.outcome[result])
for result in range(0, p2.no_sims):
    outcome2.append(p2.outcome[result])
for result in range(0, p3.no_sims):
    outcome3.append(p3.outcome[result])
for result in range(0, p4.no_sims):
    outcome4.append(p4.outcome[result])
for result in range(0, p5.no_sims):
    outcome5.append(p5.outcome[result])

ax1.plot(outcome, [0 for i in range(0, len(outcome))], 'xC0')
ax1.plot(outcome1, [1 for i in range(0, len(outcome1))], 'xC1')
ax1.plot(outcome2, [2 for i in range(0, len(outcome2))], 'xC2')
ax1.plot(outcome3, [3 for i in range(0, len(outcome3))], 'xC3')
ax1.plot(outcome4, [4 for i in range(0, len(outcome4))], 'xC4')
ax1.plot(outcome5, [5 for i in range(0, len(outcome5))], 'xC5')

one = mlines.Line2D([], [], color='C0', marker='x', markersize=5, label='$\sigma$=0.00')
two = mlines.Line2D([], [], color='C1', marker='x', markersize=5, label='$\sigma$=0.05')
three = mlines.Line2D([], [], color='C2', marker='x', markersize=5, label='$\sigma$=0.10')
four = mlines.Line2D([], [], color='C3', marker='x', markersize=5, label='$\sigma$=0.15')
five = mlines.Line2D([], [], color='C4', marker='x', markersize=5, label='$\sigma$=0.20')
six = mlines.Line2D([], [], color='C5', marker='x', markersize=5, label='$\sigma$=0.25')
ax1.legend(handles=[one, two, three, four, five, six])
ax1.set_title('Melbourne 3/4/22')
ax1.set_xlabel('Percentage Complete (%)')
ax1.yaxis.set_major_locator(ticker.NullLocator())

fig2, ax2 = plt.subplots()

x = [0, 0.05, 0.1, 0.15, 0.2, 0.25]
y = []
y1 = []
y2 = []

mean = np.mean(outcome)
sd = np.sqrt(np.var(outcome))
y.append(mean)
y1.append(mean + sd)
y2.append(mean - sd)
mean = np.mean(outcome1)
sd = np.sqrt(np.var(outcome1))
y.append(mean)
y1.append(mean + sd)
y2.append(mean - sd)
mean = np.mean(outcome2)
sd = np.sqrt(np.var(outcome2))
y.append(mean)
y1.append(mean + sd)
y2.append(mean - sd)
mean = np.mean(outcome3)
sd = np.sqrt(np.var(outcome3))
y.append(mean)
y1.append(mean + sd)
y2.append(mean - sd)
mean = np.mean(outcome4)
sd = np.sqrt(np.var(outcome4))
y.append(mean)
y1.append(mean + sd)
y2.append(mean - sd)
mean = np.mean(outcome5)
sd = np.sqrt(np.var(outcome5))
y.append(mean)
y1.append(mean + sd)
y2.append(mean - sd)
ax2.set_title('Melbourne 3/4/22')
ax2.plot(x, y, label='Mean Value')
ax2.plot(x, y1, '--', label='Mean +$\sigma$')
ax2.plot(x, y2, '--', label='Mean -$\sigma$')
ax2.legend()
ax2.set_xlabel('Cloud Cover Uncertainty')
ax2.set_ylabel('Percentage Complete (%)')

plt.show()
