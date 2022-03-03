from numpy import array


class Wing:
    def __init__(self,
                 area: float,
                 ):

        self.area = area
        self.alpha = 0
        self.Cl = 0
        self.Cd = 0
        self.density = 1.225

        # Air Density Data
        self.density_data = den_array = array((
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
