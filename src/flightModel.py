from math import cos, pi, sin, sqrt
import numpy as np
import scipy.integrate as spi
from src.weather import Weather
from src.aeroCoeff import get_ClCd
from src.aircraft import Aircraft
from src.altitude import AltitudeController
from src.battery import Battery
from src.propeller import Propeller
from src.solarPanel import SolarPanel
from src.wing import Wing
from src.yaw import YawController


def hit_ground(t, state_var):
    # Terminal event when SUAV lands on the ground
    return state_var[2]


class FlightModel:
    def __init__(self,
                 start_time: float,
                 duration: float,
                 dt: float,
                 launch_velocity: list,
                 aircraft: Aircraft,
                 altitude: AltitudeController,
                 battery: Battery,
                 propeller: Propeller,
                 wing: Wing,
                 solar_panel: SolarPanel,
                 yaw: YawController,
                 weather: Weather,
                 ):

        # Initialise time parameters
        self.start_time = start_time  # Start time of flight (hrs)
        self.duration = duration  # Maximum duration for simulation (hrs)
        self.end_time = self.start_time + self.duration
        self.dt = dt

        # Initial Flight Conditions
        self.initial_position = [0, 0, 1]
        self.initial_velocity = launch_velocity
        self.gravity = 9.80665
        self.wind_x = 0  # Wind velocity in x-direction (m/s)
        self.wind_y = 0  # Wind velocity in y-direction (m/s)
        self.wind_z = 0  # Wind velocity in z-direction (m/s)

        # Initialise fixed parameters of aircraft and subsystem
        # General Aircraft
        self.aircraft = aircraft
        # Battery Properties
        self.battery = battery
        # Solar Panel Properties
        self.solar_panel = solar_panel
        # Propeller Properties
        self.propeller = propeller
        # Yaw Controller
        self.yaw = yaw
        # Altitude Controller
        self.altitude = altitude
        # Wing Parameters
        self.wing = wing
        self.wing.alpha = self.altitude.aoa_init
        self.wing.Cl, self.wing.Cd = get_ClCd(self.wing.alpha)
        # Weather Parameters
        self.weather = weather

        # Initialise time points in seconds, for ODE solver (starts from 0)
        self.t_prev = 0  # previous time point (in s)
        self.t_hrprev = 0  # previous time point (in hr)
        self.t_end = (self.duration + self.dt) * 3600
        self.t_ODE = np.arange(0, self.t_end, self.dt * 3600)
        self.t_prevint = 0  # previous time point (in s, as an integer)

        # Arrays for storing additional data
        self.tx = np.zeros(0, dtype=int)         # Time points in solver (in s, as an integer) for power data
        self.P_propx = np.zeros(0, dtype=int)    # Propelling power in simulation (in W)
        self.P_netx = np.zeros(0, dtype=int)     # Net power in simulation (in W)

        self.v_cruise = 0
        self.P_cruise = 0
        self.state_var = None
        self.sol_t = None

        # Define conditions for termination of simulation
        hit_ground.terminal = True
        hit_ground.direction = 0

        # Initially not collecting power data throughout simulation for lower run-time
        self.collect_power_data = False

    def calculate_cruise_power(self):
        self.wing.Cl, self.wing.Cd = get_ClCd(self.wing.alpha)

        self.v_cruise = sqrt(
            2 * self.aircraft.mass * self.gravity / (self.wing.density * self.wing.area * self.wing.Cl))  # cruise velocity

        # Cruise power
        self.P_cruise = 0.5 * \
            (self.wing.density * self.wing.area * self.wing.Cd * self.v_cruise ** 3) / self.propeller.efficiency

    def calculate_density(self, state_var):
        # Evaluate air density at current altitude
        if state_var[2] > 0:
            alt_lower = np.floor(state_var[2] / 1000)
            density_lower = self.wing.density_data[int(alt_lower), 1]
            alt_upper = np.ceil(state_var[2] / 1000)
            density_upper = self.wing.density_data[int(alt_upper), 1]
            self.wing.density = (density_upper - density_lower) * \
                (state_var[2] / 1000 - alt_lower) + density_lower

    def store_data(self, t, state_der):
        # Store propelling and net power data of simulation
        if self.collect_power_data:
            seconds_elapsed = int(np.floor(t))
            dt_int = seconds_elapsed - self.t_prevint
            if dt_int > 30:
                self.tx = np.append(self.tx, seconds_elapsed)
                self.P_propx = np.append(
                    self.P_propx, round(self.propeller.power, None))
                self.P_netx = np.append(self.P_netx, round(state_der[6], None))
                self.t_prevint = seconds_elapsed

    def calculate_solar(self, t):
        time_current = self.start_time + t / 3600  # in hours

        # Calculate power from solar panel
        self.solar_panel.power = self.weather.solar_model.calculate_solar_power(
            time_current, self.solar_panel.area, self.weather.cloud_cover.calculate_cloud_cover(time_current)
        ) * self.solar_panel.efficiency

    def calculate_wing_forces(self, v_air):
        # Compute drag and lift
        drag = 0.5 * self.wing.density * self.wing.area * self.wing.Cd * v_air ** 2
        lift = 0.5 * self.wing.density * self.wing.area * self.wing.Cl * v_air ** 2

        return drag, lift

    def calculate_propeller_thrust(self, v_air, state_var):
        # Compute thrust
        if v_air != 0 and state_var[6] > 0:
            thrust = abs(self.propeller.power) * self.propeller.efficiency / \
                v_air  # thrust from propeller
        else:
            thrust = 0

        return thrust

    def calculate_weather(self, t):
        if self.weather.weather_data.size:
            t_hr = np.floor(t / 3600) + self.start_time  # time in hours
            if int(t_hr - self.t_hrprev):
                t_hr = int(t_hr)
                self.t_hrprev = t_hr

                # Load weather data for next hour
                self.calculate_wind_vel(
                    self.weather.weather_data[t_hr, 1], self.weather.weather_data[t_hr, 2],
                    self.weather.weather_data[t_hr, 3])
                # self.cloud_cover = self.weather.weather_data[t_hr, 4]

    def calculate_wind_vel(self, vel, hor_angle, ver_angle):
        # define wind velocities - hor. angle is angle from y_gr, about z_gr, and ver. angle
        #  is resulting vector rotated from the horizontal plane

        hor_angle = hor_angle * pi / 180  # convert angle to rad
        ver_angle = ver_angle * pi / 180  # convert angle to rad
        self.wind_z = vel * sin(ver_angle)
        hor_wind = vel * cos(ver_angle)
        self.wind_x = - hor_wind * sin(hor_angle)
        self.wind_y = hor_wind * cos(hor_angle)

    def calculate_roll_angle(self, t, state_var, yaw):
        if not self.yaw.landing:
            if self.yaw.point_index == len(self.yaw.points):
                self.yaw.landing = True
                self.yaw.point_index = 0

            desired_yaw = - np.arctan2(self.yaw.points[self.yaw.point_index, 0] - state_var[0],
                                       self.yaw.points[self.yaw.point_index, 1] - state_var[1])

            distance = sqrt((self.yaw.points[self.yaw.point_index, 0] - state_var[0]) ** 2 +
                            (self.yaw.points[self.yaw.point_index, 1] - state_var[1]) ** 2)

        else:
            if self.yaw.point_index == len(self.yaw.end_circle):
                self.yaw.point_index = 0

            desired_yaw = - np.arctan2(self.yaw.end_circle[self.yaw.point_index, 0] - state_var[0],
                                       self.yaw.end_circle[self.yaw.point_index, 1] - state_var[1])

            distance = sqrt((self.yaw.end_circle[self.yaw.point_index, 0] - state_var[0]) ** 2 +
                            (self.yaw.end_circle[self.yaw.point_index, 1] - state_var[1]) ** 2)

        # Proportional controller
        dt = t - self.t_prev  # current time-step
        if dt > 0:
            # Evaluate roll angle based on the smaller difference between actual and demand path angle
            if desired_yaw < 0 < yaw:
                a = desired_yaw - yaw
                b = pi - yaw + pi + desired_yaw
                roll = a * self.yaw.kp if abs(a) < abs(b) else b * self.yaw.kp
            elif yaw < 0 < desired_yaw:
                a = desired_yaw - yaw
                b = - pi - yaw - pi + desired_yaw
                roll = a * self.yaw.kp if abs(a) < abs(b) else b * self.yaw.kp
            else:
                roll = self.yaw.kp * (desired_yaw - yaw)
            self.yaw.roll_prev = roll
        else:
            roll = self.yaw.roll_prev
        self.t_prev = t

        if distance < self.yaw.radius:
            self.yaw.point_index += 1

        return roll

    def calculate_propeller_power(self, state_var):
        # If landing
        if self.yaw.landing is True:
            self.wing.alpha = self.altitude.aoa_desc
            self.calculate_cruise_power()
            self.propeller.power = self.P_cruise * self.altitude.dsc_rate
        # If ascending
        elif state_var[2] < self.altitude.cruise_alt:
            self.wing.alpha = self.altitude.aoa_init
            self.calculate_cruise_power()
            self.propeller.power = self.P_cruise * self.altitude.asc_rate
        # If cruising
        else:
            self.wing.alpha = self.altitude.aoa_init
            self.calculate_cruise_power()
            self.propeller.power = self.P_cruise

    def calculate_derivatives(self, t, state_var):
        # State variables = [x, y, z, x', y', z', E]
        # State derivatives = [x'gr, y'gr, z'gr, x''gr, y''gr, z''gr, Pnet]
        state_der = np.zeros(7)

        # Compute current air speeds
        x_air = state_var[3] - self.wind_x
        y_air = state_var[4] - self.wind_y
        z_air = state_var[5] - self.wind_z
        v_airhor = sqrt(x_air ** 2 + y_air ** 2)
        v_air = sqrt(x_air ** 2 + y_air ** 2 +
                     z_air ** 2)

        # Compute ground speeds
        state_der[0] = state_var[3]
        state_der[1] = state_var[4]
        state_der[2] = state_var[5]

        # Compute angles
        yaw = -np.arctan2(x_air, y_air)
        climb_ang = np.arctan2(z_air, v_airhor)
        roll = self.calculate_roll_angle(t, state_var, yaw)

        self.calculate_weather(t)
        self.calculate_density(state_var)
        self.calculate_propeller_power(state_var)

        drag, lift = self.calculate_wing_forces(v_air)

        self.calculate_solar(t)

        state_der[6] = self.solar_panel.power - self.propeller.power - self.aircraft.P_other  # P net

        thrust = self.calculate_propeller_thrust(v_air, state_var)

        # If the SUAV is cruising
        if self.altitude.store_PE:
            # If the battery is fully charged and net energy is positive
            if state_var[6] >= self.battery.capacity and state_der[6] > 0:
                # If the altitude is below the maximum cruising altitude
                if state_var[2] < self.altitude.max_cruise_alt:
                    # Convert net power to thrust
                    thrust = abs(self.propeller.power + state_der[6]) * self.propeller.efficiency / v_air
                else:
                    self.calculate_cruise_power()
                    self.propeller.power = self.P_cruise
                # Remove net power from derivative
                state_der[6] = 0
            # If the net power is negative and the aircraft is above cruise altitude
            elif state_der[6] < 0 and state_var[2] > self.altitude.cruise_alt:
                self.propeller.power = self.P_cruise * 0.8
            # If the aircraft is below cruise altitude
            elif state_var[2] <= self.altitude.cruise_alt:
                self.propeller.power = self.P_cruise
        else:
            # Do not let the battery charge above full
            if state_var[6] >= self.battery.capacity and state_der[6] > 0:
                state_der[6] = 0

        # Prevent battery level going below zero
        if state_var[6] < 0:
            state_der[6] = 0 if state_der[6] < 0 else state_der[6]

        self.store_data(t, state_der)

        # Compute accelerations
        state_der[3] = -((thrust - drag) * cos(climb_ang) -
                         lift * sin(climb_ang)) * sin(yaw) / self.aircraft.mass - lift * sin(roll) * cos(yaw) / \
            self.aircraft.mass
        state_der[4] = ((thrust - drag) * cos(climb_ang) -
                        lift * sin(climb_ang)) * cos(yaw) / self.aircraft.mass - lift * sin(roll) * sin(yaw) / \
            self.aircraft.mass
        state_der[5] = (lift * cos(climb_ang) * cos(roll) + (thrust - drag) *
                        sin(climb_ang) - self.aircraft.mass * self.gravity) / self.aircraft.mass

        return state_der

    def sim_flight(self):
        ini_state_var = np.zeros(7)
        ini_state_var[0], ini_state_var[1], ini_state_var[2] = self.initial_position
        ini_state_var[3],  ini_state_var[4],  ini_state_var[5] = self.initial_velocity
        ini_state_var[6] = self.battery.level

        sol = spi.solve_ivp(self.calculate_derivatives, (0, self.t_end), ini_state_var, t_eval=self.t_ODE,
                            events=hit_ground, dense_output=False, rtol=1e-8)

        self.state_var = sol.y
        self.sol_t = sol.t / 3600 + self.start_time
        self.tx = self.tx / 3600 + self.start_time
