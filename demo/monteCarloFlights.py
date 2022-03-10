import timeit
import numpy as np
from src.simulation import Simulation

start_time = timeit.default_timer()

sim_results = np.array([False] * 100)

# London
latitude = 51.5072
longitude = 0.1276
time_zone = 'GMT'
start_hour = 0
duration = 2

sim_index = 0
successful_flights = 0

while sim_index < len(sim_results):
    sim = Simulation(
        latitude=latitude,
        longitude=longitude,
        time_zone=time_zone,
        start_hour=start_hour,
        duration=duration,
    )

    flight_model = sim.generate()

    flight_model.sim_flight()

    sim_results[sim_index] = flight_model.yaw.landing

    if flight_model.yaw.landing:
        successful_flights += 1

    sim_index += 1

end_time = timeit.default_timer()
print("--- %s seconds ---" % (end_time - start_time))
print("Success rate = " + str(100 * successful_flights / len(sim_results)))
print(sim_results)
