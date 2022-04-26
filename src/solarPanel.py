
class SolarPanel:
    def __init__(self,
                 efficiency: float,
                 area: float):

        """
        Class to store solar panel parameters.

        :param efficiency: Solar panel efficiency.
        :param area: Solar panel area.
        """

        self.efficiency = efficiency
        self.area = area
        self.power = 0
