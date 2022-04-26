import pandas as pd
from pvlib.location import Location
import datetime
import numpy as np
import math


class SolarModel:
    def __init__(self,
                 longitude: float,
                 latitude: float,
                 time_zone: str,
                 days: int,
                 date: datetime.date = datetime.date.today()
                 ):

        """
        Class to collect and process solar data to be used in FlightModel.

        :param latitude: Latitude (deg).
        :param longitude: Longitude (deg).
        :param time_zone: Time Zone in pytz format e.g. 'America/New_York'.
        :param days: Number of days to forecast for.
        :param date: Date of first day of forecast. Default as current day.
        """

        self.longitude = longitude
        self.latitude = latitude
        self.time_zone = time_zone
        self.days = days
        self.date = date

        self.cs = None
        # Default solar irradiance data
        # Solar irradiance (time (in hrs), solar irradiance (W/m2))
        self.slr_irr = np.array([[0, 0.], [1, 0.], [2, 0.], [3, 0.], [4, 0.], [5, 0.], [6, 132.], [7, 400.], [8, 700.],
                                 [9, 950.], [10, 1100.], [11, 1200.], [12, 1260], [13, 1200.], [14, 1100.], [15, 950.],
                                 [16, 700.], [17, 400.], [18, 132.], [19, 0.], [20, 0.], [21, 0.], [22, 0.], [23, 0.],
                                 [24, 0.]])

    def generate_data(self):
        # Replace the solar irradiance data based on selected co-ordinates, time-zone, and month.
        # Data from the 1st of selected month is used.
        loc = Location(self.latitude, self.longitude, self.time_zone)
        start = pd.Timestamp(self.date)
        end = start + pd.Timedelta(days=self.days)
        times = pd.date_range(start=start, end=end, freq='H', tz=self.time_zone)
        self.cs = loc.get_clearsky(times)
        ghi = np.array(self.cs['ghi'])
        self.slr_irr[:, 1] = ghi[0:25]

    def calculate_solar_power(self, time,  area, cc):
        while time >= 24:
            time -= 24
        time_upper = math.ceil(time)
        slr_irr_upper = self.slr_irr[time_upper, 1]
        time_lower = math.floor(time)
        slr_irr_lower = self.slr_irr[time_lower, 1]
        grad = slr_irr_upper - slr_irr_lower
        # Irradiance w/ clear sky
        I0 = grad * (time - time_lower) + slr_irr_lower
        # Irradiance w/ cloud cover
        I = I0 * (1 - 0.75 * (cc/100) ** 3.4)

        return I * area
