import numpy as np


class Propeller:
    def __init__(self,
                 power: float,
                 efficiency: float,
                 dt: float):

        self.P_power = power
        self.P_efficiency = efficiency

        self.airVelocity = np.array([0, 0, 0])
        self.thrust = np.array([0, 0, 0])

        self.dt = dt
        self.time = 0

    def update(self):

        self.thrust[0] = self.P_efficiency * self.P_power / \
                         np.sqrt(self.airVelocity.dot(self.airVelocity))

        self.time += self.dt
