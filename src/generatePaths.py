import numpy as np


class GeneratePaths:
    def __init__(self,
                 shape: str = None,
                 start_point: list = None,
                 scanning_range: float = None,
                 scanning_width: float = None,
                 scanning_length: float = None,
                 scanning_area: float = None,
                 direction: str = None,
                 points: np.array = None,
                 ):

        self.shape = shape
        self.start_point = start_point
        self.range = scanning_range
        self.width = scanning_width
        self.length = scanning_length
        self.area = scanning_area
        self.direction = direction

        self.points = points

    def generate(self):

        if self.points is not None:
            return self.points
        else:
            if self.length is None:
                self.length = self.width
            elif self.area is not None and self.length is None:
                self.length = int(self.area/self.width)
            elif self.area is not None and self.width is None:
                self.width = int(self.area/self.length)

            self.points = np.array(([0, 0], self.start_point))
            start = np.array(self.start_point)

            if self.direction == 'w':
                mult = 1
            elif self.direction == 'e':
                mult = -1
            elif self.direction == 's':
                mult = 1
            else:
                mult = -1

            if self.shape == 'z':
                if self.direction == 'w' or self.direction == 'e':
                    while abs(self.start_point[1] - start[1]) < self.length:
                        self.points = np.r_[self.points, [np.array([start[0] - self.width * mult, start[1]])]]
                        self.points = np.r_[self.points, [np.array([start[0] - self.width * mult, start[1] + 2 *
                                                                    mult * self.range])]]
                        self.points = np.r_[self.points, [np.array([start[0], start[1] + 2 * mult * self.range])]]
                        self.points = np.r_[self.points, [np.array([start[0], start[1] + 4 * mult * self.range])]]
                        start[1] += 4 * self.range * mult

                    self.points = np.r_[self.points, [np.array([start[0] - self.width * mult, start[1]])]]
                    self.points = np.r_[self.points, [np.array([0, 0])]]

                else:
                    while abs(start[0] - self.start_point[0]) < self.length:
                        self.points = np.r_[self.points, [np.array([start[0], start[1] - self.width * mult])]]
                        self.points = np.r_[self.points, [np.array([start[0] - 2 * mult * self.range,
                                                                    start[1] - self.width * mult])]]
                        self.points = np.r_[self.points, [np.array([start[0] - 2 * mult * self.range,
                                                                    start[1]])]]
                        self.points = np.r_[self.points, [np.array([start[0] - 4 * mult * self.range, start[1]])]]

                        start[0] -= 4 * self.range * mult

                    self.points = np.r_[self.points, [np.array([start[0], start[1] - self.width * mult])]]
                    self.points = np.r_[self.points, [np.array([0, 0])]]

            elif self.shape == 's':
                width = self.width
                length = self.length

                if self.direction == 'w' or self.direction == 'e':
                    while length > self.range and width > self.range:
                        self.points = np.r_[self.points, [np.array([start[0] - width * mult, start[1]])]]
                        self.points = np.r_[self.points, [np.array([start[0] - width * mult,
                                                                    start[1] + mult * length])]]
                        self.points = np.r_[self.points, [np.array([start[0] - 2 * self.range * mult,
                                                                    start[1] + mult * length])]]
                        self.points = np.r_[self.points, [np.array([start[0] - 2 * self.range * mult,
                                                                    start[1] + 2 * mult * self.range])]]

                        start[0] -= 2 * self.range * mult
                        start[1] += 2 * self.range * mult
                        length -= 4 * self.range
                        width -= 4 * self.range

                    self.points = np.r_[self.points, [np.array([0, 0])]]

                else:
                    while length > self.range and width > self.range:
                        self.points = np.r_[self.points, [np.array([start[0], start[1] - width * mult])]]
                        self.points = np.r_[self.points, [np.array([start[0] - mult * length,
                                                                    start[1] - width * mult])]]
                        self.points = np.r_[self.points, [np.array([start[0] - mult * length, start[1]])]]
                        self.points = np.r_[self.points, [np.array([start[0] - 2 * mult * self.range, start[1]])]]

                        start[0] -= 2 * self.range * mult
                        start[1] -= 2 * self.range * mult
                        length -= 4 * self.range
                        width -= 4 * self.range

                    self.points = np.r_[self.points, [np.array([0, 0])]]

            return self.points
