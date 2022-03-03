
class Aircraft:
    def __init__(self,
                 mass: float,
                 power_other: float,
                 ):

        self.mass = mass  # Aircraft mass
        self.P_other = power_other  # Non-aerodynamic power draw  (W)
