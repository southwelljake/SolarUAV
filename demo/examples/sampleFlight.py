import timeit
import numpy as np
from src.simulation import Simulation
import matplotlib.pyplot as plt
import datetime
import pandas as pd
from src.generatePaths import GeneratePaths

"""
Demo to general any style of flight.
"""

# Set up path style
# Path 1 - Spiral or Zig Zag
# path = GeneratePaths(
#     shape='s',
#     start_point=[0, 50000],
#     scanning_range=1000,
#     scanning_width=50000,
#     scanning_length=50000,
#     direction='w',
# )

# Path 2 - Point to point
path = GeneratePaths(
    points=np.array(([0, 0], [250000, 200000], [0, 300000],
                    [-250000, 200000], [0, 0])),
)

# Path 3 - Target
# path = GeneratePaths(
#     points=np.array(([0, 50000], [0, 0])),
# )

start_time = timeit.default_timer()

# Specify location details
# London
latitude = 50
longitude = 0
time_zone = 'GMT'

# Specify launch hour
start_hour = 0
duration = 2

# Input cloud data from files
cloud_data = [
        # Day 1
        pd.read_csv('../../data/cloud_data/london_april/london_13_40_26.csv'),
        # pd.read_csv('../../data/cloud_data/london_april/london_19_40_34.csv'),
        # # Day 2
        # pd.read_csv('../../data/cloud_data/london_april/london_01_40_44.csv'),
        # pd.read_csv('../../data/cloud_data/london_april/london_07_40_52.csv'),
        # pd.read_csv('../../data/cloud_data/london_april/london_13_41_01.csv'),
]

# Set up simulation
sim = Simulation(
    latitude=latitude,
    longitude=longitude,
    time_zone=time_zone,
    start_hour=start_hour,
    duration=duration,
    # cloud_data=[pd.read_csv('../../data/general_cloud_data/blank_cloud_data.csv')],
    cloud_data=cloud_data,
    path=path,
    mission_type='p2p',
    # mission_type='target',
    abort_mission=True,
    date=datetime.date(2022, 4, 4),
)

flight_model = sim.generate()

# Define flight mission
flight_model.collect_power_data = True  # Collect power data of simulation

flight_model.sim_flight()

if sim.mission_type == 'p2p':
    print('Percentage completed before returning = ' + str(round((flight_model.yaw.distance_travelled /
                                                           flight_model.yaw.total_distance * 100), 2)) + '%')
else:
    print("Time on target: " + str((flight_model.yaw.target_end - flight_model.yaw.target_start) / 3600) + ' hours')

end_time = timeit.default_timer()
print("--- %s seconds ---" % (end_time - start_time))

# Plot results
# fig1, ax1 = plt.subplots(5, 1, figsize=(8, 12))
#
# v_hor = np.sqrt(flight_model.state_var[3, :] ** 2 + flight_model.state_var[4, :] ** 2)
#
# ax1[0].plot(flight_model.sol_t, v_hor)
# ax1[0].set_ylabel('Horizontal Velocity (m/s)')
# ax1[0].grid()
#
# ax1[1].plot(flight_model.sol_t, flight_model.state_var[5, :])
# ax1[1].set_ylabel('Z Velocity (m/s)')
# ax1[1].set_xlabel('Time (hrs)')
# ax1[1].grid()
#
# ax1[2].plot(flight_model.sol_t, flight_model.state_var[2, :])
# ax1[2].set_ylabel('Altitude (m)')
# ax1[2].set_xlabel('Time (hrs)')
# ax1[2].grid()
#
# ax1[3].plot(flight_model.sol_t, flight_model.state_var[6, :] * 100 / flight_model.battery.capacity, label=r'$SoC$')
# ax1[3].set_ylabel('State of Charge (%)')
# ax1[3].set_ylim(0, 110)
# ax1[3].grid()
#
# ax1[4].plot(flight_model.tx, flight_model.P_netx, 'r', label=r'$P_{net}$')
# ax1[4].plot(flight_model.tx, flight_model.P_propx, 'b', label=r'$P_{prop}$')
# ax1[4].set_xlabel('Time (hrs)')
# ax1[4].set_ylabel('Power (W)')
# ax1[4].grid()
#
# # Plot available solar power
# t_max = int(np.ceil(flight_model.sol_t[-1]))
# t_pslr = np.arange(int(flight_model.start_time), t_max)
# P_slr = np.zeros(0)
# P_slr_cc = np.zeros(0)
# for ttt in t_pslr:
#     P_slr = np.append(P_slr, flight_model.solar_model.calculate_solar_power(
#         ttt, flight_model.solar_panel.area, 0) * flight_model.solar_panel.efficiency)
#     P_slr_cc = np.append(P_slr_cc, flight_model.solar_model.calculate_solar_power(
#         ttt, flight_model.solar_panel.area, flight_model.cloud_cover.cloud_cover[ttt, 1]) *
#                          flight_model.solar_panel.efficiency)
# ax1[4].plot(t_pslr, P_slr, '--', label=r'$P_{solar}$')
# ax1[4].plot(t_pslr, P_slr_cc, '--', label=r'$P_{solar} w/CC$')
# ax1[4].legend(loc='upper left')

