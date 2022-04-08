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
from src.probabilityForecast import ProbabilityForecast
from src.generatePaths import GeneratePaths
import datetime


class Simulation:
    def __init__(self,
                 latitude: float,
                 longitude: float,
                 time_zone: str,
                 start_hour: float,
                 duration: int,
                 path: GeneratePaths,
                 date: datetime.date = datetime.date.today(),
                 mission_type: str = 'p2p',
                 cloud_data: list = None,
                 abort_mission: bool = True,
                 abort_time: float = None,
                 ):

        self.latitude = latitude
        self.longitude = longitude
        self.time_zone = time_zone
        self.start_hour = start_hour
        self.duration = duration
        self.path = path
        self.cloud_data = cloud_data
        self.date = date
        self.mission_type = mission_type
        self.abort_mission = abort_mission
        self.abort_time = abort_time

    def generate(self):
        path = GeneratePaths(
            shape=self.path.shape,
            start_point=self.path.start_point,
            scanning_range=self.path.range,
            scanning_width=self.path.width,
            scanning_length=self.path.length,
            direction=self.path.direction,
            points=self.path.points,
        )

        solar_model = SolarModel(
            longitude=self.longitude,
            latitude=self.latitude,
            time_zone=self.time_zone,
            date=self.date,
            days=self.duration,
        )

        solar_model.generate_data()

        # Cloud Cover Model
        cloud_cover = CloudCover(
            longitude=self.longitude,
            latitude=self.latitude,
            time_zone=self.time_zone,
            date=self.date,
            days=self.duration,
        )

        if self.cloud_data is None:
            cloud_cover.generate_data()
            cloud_cover.process_data()
        else:
            probability_forecast = ProbabilityForecast(file=self.cloud_data)
            probability_forecast.generate_data()
            cloud_cover.cloud_cover = probability_forecast.cloud_cover

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
            path=path,
            tolerance=100,
            radius_land=2000,
            radius_target=2000,
            mission_type=self.mission_type,
            abort_mission=self.abort_mission,
            abort_time=self.abort_time
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
            solar_model=solar_model,
            cloud_cover=cloud_cover,
            solar_panel=solar_panel,
            wing=wing,
            yaw=yaw
        )

        return flight_model
