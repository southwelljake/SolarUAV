import pandas as pd
import datetime
from pvlib.forecast import GFS, NAM, NDFD, HRRR, RAP
import numpy as np
import math
import datetime


class CloudCover:
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 time_zone: str,
                 days: int,
                 date: datetime.date = datetime.date.today(),
                 ):

        self.latitude = latitude
        self.longitude = longitude
        self.time_zone = time_zone
        self.days = days
        self.date = date

        self.data = None
        self.cloud_cover = np.array([[0, 0]] * (days * 25 + 1))
        self.wind_data = np.array([[0, 0, 0, 0]] * (days * 25 + 1))

    def generate_data(self):

        start = pd.Timestamp(self.date, tz=self.time_zone)
        end = start + pd.Timedelta(days=self.days)

        model = GFS()

        self.data = model.get_processed_data(self.latitude, self.longitude, start, end)

    def process_data(self):
        self.process_cloud_data()
        # self.process_wind_data()

    def process_cloud_data(self):
        for i in range(0, len(self.cloud_cover)):
            self.cloud_cover[i, 0] = i

        total_cc = np.array(self.data['total_clouds'])

        for i in range(0, len(total_cc) - 1):
            self.cloud_cover[3 * i, 1] = total_cc[i]
            self.cloud_cover[3 * i + 1, 1] = (total_cc[i + 1] - total_cc[i]) / 3 + total_cc[i]
            self.cloud_cover[3 * i + 2, 1] = 2 * (total_cc[i + 1] - total_cc[i]) / 3 + total_cc[i]
        self.cloud_cover[3 * (len(total_cc) - 1), 1] = total_cc[len(total_cc) - 1]

    def process_wind_data(self):
        wind_vel = np.array(self.data['wind_speed'])

        for i in range(0, len(wind_vel) - 1):
            self.wind_data[3 * i, 1] = wind_vel[i]
            self.wind_data[3 * i + 1, 1] = (wind_vel[i + 1] - wind_vel[i]) / 3 + wind_vel[i]
            self.wind_data[3 * i + 2, 1] = 2 * (wind_vel[i + 1] - wind_vel[i]) / 3 + wind_vel[i]
        self.wind_data[3 * (len(wind_vel) - 1), 1] = wind_vel[len(wind_vel) - 1]

    def calculate_cloud_cover(self, time):
        time_upper = math.ceil(time)
        cc_upper = self.cloud_cover[time_upper, 1]
        time_lower = math.floor(time)
        cc_lower = self.cloud_cover[time_lower, 1]
        grad = cc_upper - cc_lower
        return grad * (time - time_lower) + cc_lower

    def calculate_wind_speed(self, time):
        # time_upper = math.ceil(time)
        # v_upper = self.wind_data[time_upper, 1]
        # time_lower = math.floor(time)
        # v_lower = self.wind_data[time_lower, 1]
        # grad = v_upper - v_lower
        # return grad * (time - time_lower) + v_lower
        return 0