fig1, ax1 = plt.subplots(nrows=2)

ax1[0].plot(flight_model.sol_t, flight_model.state_var[6, :] * 100 / flight_model.battery.capacity, label=r'$SoC$')
ax1[0].set_ylabel('State of Charge (%)')
ax1[0].set_ylim(0, 110)
ax1[0].grid()

ax1[1].plot(flight_model.tx, flight_model.P_netx, 'r', label=r'$P_{net}$')
ax1[1].plot(flight_model.tx, flight_model.P_propx, 'b', label=r'$P_{prop}$')
ax1[1].set_xlabel('Time (hrs)')
ax1[1].set_ylabel('Power (W)')
ax1[1].grid()

# Plot available solar power
t_max = int(np.ceil(flight_model.sol_t[-1]))
t_pslr = np.arange(int(flight_model.start_time), t_max)
P_slr = np.zeros(0)
P_slr_cc = np.zeros(0)
for ttt in t_pslr:
    P_slr = np.append(P_slr, flight_model.solar_model.calculate_solar_power(
        ttt, flight_model.solar_panel.area, 0) * flight_model.solar_panel.efficiency)
    P_slr_cc = np.append(P_slr_cc, flight_model.solar_model.calculate_solar_power(
        ttt, flight_model.solar_panel.area, flight_model.cloud_cover.cloud_cover[ttt, 1]) *
                         flight_model.solar_panel.efficiency)
ax1[1].plot(t_pslr, P_slr, '--', label=r'$P_{solar}$')
ax1[1].plot(t_pslr, P_slr_cc, '--', label=r'$P_{solar} w/CC$')
ax1[1].legend(loc='upper left')

fig2, ax2 = plt.subplots()

ax2.plot(flight_model.state_var[0, :] / 1000, flight_model.state_var[1, :] / 1000)
ax2.plot(flight_model.yaw.points[:, 0] / 1000, flight_model.yaw.points[:, 1] / 1000, 'xr')
ax2.set_xlabel('X Distance (km)')
ax2.set_ylabel('Y Distance (km)')

# if flight_model.yaw.mission_type == 'target':
#     ax2.text(flight_model.yaw.points[0, 0] / 1000, flight_model.yaw.points[0, 1] / 1000 + 5, 'Target')
#     ax2.text(flight_model.yaw.points[-1, 0] / 1000 + 1, flight_model.yaw.points[-1, 1] / 1000 + 4, 'Start')
#     ax2.text(flight_model.yaw.points[-1, 0] / 1000 - 3, flight_model.yaw.points[-1, 1] / 1000 + 4, 'End')
# else:
#     ax2.text(flight_model.yaw.points[0, 0] / 1000 + 20, flight_model.yaw.points[0, 1] / 1000 + 5, 'Start')
#     ax2.text(flight_model.yaw.points[-1, 0] / 1000 - 50, flight_model.yaw.points[-1, 1] / 1000 + 5, 'End')
#     for i in range(1, len(flight_model.yaw.points) - 1):
#         ax2.text(flight_model.yaw.points[i, 0] / 1000 - 5, flight_model.yaw.points[i, 1] / 1000 + 5, 'P' + str(i))

fig3, ax3 = plt.subplots()

ax3.plot(flight_model.cloud_cover.cloud_cover[:, 0], flight_model.cloud_cover.cloud_cover[:, 1])
ax3.set_ylabel('Cloud cover (%)')
ax3.set_xlabel('Time (hrs)')

plt.show()
