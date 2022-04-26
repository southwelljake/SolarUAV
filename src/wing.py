from numpy import array, floor, ceil, where, sqrt


class Wing:
    def __init__(self,
                 area: float,
                 ):

        """
        Class to represent wing subsystem.

        :param area: Wing area.
        """

        self.area = area
        self.alpha = 0
        self.Cl = 0
        self.Cd = 0
        self.density = 1.225
        self.gravity = 9.80665

        # Air Density Data
        self.density_data = array((
                    [0, 1.225],
                    [1, 1.112],
                    [2, 1.007],
                    [3, 0.9093],
                    [4, 0.8134],
                    [5, 0.7364],
                    [6, 0.6601],
                    [7, 0.5900],
                    [8, 0.5258],
                    [9, 0.4671],
                    [10, 0.4135]
        ))

        # Aerodynamics Coefficient Data
        self.aero_data = array((
                    [8.72, 1.139275, 0.0504],
                    [8.238, 1.093481, 0.042497],
                    [7.743, 1.046386, 0.036309],
                    [7.239, 0.998258, 0.033957],
                    [6.727, 0.94931, 0.02951],
                    [6.21, 0.899701, 0.026614],
                    [5.688, 0.849545, 0.024827],
                    [5.162, 0.798917, 0.023332],
                    [4.633, 0.747868, 0.021867],
                    [4.101, 0.696436, 0.020526],
                    [3.566, 0.64466, 0.019142],
                    [3.029, 0.592589, 0.017668],
                    [2.49, 0.540285, 0.016321],
                    [1.95, 0.48782, 0.015074],
                    [1.41, 0.435261, 0.013936]
        ))

    def calculate_density(self, state_var):
        # Evaluate air density at current altitude
        if state_var[2] > 0:
            alt_lower = floor(state_var[2] / 1000)
            density_lower = self.density_data[int(alt_lower), 1]
            alt_upper = ceil(state_var[2] / 1000)
            density_upper = self.density_data[int(alt_upper), 1]
            self.density = (density_upper - density_lower) * \
                (state_var[2] / 1000 - alt_lower) + density_lower

    def calculate_wing_forces(self, v_air):
        # Compute drag and lift
        drag = 0.5 * self.density * self.area * self.Cd * v_air ** 2
        lift = 0.5 * self.density * self.area * self.Cl * v_air ** 2

        return drag, lift

    def calculate_aero_coeff(self):
        # Evaluate Lift and Drag coefficient at current angle of attack
        index = where(self.aero_data == self.alpha)
        self.Cl, self.Cd = float(self.aero_data[index[0], 1]), float(self.aero_data[index[0], 2])

    def calculate_cruise_power(self, prop_efficiency, mass):
        self.calculate_aero_coeff()

        # Cruise velocity
        v_cruise = sqrt(
            2 * mass * self.gravity / (self.density * self.area * self.Cl))

        # Cruise power
        P_cruise = 0.5 * \
            (self.density * self.area * self.Cd * v_cruise ** 3) / prop_efficiency

        return v_cruise, P_cruise
