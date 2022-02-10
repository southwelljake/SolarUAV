import numpy as np
from math import atan, sqrt, degrees, pi


class Wing:
    def __init__(self,
                 area: float,
                 polar_data: np.array,
                 density_data: np.array,
                 ):

        self.area = area
        self.polar_data = polar_data
        self.density_data = density_data

        # Input states
        self.ground_position = np.zeros((3, 1), dtype=np.float_)
        self.ground_velocity = np.zeros((3, 1), dtype=np.float_)
        self.air_velocity = np.zeros((3, 1), dtype=np.float_)
        self.body_rotation = np.zeros((3, 1), dtype=np.float_)

        # Output state
        self.force = np.zeros((3, 1), dtype=np.float_)

        self.density = 0
        self.climb_angle = 0
        self.yaw_angle = 0
        self.roll_angle = 0
        self.angle_of_attack = 0
        self.cl = 0
        self.cd = 0

    def update(self):
        self.calculate_angles()
        self.interpolate_polar()
        self.interpolate_density()

        lift = 0.5 * self.density * self.area * self.cl * sqrt(np.matmul(self.air_velocity.T, self.air_velocity))
        drag = 0.5 * self.density * self.area * self.cd * sqrt(np.matmul(self.air_velocity.T, self.air_velocity))

        self.force[1] = -drag
        self.force[2] = lift

    def calculate_angles(self):
        if self.air_velocity[2] > 0:
            self.climb_angle = atan(self.air_velocity[2] / sqrt(self.air_velocity[0] ** 2 + self.air_velocity[1] ** 2))
        else:
            self.climb_angle = 0
        self.body_rotation[0] = self.angle_of_attack + self.climb_angle

        if self.air_velocity[1] == 0 and self.air_velocity[0] == 0:
            self.yaw_angle = 0
        elif self.air_velocity[1] == 0 and self.air_velocity[0] > 0:
            self.yaw_angle = pi / 2 * (-1) * np.sign(self.air_velocity[0])
        else:
            self.yaw_angle = atan(self.air_velocity[0] / self.air_velocity[1]) * (-1)

    def interpolate_polar(self):
        count = 1
        while self.angle_of_attack <= self.polar_data[0, count]:
            count += 1

        self.cl = (self.angle_of_attack - self.polar_data[0, count - 1]) / \
                  (self.polar_data[0, count] - self.polar_data[0, count - 1]) * \
                  (self.polar_data[1, count] - self.polar_data[1, count - 1]) + self.polar_data[1, count - 1]

        self.cd = (self.angle_of_attack - self.polar_data[0, count - 1]) / \
                  (self.polar_data[0, count] - self.polar_data[0, count - 1]) * \
                  (self.polar_data[2, count] - self.polar_data[2, count - 1]) + self.polar_data[2, count - 1]

    def interpolate_density(self):
        altitude = (self.ground_position[2] / 1000)
        count = 1
        while altitude >= self.density_data[0, count]:
            count += 1

        self.density = (altitude - self.density_data[0, count - 1]) / \
                       (self.density_data[0, count] - self.density_data[0, count - 1]) * \
                       (self.density_data[1, count] - self.density_data[1, count - 1]) + self.density_data[1, count - 1]

