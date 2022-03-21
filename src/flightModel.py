from math import cos, pi, sin, sqrt
import numpy as np
import scipy.integrate as spi
from src.weather import Weather
from src.aircraft import Aircraft
from src.altitude import AltitudeController
from src.battery import Battery
from src.propeller import Propeller
from src.solarPanel import SolarPanel
from src.wing import Wing
from src.yaw import YawController
import time


def hit_ground(t, state_var):
    # Terminal event when UAV lands on the ground
    return state_var[2]


def timeout(t, state_var):
    # Give the simulation a 2 minute time out period
    return 120 - state_var[7]


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
        # Calculate Cl and Cd
        self.calculate_aero_coeff()
        # Weather Parameters
        self.weather = weather

        # Initialise time points in seconds, for ODE solver (starts from 0)
        self.t_prev = 0  # Previous time point (in s)
        self.t_hrprev = 0  # Previous time point (in hr)
        self.t_end = (self.duration + self.dt) * 3600
        self.t_ODE = np.arange(0, self.t_end, self.dt * 3600)
        self.t_prevint = 0  # Previous time point (in s, as an integer)

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

        timeout.terminal = True
        timeout.direction = 0

        # Initially not collecting power data throughout simulation for lower run-time
        self.collect_power_data = False

        self.start_run = time.time()

    def calculate_cruise_power(self):
        self.calculate_aero_coeff()

        # Cruise velocity
        self.v_cruise = sqrt(
            2 * self.aircraft.mass * self.gravity / (self.wing.density * self.wing.area * self.wing.Cl))

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

    def calculate_aero_coeff(self):
        # Evaluate Lift and Drag coefficient at current angle of attack
        index = np.where(self.wing.aero_data == self.wing.alpha)
        self.wing.Cl, self.wing.Cd = float(self.wing.aero_data[index[0], 1]), float(self.wing.aero_data[index[0], 2])

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

    def calculate_wind_vel(self, t):
        time_current = self.start_time + t / 3600
        # mph to m/s
        vel = self.weather.cloud_cover.calculate_wind_speed(time_current) / 2.237
        hor_angle = 0
        ver_angle = 0
        hor_angle = hor_angle * pi / 180
        ver_angle = ver_angle * pi / 180
        self.wind_z = vel * sin(ver_angle)
        hor_wind = vel * cos(ver_angle)
        self.wind_x = - hor_wind * sin(hor_angle)
        self.wind_y = hor_wind * cos(hor_angle)

    def calculate_roll_angle(self, t, state_var, yaw):
        # Function to calculate required roll angle to follow desired flight path

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
        dt = t - self.t_prev  # Current time-step
        if dt > 0:
            # Evaluate roll angle based on the smaller difference between actual and demand path angle
            a = desired_yaw - yaw
            if desired_yaw < 0 < yaw:
                b = a + 2 * pi
                if abs(a) < abs(b):
                    roll = a * self.yaw.kp
                else:
                    roll = b * self.yaw.kp
            elif yaw < 0 < desired_yaw:
                b = a - 2 * pi
                if abs(a) < abs(b):
                    roll = a * self.yaw.kp
                else:
                    roll = b * self.yaw.kp
            else:
                roll = self.yaw.kp * a
            self.yaw.roll_prev = roll
        else:
            roll = self.yaw.roll_prev
        self.t_prev = t

        if distance < self.yaw.radius:
            self.yaw.point_index += 1

        return roll

    def calculate_propeller_power(self, state_var):
        # Function to calculate the required propelling power for different phases of flight

        # If landing
        if self.yaw.landing:
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

    def calculate_net_pe(self, state_var, state_der, thrust, v_air):
        # Function to convert net positive energy into potential energy (altitude)

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

        return state_var, state_der, thrust

    def calculate_derivatives(self, t, state_var):
        # State variables = [x, y, z, x', y', z', E]
        # State derivatives = [x'gr, y'gr, z'gr, x''gr, y''gr, z''gr, Pnet]
        state_der = np.zeros(8)

        self.calculate_wind_vel(t)

        # Compute current air speeds
        x_air = state_var[3] - self.wind_x
        y_air = state_var[4] - self.wind_y
        z_air = state_var[5] - self.wind_z
        v_airhor = sqrt(x_air ** 2 + y_air ** 2)
        v_air = sqrt(x_air ** 2 + y_air ** 2 + z_air ** 2)

        # Compute ground speeds
        state_der[0] = state_var[3]
        state_der[1] = state_var[4]
        state_der[2] = state_var[5]

        # Compute angles
        yaw = -np.arctan2(x_air, y_air)
        climb_ang = np.arctan2(z_air, v_airhor)
        roll = self.calculate_roll_angle(t, state_var, yaw)

        self.calculate_density(state_var)
        self.calculate_propeller_power(state_var)
        drag, lift = self.calculate_wing_forces(v_air)
        self.calculate_solar(t)

        state_der[6] = self.solar_panel.power - self.propeller.power - self.aircraft.P_other  # P net

        thrust = self.calculate_propeller_thrust(v_air, state_var)
        state_var, state_der, thrust = self.calculate_net_pe(state_var, state_der, thrust, v_air)

        self.store_data(t, state_der)

        # Prevent battery level going below zero
        if state_var[6] <= 0:
            state_der[6] = 0 if state_der[6] < 0 else state_der[6]

        # Compute accelerations
        state_der[3] = -((thrust - drag) * cos(climb_ang) -
                         lift * sin(climb_ang)) * sin(yaw) / self.aircraft.mass - lift * sin(roll) * cos(yaw) / \
            self.aircraft.mass
        state_der[4] = ((thrust - drag) * cos(climb_ang) -
                        lift * sin(climb_ang)) * cos(yaw) / self.aircraft.mass - lift * sin(roll) * sin(yaw) / \
            self.aircraft.mass
        state_der[5] = (lift * cos(climb_ang) * cos(roll) + (thrust - drag) *
                        sin(climb_ang) - self.aircraft.mass * self.gravity) / self.aircraft.mass

        state_var[7] = time.time() - self.start_run
        state_der[7] = 0

        return state_der

    def sim_flight(self):
        ini_state_var = np.zeros(8)
        ini_state_var[0], ini_state_var[1], ini_state_var[2] = self.initial_position
        ini_state_var[3], ini_state_var[4], ini_state_var[5] = self.initial_velocity
        ini_state_var[6] = self.battery.level
        ini_state_var[7] = time.time() - self.start_run

        try:
            sol = spi.solve_ivp(self.calculate_derivatives, (0, self.t_end), ini_state_var, t_eval=self.t_ODE,
                                events=[hit_ground, timeout], dense_output=False, method='RK45')

            self.state_var = sol.y
            self.sol_t = sol.t / 3600 + self.start_time
            self.tx = self.tx / 3600 + self.start_time
        except:
            print('Killed Simulation due to timeout')
