import timeit
import numpy as np
from src.flightModel import FlightModel
from src.aircraft import Aircraft
from src.altitude import AltitudeController
from src.battery import Battery
from src.propeller import Propeller
from src.solarPanel import SolarPanel
from src.solarModel import SolarModel
from src.wing import Wing
from src.yaw import YawController
from src.cloudCover import CloudCover
from src.weather import Weather
import matplotlib.pyplot as plt

start_time = timeit.default_timer()

# Central Canada
# latitude = 55
# longitude = -100
# time_zone = 'America/Winnipeg'

# London
latitude = 51.5072
longitude = 0.1276
time_zone = 'GMT'

solar_model = SolarModel(
    longitude=longitude,
    latitude=latitude,
    time_zone=time_zone,
    days=3,
)

solar_model.generate_data()

# Cloud Cover Model
cloud_cover = CloudCover(
    longitude=longitude,
    latitude=latitude,
    time_zone=time_zone,
    days=3,
)
cloud_cover.generate_data()

# Weather Data
weather = Weather(
    solar_model=solar_model,
    cloud_cover=cloud_cover,
)

weather.generate_data()

# Aircraft Properties
aircraft = Aircraft(
    mass=18.2,
    power_other=10,
)

# Altitude Controller Properties
altitude = AltitudeController(
    store_PE=False,
    cruise_alt=500,
    max_cruise_alt=8000,
    aoa_init=8,
    aoa_desc=2,
    asc_rate=1.6,
    dsc_rate=0.5,
)

# Battery Properties
battery = Battery(
    initial_level=4590000,
    capacity=4590000,
)

# Propeller Properties
propeller = Propeller(
    efficiency=0.72,
)

# Solar Panel Properties
solar_panel = SolarPanel(
    efficiency=0.2,
    area=2.857,
)

# Wing Properties
wing = Wing(
    area=2.857,
)

# Yaw Controller Properties
yaw = YawController(
    kp=0.1,
    points=np.array(([300000, 450000], [0, 650000], [-300000, 450000], [0, 0])),
    radius=100,
)

# Create Flight Model
flight_model = FlightModel(
    start_time=6,
    duration=72,
    dt=0.01,
    launch_velocity=[0, 15, 0],
    aircraft=aircraft,
    altitude=altitude,
    battery=battery,
    propeller=propeller,
    weather=weather,
    solar_panel=solar_panel,
    wing=wing,
    yaw=yaw
)

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

ax1[3].plot(flight_model.sol_t, flight_model.state_var[6, :] * 100 / battery.capacity, label=r'$SoC$')
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
    P_slr = np.append(P_slr, solar_model.calculate_solar_power(
        ttt, solar_panel.area, 0) * solar_panel.efficiency)
    P_slr_cc = np.append(P_slr_cc, solar_model.calculate_solar_power(
        ttt, solar_panel.area, cloud_cover.cloud_cover[ttt, 1]) * solar_panel.efficiency)
ax1[4].plot(t_pslr, P_slr, '--', label=r'$P_{solar}$')
ax1[4].plot(t_pslr, P_slr_cc, '--', label=r'$P_{solar} w/CC$')
ax1[4].legend(loc='upper left')

fig2, ax2 = plt.subplots()

ax2.plot(flight_model.state_var[0, :] / 1000, flight_model.state_var[1, :] / 1000)
ax2.set_xlabel('X Distance (km)')
ax2.set_ylabel('Y Distance (km)')

fig3, ax3 = plt.subplots()

cloud_vars = ['total_clouds', 'low_clouds', 'mid_clouds', 'high_clouds']
ax3.plot(cloud_cover.data[cloud_vars])
ax3.set_ylabel('Cloud cover %')
ax3.set_xlabel('Forecast Time ({})'.format(cloud_cover.time_zone))
ax3.set_title('GFS 0.5 deg forecast for lat={}, lon={}'.format(cloud_cover.latitude, cloud_cover.longitude))
ax3.legend(cloud_vars)

plt.show()
