
class SolarPanel:
    def __init__(self,
                 efficiency: float,
                 area: float):

        self.efficiency = efficiency
        self.area = area
        self.power = 0
