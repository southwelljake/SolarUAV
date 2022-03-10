from src.flightModel import FlightModel
from src.aircraft import Aircraft
from src.altitude import AltitudeController
from src.battery import Battery
from src.propeller import Propeller
from src.solarPanel import SolarPanel
from src.solarModel import SolarModel
from src.wing import Wing
from src.yaw import YawController
from src.cloudCover import CloudCover
from src.weather import Weather
from src.probabilityForecast import ProbabilityForecast
from numpy import array
import pandas as pd


class Simulation:
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 time_zone: str,
                 start_hour: float,
                 duration: int,
                 ):

        self.latitude = latitude
        self.longitude = longitude
        self.time_zone = time_zone
        self.start_hour = start_hour
        self.duration = duration

    def generate(self):
        solar_model = SolarModel(
            longitude=self.longitude,
            latitude=self.latitude,
            time_zone=self.time_zone,
            days=3,
        )

        solar_model.generate_data()

        # Cloud Cover Model
        cloud_cover = CloudCover(
            longitude=self.longitude,
            latitude=self.latitude,
            time_zone=self.time_zone,
            days=3,
        )

        # cloud_cover.generate_data()
        # cloud_cover.data = pd.read_csv('../data/cloud_data_2/cloud_cover_17_58_55.csv')
        # cloud_cover.process_data()

        probability_forecast = ProbabilityForecast()
        probability_forecast.generate_data()

        cloud_cover.cloud_cover = probability_forecast.cloud_cover

        # Weather Data
        weather = Weather(
            solar_model=solar_model,
            cloud_cover=cloud_cover,
        )

        weather.generate_data()

        # Aircraft Properties
        aircraft = Aircraft(
            mass=18.2,
            power_other=10,
        )

        # Altitude Controller Properties
        altitude = AltitudeController(
            store_PE=False,
            cruise_alt=500,
            max_cruise_alt=8000,
            aoa_init=8.72,
            aoa_desc=1.41,
            asc_rate=1.6,
            dsc_rate=0.5,
        )

        # Battery Properties
        battery = Battery(
            initial_level=4590000,
            capacity=4590000,
        )

        # Propeller Properties
        propeller = Propeller(
            efficiency=0.72,
        )

        # Solar Panel Properties
        solar_panel = SolarPanel(
            efficiency=0.2,
            area=2.857,
        )

        # Wing Properties
        wing = Wing(
            area=2.857,
        )

        # Yaw Controller Properties
        yaw = YawController(
            kp=0.1,
            points=array(([150000, 150000], [0, 200000],
                          [-150000, 150000], [0, 0])),
            radius=100,
        )

        # Create Flight Model
        flight_model = FlightModel(
            start_time=self.start_hour,
            duration=self.duration * 24,
            dt=0.01,
            launch_velocity=[0, 15, 0],
            aircraft=aircraft,
            altitude=altitude,
            battery=battery,
            propeller=propeller,
            weather=weather,
            solar_panel=solar_panel,
            wing=wing,
            yaw=yaw
        )

        return flight_model
