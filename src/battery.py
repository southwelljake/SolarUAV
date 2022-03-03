
class Battery:
    def __init__(self,
                 initial_level: float,
                 capacity: float):

        self.level = initial_level  # Initial battery energy (J)
        self.capacity = capacity  # Battery capacity (J)
