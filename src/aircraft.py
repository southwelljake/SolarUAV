
class Aircraft:
    def __init__(self,
                 mass: float,
                 power_other: float,
                 ):

        """
        Class to store general aircraft variables.

        :param mass: Mass of the aircraft (kg)
        :param power_other: Other Power draw on aircraft (W)
        """

        self.mass = mass
        self.P_other = power_other
