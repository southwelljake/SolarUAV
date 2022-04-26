
class Battery:
    def __init__(self,
                 initial_level: float,
                 capacity: float):

        """
        Class to store battery variables.

        :param initial_level: Initial battery energy (J)
        :param capacity:  Battery capacity (J)
        """

        self.level = initial_level
        self.capacity = capacity
