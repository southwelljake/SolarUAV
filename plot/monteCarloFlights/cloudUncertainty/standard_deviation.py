from src.processSensitivity import ProcessSensitivity
import matplotlib.pyplot as plt
import numpy as np

p = []
p.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_24_0.txt'))
p.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_24_1.txt'))
p.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_24_2.txt'))
p.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_24_3.txt'))
p.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_24_4.txt'))
p.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_24_5.txt'))

p2 = []
p2.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_0.txt'))
p2.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_1.txt'))
p2.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_2.txt'))
p2.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_3.txt'))
p2.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_4.txt'))
p2.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_72_5.txt'))

p3 = []
p3.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_30_0.txt'))
p3.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_30_1.txt'))
p3.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_30_2.txt'))
p3.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_30_3.txt'))
p3.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_30_4.txt'))
p3.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_constant_30_5.txt'))

p4 = []
p4.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_0_0.txt'))
p4.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_0_1.txt'))
p4.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_0_2.txt'))
p4.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_0_3.txt'))
p4.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_0_4.txt'))
p4.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_0_5.txt'))

p5 = []
p5.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_30_0.txt'))
p5.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_30_1.txt'))
p5.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_30_2.txt'))
p5.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_30_3.txt'))
p5.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_30_4.txt'))
p5.append(ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/melbourne_constant_30_5.txt'))

outcome = []
outcome2 = []
outcome3 = []
outcome4 = []
outcome5 = []
handles = []
sd = []
sd2 = []
sd3 = []
sd4 = []
sd5 = []

for i in range(0, 6):
    outcome.append([])
    for result in range(0, p[i].no_sims):
        outcome[i].append(p[i].outcome[result])

    outcome2.append([])
    for result in range(0, p2[i].no_sims):
        outcome2[i].append(p2[i].outcome[result])

    outcome3.append([])
    for result in range(0, p3[i].no_sims):
        outcome3[i].append(p3[i].outcome[result])

    outcome4.append([])
    for result in range(0, p4[i].no_sims):
        outcome4[i].append(p4[i].outcome[result])

    outcome5.append([])
    for result in range(0, p5[i].no_sims):
        outcome5[i].append(p5[i].outcome[result])

    sd.append(np.sqrt(np.var(outcome[i])))
    sd2.append(np.sqrt(np.var(outcome2[i])))
    sd3.append(np.sqrt(np.var(outcome3[i])))
    sd4.append(np.sqrt(np.var(outcome4[i])))
    sd5.append(np.sqrt(np.var(outcome5[i])))

fig2, ax2 = plt.subplots()

cc = [0, 0.05, 0.1, 0.15, 0.2, 0.25]

ax2.plot(cc, sd, label='London - Launch 24')
ax2.plot(cc, sd2, label='Melbourne - Launch 72')
ax2.plot(cc, sd3, label='London - Launch 30')
ax2.plot(cc, sd4, label='Melbourne - Launch 0')
ax2.plot(cc, sd5, label='Melbourne - Launch 30')
ax2.set_xlabel('Cloud Cover Uncertainty')
ax2.set_ylabel('Mission Standard Deviation (%)')
ax2.legend()

plt.show()
