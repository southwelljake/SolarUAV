from numpy import array, sqrt, arctan2, pi
from src.generatePaths import GeneratePaths


class YawController:
    def __init__(self,
                 kp: float,
                 path: GeneratePaths,
                 tolerance: float,
                 radius_target: float,
                 radius_land: float,
                 mission_type: str = 'p2p',
                 abort_mission: bool = True,
                 abort_time: float = None,
                 ):

        self.kp = kp
        self.path = path
        self.tolerance = tolerance
        self.mission_type = mission_type
        self.abort_mission = abort_mission
        self.abort_time = abort_time

        self.desired_yaw = 0
        self.roll_prev = 0
        self.point_index = 0
        self.landing = False

        self.radius_target = radius_target
        self.radius_land = radius_land

        self.points = None
        self.target_circle = None
        self.end_circle = None
        self.total_distance = 0
        self.distance_travelled = 0

        self.t_prev = 0
        self.at_target = False
        self.returning = False
        self.target_start = 0
        self.target_end = 0

    def create_path(self):
        self.points = self.path.generate()

        self.target_circle = array(([self.points[0, 0], self.points[0, 1] + self.radius_target],
                                    [self.points[0, 0] - self.radius_target, self.points[0, 1]],
                                    [self.points[0, 0], self.points[0, 1] - self.radius_target],
                                    [self.points[0, 0] + self.radius_target, self.points[0, 1]]))

        self.end_circle = array(([self.points[-1, 0], self.points[-1, 1] + self.radius_land],
                                 [self.points[-1, 0] - self.radius_land, self.points[-1, 1]],
                                 [self.points[-1, 0], self.points[-1, 1] - self.radius_land],
                                 [self.points[-1, 0] + self.radius_land, self.points[-1, 1]]))

        for j in range(1, len(self.points[:, 1])):
            self.total_distance += sqrt(
                (self.points[j][0] / 1000 - self.points[j - 1][0] / 1000) ** 2 +
                (self.points[j][1] / 1000 - self.points[j - 1][1] / 1000) ** 2
            )

    def calculate_roll_angle_p2p(self, t, state_var, yaw):
        if not self.landing:
            if self.point_index == len(self.points):
                self.landing = True
                self.point_index = 0

            desired_yaw = - arctan2(self.points[self.point_index, 0] - state_var[0],
                                    self.points[self.point_index, 1] - state_var[1])

            distance = sqrt((self.points[self.point_index, 0] - state_var[0]) ** 2 +
                            (self.points[self.point_index, 1] - state_var[1]) ** 2)

        else:
            if self.point_index == len(self.end_circle):
                self.point_index = 0

            desired_yaw = - arctan2(self.end_circle[self.point_index, 0] - state_var[0],
                                    self.end_circle[self.point_index, 1] - state_var[1])

            distance = sqrt((self.end_circle[self.point_index, 0] - state_var[0]) ** 2 +
                            (self.end_circle[self.point_index, 1] - state_var[1]) ** 2)

        roll = self.proportional_controller(t, yaw, desired_yaw)

        if distance < self.tolerance:
            self.point_index += 1

        return roll

    def calculate_roll_angle_target(self, t, initial_position, state_var, yaw):
        if not self.landing:
            if self.returning:
                # Return to initial position
                desired_yaw = - arctan2(initial_position[0] - state_var[0],
                                        initial_position[1] - state_var[1])

                distance = sqrt((initial_position[0] - state_var[0]) ** 2 +
                                (initial_position[1] - state_var[1]) ** 2)

                if distance < self.tolerance:
                    self.landing = True
                    self.point_index = 0
                    self.target_end = t

            elif not self.at_target:
                desired_yaw = - arctan2(self.points[0, 0] - state_var[0],
                                        self.points[0, 1] - state_var[1])

                distance = sqrt((self.points[0, 0] - state_var[0]) ** 2 +
                                (self.points[0, 1] - state_var[1]) ** 2)
            else:
                if self.point_index == len(self.target_circle):
                    self.point_index = 0

                desired_yaw = - arctan2(self.target_circle[self.point_index, 0] - state_var[0],
                                        self.target_circle[self.point_index, 1] - state_var[1])

                distance = sqrt((self.target_circle[self.point_index, 0] - state_var[0]) ** 2 +
                                (self.target_circle[self.point_index, 1] - state_var[1]) ** 2)
        else:
            if self.point_index == len(self.end_circle):
                self.point_index = 0

            desired_yaw = - arctan2(self.end_circle[self.point_index, 0] - state_var[0],
                                    self.end_circle[self.point_index, 1] - state_var[1])

            distance = sqrt((self.end_circle[self.point_index, 0] - state_var[0]) ** 2 +
                            (self.end_circle[self.point_index, 1] - state_var[1]) ** 2)

        if distance < self.tolerance:
            if not self.at_target:
                self.at_target = True
                self.target_start = t
            else:
                self.point_index += 1

        roll = self.proportional_controller(t, yaw, desired_yaw)

        return roll

    def proportional_controller(self, t, yaw, desired_yaw):

        # Proportional controller
        dt = t - self.t_prev  # Current time-step
        if dt > 0:
            # Evaluate roll angle based on the smaller difference between actual and demand path angle
            a = desired_yaw - yaw
            if desired_yaw < 0 < yaw:
                b = a + 2 * pi
                if abs(a) < abs(b):
                    roll = a * self.kp
                else:
                    roll = b * self.kp
            elif yaw < 0 < desired_yaw:
                b = a - 2 * pi
                if abs(a) < abs(b):
                    roll = a * self.kp
                else:
                    roll = b * self.kp
            else:
                roll = self.kp * a
            self.roll_prev = roll
        else:
            roll = self.roll_prev
        self.t_prev = t

        return roll

    def calculate_distance_travelled(self, state_var):

        for i in range(1, self.point_index):
            self.distance_travelled += sqrt(
                (self.points[i][0] / 1000 - self.points[i - 1][0] / 1000) ** 2 +
                (self.points[i][1] / 1000 - self.points[i - 1][1] / 1000) ** 2
            )

        self.distance_travelled += sqrt(
                (state_var[0] / 1000 - self.points[self.point_index - 1][0] / 1000) ** 2 +
                (state_var[1] / 1000 - self.points[self.point_index - 1][1] / 1000) ** 2
            )
