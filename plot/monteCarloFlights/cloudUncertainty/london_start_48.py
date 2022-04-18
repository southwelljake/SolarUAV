from src.processSensitivity import ProcessSensitivity
from src.probabilityForecast import ProbabilityForecast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines
from scipy.stats import beta

p = ProcessSensitivity('../../../data/monte_carlo_results/cloudUncertainty/london_start48_100.txt')

percentage = []

# Plot results
fig1, ax1 = plt.subplots()

for result in range(0, p.no_sims):
    percentage.append(p.outcome[result] / 100)

a = np.mean(percentage) * (np.mean(percentage) * (1 - np.mean(percentage)) / np.var(percentage) - 1)
b = (1 - np.mean(percentage)) * (np.mean(percentage) * (1 - np.mean(percentage)) / np.var(percentage) - 1)
x = np.linspace(0, 1, 100)
pdf = beta.pdf(x, a, b)

print(np.mean(percentage))
print(np.sqrt(np.var(percentage)))

ax1.plot(x * 100, pdf, 'C0', label='Start Hour 48')
ax1.plot([80.24], [0], 'rx')

ax1.set_ylabel('PDF')
ax1.set_xlabel('Cloud Cover (%)')
ax1.legend()
ax1.set_title('London 3/4/22')

plt.show()