import pandas as pd
import datetime
from pvlib.forecast import GFS, NAM, NDFD, HRRR, RAP
import numpy as np
import math


class CloudCover:
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 time_zone: str,
                 days: int,
                 ):

        self.latitude = latitude
        self.longitude = longitude
        self.time_zone = time_zone
        self.days = days

        self.data = None
        self.cloud_cover = np.array([[0, 0]] * (days * 24 + 1))

    def generate_data(self):

        start = pd.Timestamp(datetime.date.today(), tz=self.time_zone)
        end = start + pd.Timedelta(days=self.days)

        model = GFS()

        self.data = model.get_processed_data(self.latitude, self.longitude, start, end)
        total_cc = np.array(self.data['total_clouds'])

        for i in range(0, 8 * self.days):
            self.cloud_cover[3 * i, 1] = total_cc[i]
            self.cloud_cover[3 * i + 1, 1] = (total_cc[i + 1] - total_cc[i]) / 3 + total_cc[i]
            self.cloud_cover[3 * i + 2, 1] = 2 * (total_cc[i + 1] - total_cc[i]) / 3 + total_cc[i]
        self.cloud_cover[24 * self.days, 1] = total_cc[8 * self.days]

    def calculate_cloud_cover(self, time):
        while time >= 24:
            time -= 24
        time_upper = math.ceil(time)
        cc_upper = self.cloud_cover[time_upper, 1]
        time_lower = math.floor(time)
        cc_lower = self.cloud_cover[time_lower, 1]
        grad = cc_upper - cc_lower
        return grad * (time - time_lower) + cc_lower
