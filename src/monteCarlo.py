from src.simulation import Simulation
import time
import random


class MonteCarlo:
    def __init__(self,
                 simulation: Simulation,
                 samples: int,
                 file_path: str,
                 other_variables: list = None):

        """
        Class to run multiple simulations and vary parameters.

        :param simulation: A flight simulation.
        :param samples: No. of samples.
        :param file_path: File path to write results to.
        :param other_variables: List of parameters to vary and range of values.
            e.g. [['flight_model.aircraft.mass', [15, 20]],
                  ['flight_model.battery.capacity', [0.5 * 4590000, 1.5 * 4590000]]]
        """

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
                        if var[2] == 'int':
                            exec(var[0] + ' = ' + str(int(sample)))
                        else:
                            exec(var[0] + ' = ' + str(sample))

                flight_model.sim_flight()

                if flight_model.yaw.mission_type == 'p2p':
                    print('Simulation No.: ' + str(j + 1) + ' Duration: ' + str((time.time() - start_time)) +
                          's Outcome: ' + str(flight_model.yaw.distance_travelled /
                                              flight_model.yaw.total_distance * 100)
                          + '%\n')
                    f.write('Simulation No.: ' + str(j + 1) + ' Duration: ' + str((time.time() - start_time)) +
                            's Outcome: ' + str(flight_model.yaw.distance_travelled /
                                                flight_model.yaw.total_distance * 100)
                            + '%\n')

                elif flight_model.yaw.mission_type == 'target':
                    print('Simulation No.: ' + str(j + 1) + ', Duration: ' + str((time.time() - start_time)) +
                          's, Time on target: ' + str((flight_model.yaw.target_end - flight_model.yaw.target_start) /
                                                      3600) + ' hrs \n')
                    f.write('Simulation No.: ' + str(j + 1) + ', Duration: ' + str((time.time() - start_time)) +
                            's, Time on target: ' + str((flight_model.yaw.target_end - flight_model.yaw.target_start) /
                                                        3600) + ' hrs \n')

                if self.other_variables is not None:
                    for i in range(0, len(self.other_variables)):
                        print(self.other_variables[i][0] + ' = ' + str(eval(self.other_variables[i][0])) + '\n')
                        f.write(self.other_variables[i][0] + ' = ' + str(eval(self.other_variables[i][0])) + '\n')

                if flight_model.yaw.landing:
                    self.successful_flights += 1

            print("Success rate = " + str(100 * self.successful_flights / self.samples) + '\n')
            f.write("Success rate = " + str(100 * self.successful_flights / self.samples) + '\n')

