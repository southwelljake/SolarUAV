import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta


class ProbabilityForecast:
    def __init__(self,
                 file: list,
                 plot_results: bool = False):

        self.file = file
        self.plot_results = plot_results

        # First time to be used as the first time of the last reading
        self.first_time = pd.Timestamp(self.file[-1].values[0, 0])

        # Last time to be used as the last time of the first reading
        self.last_time = pd.Timestamp(self.file[0].values[-1, 0])

        time_diff_start = pd.Timestamp(self.file[-1].values[0, 0]) - pd.Timestamp(self.file[0].values[0, 0])

        # If data from multiple days
        if time_diff_start.components.days > 0:
            self.start_hour = time_diff_start.components.days * 24 + time_diff_start.components.hours
            no_days = np.ceil((pd.Timestamp(self.file[0].values[-1, 0]) -
                       pd.Timestamp(self.file[0].values[0, 0])).components.days +
                       (pd.Timestamp(self.file[0].values[-1, 0]) -
                       pd.Timestamp(self.file[0].values[0, 0])).components.hours / 24)
            end_hour = ((no_days - 1) * 24) + self.start_hour - 3

            if self.first_time.tz.zone == 'UTC':
                end_hour += 3

            self.time = np.linspace(self.start_hour, end_hour, int((end_hour - self.start_hour) / 3 + 1))

            self.total_clouds = np.zeros((len(self.file), len(self.time)))

            self.cloud_cover = np.array([[0.0, 0.0]] * (3 * len(self.time) - 2))
            # self.cloud_cover = np.array([[0.0, 0.0]] * len(self.time))

            self.mean_total = np.zeros(len(self.time))
            self.var_total = np.zeros(len(self.time))
            self.sd_total = np.zeros(len(self.time))
            self.a = np.zeros(len(self.time))
            self.b = np.zeros(len(self.time))
        else:
            self.start_hour = 0
            no_days = (pd.Timestamp(self.file[0].values[-1, 0]) - pd.Timestamp(
                self.file[0].values[0, 0])).components.days
            end_hour = (no_days + 1) * 24 - 3

            if self.first_time.tz.zone == 'UTC':
                end_hour -= 3

            self.time = np.linspace(self.start_hour, end_hour, int((end_hour - self.start_hour) / 3 + 1))

            self.total_clouds = np.zeros((len(self.file), len(self.time)))

            self.cloud_cover = np.array([[0.0, 0.0]] * (3 * len(self.time) - 2))

            self.mean_total = np.zeros(len(self.time))
            self.var_total = np.zeros(len(self.time))
            self.sd_total = np.zeros(len(self.time))
            self.a = np.zeros(len(self.time))
            self.b = np.zeros(len(self.time))

    def generate_data(self):

        for i in range(0, len(self.file)):
            # Calculate start time
            start = pd.Timestamp(self.file[i].values[0, 0])
            start_diff = self.first_time - start
            start_index = start_diff.components.days * 8 + start_diff.components.hours / 3

            # Calculate end time
            end = pd.Timestamp(self.file[i].values[-1, 0])
            end_diff = self.last_time - end
            end_index = len(self.file[i].values[:, 0]) - \
                abs((end_diff.components.days * 8 + end_diff.components.hours / 3))

            # Store overlapping data in total_clouds
            self.total_clouds[i, :] = self.file[i].values[int(start_index):int(end_index), 6] / 100

        for j in range(0, len(self.time)):
            self.mean_total[j] = np.sum(self.total_clouds, axis=0)[j] / len(self.file)
            self.var_total[j] = np.var(self.total_clouds, axis=0)[j]
            self.sd_total[j] = np.sqrt(self.var_total[j])

            if self.var_total[j] > 0:
                self.a[j] = self.mean_total[j] * (self.mean_total[j] * (1 - self.mean_total[j]) / self.var_total[j] - 1)
                self.b[j] = (1 - self.mean_total[j]) * (self.mean_total[j] * (1 - self.mean_total[j]) /
                                                        self.var_total[j] - 1)

                samples = np.random.beta(self.a[j], self.b[j], 1)
                self.cloud_cover[3 * j, 0] = 3 * j
                self.cloud_cover[3 * j, 1] = samples[0] * 100
            else:
                self.cloud_cover[3 * j, 0] = 3 * j
                self.cloud_cover[3 * j, 1] = self.mean_total[j] * 100

        for k in range(0, len(self.time) - 1):
            self.cloud_cover[3 * k + 1, 0] = 3 * k + 1
            self.cloud_cover[3 * k + 2, 0] = 3 * k + 2
            self.cloud_cover[3 * k + 1, 1] = (self.cloud_cover[3 * k + 3, 1] - self.cloud_cover[3 * k, 1]) / 3 + \
                self.cloud_cover[3 * k, 1]
            self.cloud_cover[3 * k + 2, 1] = 2 * (self.cloud_cover[3 * k + 3, 1] - self.cloud_cover[3 * k, 1]) / 3 + \
                self.cloud_cover[3 * k, 1]

        if self.plot_results:
            self.plot()

    def plot(self):
        fig, ax = plt.subplots()

        for k in range(0, len(self.file)):
            ax.plot(self.time, self.total_clouds[k, :] * 100, label='+' + str(k * 6) + ' hours')
        ax.set_xlabel('Time (hrs)')
        ax.set_ylabel('Cloud Cover (%)')
        ax.set_title('Total Cloud Cover')
        ax.set_ylim([-5, 105])
        ax.legend()

        fig2, ax2 = plt.subplots()

        ax2.plot(self.time, self.mean_total * 100, label='Mean')
        ax2.plot(self.time, self.sd_total * 100, label='SD')
        ax2.set_xlabel('Time (hrs)')
        ax2.set_ylabel('Cloud Cover (%)')
        ax2.set_title('Total Cloud Cover')
        ax2.set_ylim([-5, 105])
        ax2.legend()

        fig3, ax3 = plt.subplots()

        ax3.set_title('Random Sample Cloud Cover')
        ax3.set_xlabel('Time (hrs)')
        ax3.set_ylabel('Cloud Cover (%)')
        ax3.plot(self.cloud_cover[:, 0] + self.start_hour, self.cloud_cover[:, 1])
        ax3.set_ylim([-5, 105])

        # fig4, ax4 = plt.subplots()
        #
        # ax4.plot(beta.pdf(np.linspace(0, 1, 100), self.a[5], self.b[5]))
        # ax4.plot([self.total_clouds[0, 5] * 100, self.total_clouds[1, 5] * 100, self.total_clouds[2, 5] * 100,
        #          self.total_clouds[3, 5] * 100, self.total_clouds[4, 5] * 100], [0, 0, 0, 0, 0], 'xr')
        # ax4.set_xlabel('Cloud Cover (%)')
        # ax4.set_ylabel('PDF')

        plt.show()
