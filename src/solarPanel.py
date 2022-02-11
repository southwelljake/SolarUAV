
class SolarPanel:
    def __init__(self,
                 efficiency: float,
                 area: float):

        self.efficiency = efficiency
        self.area = area

        self.P_solar = 0

        # Input states
        self.irradiance = 0
        self.cloud_cover = 0

    def update(self):

        self.P_solar = self.efficiency * self.area * self.irradiance * \
                       (1 - 0.75 * self.cloud_cover ** 0.75)

