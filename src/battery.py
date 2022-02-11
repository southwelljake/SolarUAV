
class Battery:
    def __init__(self,
                 initial_level: float,
                 capacity: float):

        self.level = initial_level
        self.capacity = capacity

        self.soc = self.level/self.capacity

    def update(self):
        self.soc = self.level / self.capacity
