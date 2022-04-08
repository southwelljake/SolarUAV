
class Propeller:
    def __init__(self,
                 efficiency: float):

        self.efficiency = efficiency  # Efficiency of propellers
        self.power = 0  # Power to propellers (W)

    def calculate_propeller_thrust(self, v_air, state_var):
        # Compute thrust
        if v_air != 0 and state_var[6] > 0:
            thrust = abs(self.power) * self.efficiency / v_air
        else:
            thrust = 0

        return thrust
