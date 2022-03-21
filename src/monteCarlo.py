from src.simulation import Simulation
import time
import random


class MonteCarlo:
    def __init__(self,
                 simulation: Simulation,
                 samples: int,
                 file_path: str,
                 other_variables: list = None):

        self.sim = simulation
        self.samples = samples
        self.file_path = file_path
        self.other_variables = other_variables

        self.successful_flights = 0

    def run(self):
        with open(self.file_path, 'w') as f:
            print('Total Simulations to run: ' + str(self.samples) + '\n')
            f.write('Total Simulations to run: ' + str(self.samples) + '\n')

            for j in range(0, self.samples):

                flight_model = self.sim.generate()
                start_time = time.time()

                if self.other_variables is not None:
                    for var in self.other_variables:
                        sample = random.uniform(var[1][0], var[1][1])
                        exec(var[0] + ' = ' + str(sample))

                flight_model.sim_flight()

                print('Simulation No.: ' + str(j + 1) + ' Duration: ' + str((time.time() - start_time)) +
                      's Outcome: ' + str(flight_model.yaw.landing) + '\n')
                f.write('Simulation No.: ' + str(j + 1) + ' Duration: ' + str((time.time() - start_time)) +
                        's Outcome: ' + str(flight_model.yaw.landing) + '\n')

                if self.other_variables is not None:
                    for i in range(0, len(self.other_variables)):
                        print(self.other_variables[i][0] + ' = ' + str(eval(self.other_variables[i][0])) + '\n')
                        f.write(self.other_variables[i][0] + ' = ' + str(eval(self.other_variables[i][0])) + '\n')

                if flight_model.yaw.landing:
                    self.successful_flights += 1

            print("Success rate = " + str(100 * self.successful_flights / self.samples) + '\n')
            f.write("Success rate = " + str(100 * self.successful_flights / self.samples) + '\n')

