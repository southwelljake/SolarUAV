import timeit
import time
from src.cloudCover import CloudCover
from pathlib import Path

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

cloud_model = CloudCover(
    longitude=longitude,
    latitude=latitude,
    time_zone=time_zone,
    days=7,
)

no_forecasts = 1

for i in range(0, no_forecasts):
    cloud_model.generate_data()

    current_time = time.strftime("%H_%M_%S", time.localtime())
    file_path = Path('../data/cloud_data_winnipeg/cloud_cover_' + current_time + '.csv')

    cloud_model.data.to_csv(file_path, mode='w')

    print('Forecast: ' + str(i + 1) + '/' + str(no_forecasts) + ' at ' + current_time)

    if i < no_forecasts - 1:
        time.sleep(6*3600)

end_time = timeit.default_timer()
print("--- %s seconds ---" % (end_time - start_time))
