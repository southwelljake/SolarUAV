import pandas as pd
import numpy as np


class ProbabilityForecast:
    def __init__(self):

        self.file = [pd.read_csv('../data/cloud_data_2/cloud_cover_17_58_55.csv'),
                     pd.read_csv('../data/cloud_data_2/cloud_cover_23_59_00.csv'),
                     pd.read_csv('../data/cloud_data_2/cloud_cover_05_59_07.csv'),
                     pd.read_csv('../data/cloud_data_2/cloud_cover_11_59_15.csv'),
                     pd.read_csv('../data/cloud_data_2/cloud_cover_17_59_21.csv')]

        self.time = np.linspace(24, 72, 17)

        self.cloud_cover = np.array([[0.0, 0.0]] * (3 * len(self.time) - 2))

    def generate_data(self):
        total_clouds = np.zeros((len(self.file), len(self.time)))
        total_clouds[0, :] = self.file[0].values[8:25, 6] / 100
        total_clouds[1, :] = self.file[1].values[8:25, 6] / 100
        total_clouds[2, :] = self.file[2].values[0:17, 6] / 100
        total_clouds[3, :] = self.file[3].values[0:17, 6] / 100
        total_clouds[4, :] = self.file[4].values[0:17, 6] / 100

        mean_total = np.zeros(17)
        var_total = np.zeros(17)
        sd_total = np.zeros(17)
        a = np.zeros(17)
        b = np.zeros(17)

        for i in range(0, len(self.time)):
            mean_total[i] = (total_clouds[0, i] + total_clouds[1, i] + total_clouds[2, i] + total_clouds[3, i] +
                             total_clouds[4, i]) / 5
            var_total[i] = ((total_clouds[0, i] - mean_total[i]) ** 2 + (total_clouds[1, i] - mean_total[i]) ** 2 +
                            (total_clouds[2, i] - mean_total[i]) ** 2 + (total_clouds[3, i] - mean_total[i]) ** 2 +
                            (total_clouds[4, i] - mean_total[i]) ** 2) / 5

            sd_total[i] = np.sqrt(var_total[i])
            a[i] = mean_total[i] * (mean_total[i] * (1 - mean_total[i]) / var_total[i] - 1)
            b[i] = (1 - mean_total[i]) * (mean_total[i] * (1 - mean_total[i]) / var_total[i] - 1)

            samples = np.random.beta(a[i], b[i], 1)
            self.cloud_cover[3 * i, 0] = 3 * i
            self.cloud_cover[3 * i, 1] = samples[0] * 100

        for j in range(0, len(self.time) - 1):
            self.cloud_cover[3 * j + 1, 0] = 3 * j + 1
            self.cloud_cover[3 * j + 2, 0] = 3 * j + 2
            self.cloud_cover[3 * j + 1, 1] = (self.cloud_cover[3 * j + 3, 1] - self.cloud_cover[3 * j, 1]) / 3 + \
                self.cloud_cover[3 * j, 1]
            self.cloud_cover[3 * j + 2, 1] = 2 * (self.cloud_cover[3 * j + 3, 1] - self.cloud_cover[3 * j, 1]) / 3 + \
                self.cloud_cover[3 * j, 1]
