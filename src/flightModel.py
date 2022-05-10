from math import cos, pi, sin, sqrt
import numpy as np
import scipy.integrate as spi
from src.aircraft import Aircraft
from src.altitude import AltitudeController
from src.battery import Battery
from src.propeller import Propeller
from src.solarPanel import SolarPanel
from src.wing import Wing
from src.yaw import YawController
from src.solarModel import SolarModel
from src.cloudCover import CloudCover
import time


def hit_ground(t, state_var):
    # Terminal event when UAV lands on the ground
    return state_var[2]


def timeout(t, state_var):
    # Give the simulation a 5 minute time out period
    return 300 - state_var[7]


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
                 solar_model: SolarModel,
                 cloud_cover: CloudCover,
                 ):

        """
        Class to execute the overall flight dynamics equations from connected subsystems.

        :param start_time: Launch hour for the simulation (hours).
        :param duration: Maximum flight duration (hours).
        :param dt: Time step for simulation results (hours).
        :param launch_velocity: Launch velocities (m/s).
        :param aircraft: Aircraft class.
        :param altitude: AltitudeController class.
        :param battery: Battery class.
        :param propeller: Propeller class.
        :param wing: Wing class.
        :param solar_panel: SolarPanel class.
        :param yaw: YawController class.
        :param solar_model: SolarModel class.
        :param cloud_cover: CloudCover class.
        """

        # Initialise time parameters
        self.start_time = start_time  # Start time of flight (hrs)
        self.duration = duration  # Maximum duration for simulation (hrs)
        self.end_time = self.start_time + self.duration
        self.dt = dt

        # Initial Flight Conditions
        self.initial_position = [0, 0, 1]
        self.initial_velocity = launch_velocity
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
        # Set initial aoa
        self.wing.alpha = self.altitude.aoa_init
        # Calculate Cl and Cd
        self.wing.calculate_aero_coeff()
        # Solar model
        self.solar_model = solar_model
        # Cloud Cover
        self.cloud_cover = cloud_cover

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

        # Variables for cruise conditions
        self.v_cruise = 0
        self.P_cruise = 0

        # Final output variables
        self.state_var = None
        self.sol_t = None

        # Define conditions for termination of simulation
        hit_ground.terminal = True
        hit_ground.direction = 0

        timeout.terminal = True
        timeout.direction = 0

        # Initially not collecting power data throughout simulation for lower run-time
        self.collect_power_data = False

        # Store time simulation begins
        self.start_run = time.time()

    def store_data(self, t, state_der):
        """
        Function to store propelling and net power data of simulation.
        """

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
        """
        Function to calculate solar power input at a given time.
        """

        # Current time in hours
        time_current = self.start_time + t / 3600

        # Calculate power from solar panel
        return self.solar_model.calculate_solar_power(
            time_current, self.solar_panel.area, self.cloud_cover.calculate_cloud_cover(time_current)
        ) * self.solar_panel.efficiency

    def calculate_abort_mission(self, t, state_var):
        """
        Function to determine when to abort a mission.
        """

        if self.yaw.abort_mission:
            # Function to calculate required roll angle to follow desired flight path
            # Allow an hour to land
            time_to_land = 3600
            energy_to_land = self.P_cruise * self.altitude.dsc_rate * time_to_land

            # Calculate current distance from end point
            distance_to_return = sqrt((state_var[0] - self.yaw.points[-1, 0]) ** 2 +
                                      (state_var[1] - self.yaw.points[-1, 1]) ** 2)

            # Calculate energy to cruise to end point
            if distance_to_return > 0:
                time_to_return = distance_to_return / self.v_cruise
                energy_to_return = self.P_cruise * time_to_return
            else:
                time_to_return = 0
                energy_to_return = 0

            # At point where the UAV must return if there is no further charging (within 5%)
            if state_var[6] - 0.05 * self.battery.capacity <= energy_to_return + energy_to_land and not \
                    self.yaw.returning:

                will_charge = False
                time = t/3600
                dt = 0.1
                net_energy = 0
                while time + self.start_time <= self.start_time + (t + time_to_return) / 3600:
                    net_energy += (
                        self.calculate_solar(time * 3600) - self.propeller.power - self.aircraft.P_other
                    ) * dt
                    time += dt

                if net_energy * 3600 + state_var[6] > 0.05 * self.battery.capacity:
                    will_charge = True

                if not will_charge:
                    self.yaw.returning = True
                    if self.yaw.mission_type == 'p2p':
                        self.yaw.calculate_distance_travelled(state_var)
                        self.yaw.point_index = len(self.yaw.points) - 1

    def calculate_propeller_power(self, state_var):
        """
        Function to calculate the required propelling power for different phases of flight.
        """

        # If landing
        if self.yaw.landing:
            self.wing.alpha = self.altitude.aoa_desc
            self.v_cruise, self.P_cruise = self.wing.calculate_cruise_power(self.propeller.efficiency,
                                                                            self.aircraft.mass)
            self.propeller.power = self.P_cruise * self.altitude.dsc_rate
        # If ascending
        elif state_var[2] < self.altitude.cruise_alt:
            self.wing.alpha = self.altitude.aoa_init
            self.v_cruise, self.P_cruise = self.wing.calculate_cruise_power(self.propeller.efficiency,
                                                                            self.aircraft.mass)
            self.propeller.power = self.P_cruise * self.altitude.asc_rate
        # If cruising
        else:
            self.wing.alpha = self.altitude.aoa_init
            self.v_cruise, self.P_cruise = self.wing.calculate_cruise_power(self.propeller.efficiency,
                                                                            self.aircraft.mass)
            self.propeller.power = self.P_cruise

    def calculate_net_pe(self, state_var, state_der, thrust, v_air):
        """
        Function to convert net positive energy into potential energy (altitude)
        """

        # If the SUAV is cruising
        if self.altitude.store_PE:
            # If the battery is fully charged and net energy is positive
            if state_var[6] >= self.battery.capacity and state_der[6] > 0:
                # If the altitude is below the maximum cruising altitude
                if state_var[2] < self.altitude.max_cruise_alt:
                    # Convert net power to thrust
                    thrust = abs(self.propeller.power + state_der[6]) * self.propeller.efficiency / v_air
                else:
                    self.wing.calculate_cruise_power(self.propeller.efficiency, self.aircraft.mass)
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
        """

        State variables = [x, y, z, x', y', z', E, time]
        State derivatives = [x'gr, y'gr, z'gr, x''gr, y''gr, z''gr, Pnet, time]
        """

        # Initialise state derivatives
        state_der = np.zeros(8)

        # Calculate wind speeds from data
        self.wind_x, self.wind_y, self.wind_z = self.cloud_cover.calculate_wind_vel(t, self.start_time)

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

        self.calculate_abort_mission(t, state_var)
        if self.yaw.mission_type == 'target':
            roll = self.yaw.calculate_roll_angle_target(t, self.initial_position, state_var, yaw)
        else:
            roll = self.yaw.calculate_roll_angle_p2p(t, state_var, yaw)

        self.wing.calculate_density(state_var)
        self.calculate_propeller_power(state_var)
        drag, lift = self.wing.calculate_wing_forces(v_air)
        self.solar_panel.power = self.calculate_solar(t)

        state_der[6] = self.solar_panel.power - self.propeller.power - self.aircraft.P_other  # P net

        thrust = self.propeller.calculate_propeller_thrust(v_air, state_var)
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
                        sin(climb_ang) - self.aircraft.mass * self.wing.gravity) / self.aircraft.mass

        state_var[7] = time.time() - self.start_run
        state_der[7] = 0

        return state_der

    def sim_flight(self):
        ini_state_var = np.zeros(8)
        ini_state_var[0], ini_state_var[1], ini_state_var[2] = self.initial_position
        ini_state_var[3], ini_state_var[4], ini_state_var[5] = self.initial_velocity
        ini_state_var[6] = self.battery.level
        ini_state_var[7] = time.time() - self.start_run

        # Create the flight path to simulate
        self.yaw.create_path()

        try:
            sol = spi.solve_ivp(self.calculate_derivatives, (0, self.t_end), ini_state_var, t_eval=self.t_ODE,
                                events=[hit_ground, timeout], dense_output=False, method='RK45')

            self.state_var = sol.y
            self.sol_t = sol.t / 3600 + self.start_time
            self.tx = self.tx / 3600 + self.start_time

            if not self.yaw.returning and self.yaw.landing:
                self.yaw.distance_travelled = self.yaw.total_distance
            elif not self.yaw.abort_mission and not self.yaw.landing:
                self.yaw.calculate_distance_travelled(self.state_var[:, -1])

        except:
            print('Killed Simulation')
