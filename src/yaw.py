from numpy import array


class YawController:
    def __init__(self,
                 kp: float,
                 points: array,
                 radius: float,):

        self.kp = kp
        self.points = points
        self.radius = radius

        self.desired_yaw = 0
        self.roll_prev = 0
        self.point_index = 0
        self.landing = False

        self.end_circle = array(([self.points[-1, 0], self.points[-1, 1] + 2000],
                                 [self.points[-1, 0] - 2000, self.points[-1, 1]],
                                 [self.points[-1, 0], self.points[-1, 1] - 2000],
                                 [self.points[-1, 0] + 2000, self.points[-1, 1]]))
