from src.cloudCover import CloudCover
from src.solarModel import SolarModel
import numpy as np


class Weather:
    def __init__(self,
                 cloud_cover: CloudCover,
                 solar_model: SolarModel
                 ):

        self.solar_model = solar_model
        self.cloud_cover = cloud_cover

        self.weather_data = None

    def generate_data(self):
        # Generate weather data for 4 days - no cloud cover and no wind
        # weather_data is in the format [time elapsed(hrs), vel. magnitude(m/s),
        #                                vel. hor. angle(deg), vel. ver angle(deg), cc (%)]
        self.weather_data = np.zeros((1, 5))
        for i in range(0, 24):  # day 1
            weather_data_row = np.array([i, 0, 0, 0, 0])
            self.weather_data = np.vstack((self.weather_data, weather_data_row))
        self.weather_data = np.delete(self.weather_data, 0, 0)
        for i in range(24, 48):  # day 2
            weather_data_row = np.array([i, 0, 0, 0, 0])
            self.weather_data = np.vstack((self.weather_data, weather_data_row))
        for i in range(48, 96):  # day 3 n 4
            weather_data_row = np.array([i, 0, 0, 0, 0])
            self.weather_data = np.vstack((self.weather_data, weather_data_row))