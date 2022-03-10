import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import beta

file_1 = pd.read_csv('../data/cloud_data_2/cloud_cover_17_58_55.csv')
file_2 = pd.read_csv('../data/cloud_data_2/cloud_cover_23_59_00.csv')
file_3 = pd.read_csv('../data/cloud_data_2/cloud_cover_05_59_07.csv')
file_4 = pd.read_csv('../data/cloud_data_2/cloud_cover_11_59_15.csv')
file_5 = pd.read_csv('../data/cloud_data_2/cloud_cover_17_59_21.csv')

time = np.linspace(24, 72, 17)

total_clouds = np.zeros((5, 17))
total_clouds[0, :] = file_1.values[8:25, 6] / 100
total_clouds[1, :] = file_2.values[8:25, 6] / 100
total_clouds[2, :] = file_3.values[0:17, 6] / 100
total_clouds[3, :] = file_4.values[0:17, 6] / 100
total_clouds[4, :] = file_5.values[0:17, 6] / 100

mean_total = np.zeros(17)
var_total = np.zeros(17)
sd_total = np.zeros(17)
a = np.zeros(17)
b = np.zeros(17)
cloud_cover = np.array([[0.0, 0.0]] * len(time))

for i in range(0, len(time)):
    mean_total[i] = (total_clouds[0, i] + total_clouds[1, i] + total_clouds[2, i] + total_clouds[3, i] +
                     total_clouds[4, i]) / 5
    var_total[i] = ((total_clouds[0, i] - mean_total[i]) ** 2 + (total_clouds[1, i] - mean_total[i]) ** 2 +
                    (total_clouds[2, i] - mean_total[i]) ** 2 + (total_clouds[3, i] - mean_total[i]) ** 2 +
                    (total_clouds[4, i] - mean_total[i]) ** 2) / 5

    sd_total[i] = np.sqrt(var_total[i])
    a[i] = mean_total[i] * (mean_total[i] * (1 - mean_total[i]) / var_total[i] - 1)
    b[i] = (1 - mean_total[i]) * (mean_total[i] * (1 - mean_total[i]) / var_total[i] - 1)

    samples = np.random.beta(a[i], b[i], 1)
    cloud_cover[i, 0] = i
    cloud_cover[i, 1] = samples[0]

fig, ax = plt.subplots()

ax.plot(time, total_clouds[0, :], label='0 hours')
ax.plot(time, total_clouds[1, :], label='+6 hours')
ax.plot(time, total_clouds[2, :], label='+12 hours')
ax.plot(time, total_clouds[3, :], label='+18 hours')
ax.plot(time, total_clouds[4, :], label='+24 hours')
ax.set_xlabel('Time (hrs)')
ax.set_ylabel('Cloud Coverage')
ax.set_title('Total Cloud Cover')
ax.legend()

fig2, ax2 = plt.subplots()

ax2.plot(time, mean_total, label='Mean')
ax2.plot(time, sd_total, label='SD')
ax2.set_xlabel('Time (hrs)')
ax2.set_ylabel('Cloud Coverage')
ax2.set_title('Total Cloud Cover')
ax2.legend()

fig3, ax3 = plt.subplots()

ax3.plot(cloud_cover[:, 0], cloud_cover[:, 1])

plt.show()
