
class Propeller:
    def __init__(self,
                 efficiency: float):

        """
        Class to represent propeller subsystem.

        :param efficiency: Propeller efficiency.
        """

        self.efficiency = efficiency
        self.power = 0

    def calculate_propeller_thrust(self, v_air, state_var):
        # Compute thrust
        if v_air != 0 and state_var[6] > 0:
            thrust = abs(self.power) * self.efficiency / v_air
        else:
            thrust = 0

        return thrust
