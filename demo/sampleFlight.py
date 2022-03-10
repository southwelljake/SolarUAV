import timeit
import numpy as np
from src.simulation import Simulation
import matplotlib.pyplot as plt

start_time = timeit.default_timer()

# Central Canada
# latitude = 55
# longitude = -100
# time_zone = 'America/Winnipeg'

# Miami
# latitude = 25.7617
# longitude = 80.1918
# time_zone = 'EST'

# London
latitude = 51.5072
longitude = 0.1276
time_zone = 'GMT'
start_hour = 24
duration = 2

sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
)

flight_model = sim.generate()

# Define flight mission
flight_model.collect_power_data = True  # Collect power data of simulation

flight_model.sim_flight()

end_time = timeit.default_timer()
print("--- %s seconds ---" % (end_time - start_time))

# Plot results
fig1, ax1 = plt.subplots(5, 1, figsize=(8, 12))

v_grhor = np.sqrt(flight_model.state_var[3, :] ** 2 + flight_model.state_var[4, :] ** 2)

ax1[0].plot(flight_model.sol_t, v_grhor)
ax1[0].set_ylabel('Horizontal Velocity (m/s)')
ax1[0].grid()

ax1[1].plot(flight_model.sol_t, flight_model.state_var[5, :])
ax1[1].set_ylabel('Z Velocity (m/s)')
ax1[1].set_xlabel('Time (hrs)')
ax1[1].grid()

ax1[2].plot(flight_model.sol_t, flight_model.state_var[2, :])
ax1[2].set_ylabel('Altitude (m)')
ax1[2].set_xlabel('Time (hrs)')
ax1[2].grid()

ax1[3].plot(flight_model.sol_t, flight_model.state_var[6, :] * 100 / flight_model.battery.capacity, label=r'$SoC$')
ax1[3].set_ylabel('State of Charge (%)')
ax1[3].set_ylim(0, 110)
ax1[3].grid()

ax1[4].plot(flight_model.tx, flight_model.P_netx, 'r', label=r'$P_{net}$')
ax1[4].plot(flight_model.tx, flight_model.P_propx, 'b', label=r'$P_{prop}$')
ax1[4].set_xlabel('Time (hrs)')
ax1[4].set_ylabel('Power (W)')
ax1[4].grid()

# Plot available solar power
t_max = int(np.ceil(flight_model.sol_t[-1]))
t_pslr = np.arange(int(flight_model.start_time), t_max)
P_slr = np.zeros(0)
P_slr_cc = np.zeros(0)
for ttt in t_pslr:
    P_slr = np.append(P_slr, flight_model.weather.solar_model.calculate_solar_power(
        ttt, flight_model.solar_panel.area, 0) * flight_model.solar_panel.efficiency)
    P_slr_cc = np.append(P_slr_cc, flight_model.weather.solar_model.calculate_solar_power(
        ttt, flight_model.solar_panel.area, flight_model.weather.cloud_cover.cloud_cover[ttt, 1]) *
                         flight_model.solar_panel.efficiency)
ax1[4].plot(t_pslr, P_slr, '--', label=r'$P_{solar}$')
ax1[4].plot(t_pslr, P_slr_cc, '--', label=r'$P_{solar} w/CC$')
ax1[4].legend(loc='upper left')

fig2, ax2 = plt.subplots()

ax2.plot(flight_model.state_var[0, :] / 1000, flight_model.state_var[1, :] / 1000)
ax2.plot(flight_model.yaw.points[:, 0] / 1000, flight_model.yaw.points[:, 1] / 1000, 'xr')
ax2.set_xlabel('X Distance (km)')
ax2.set_ylabel('Y Distance (km)')

fig3, ax3 = plt.subplots()

ax3.plot(flight_model.weather.cloud_cover.cloud_cover[:, 0], flight_model.weather.cloud_cover.cloud_cover[:, 1])
ax3.set_ylabel('Cloud cover (%)')
ax3.set_xlabel('Time (hrs)')

plt.show()
