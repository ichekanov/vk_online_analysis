from datetime import datetime
from utils.parse_all_sessions_from_raw import parse_all_sessions_from_raw
from time import time

start = time()
parse_all_sessions_from_raw(
    "/Users/ichek/Documents/GitHub/vk_online_analysis/data/raw_data",
    datetime(2022, 3, 15),
    datetime(2022, 6, 2)
)
end = time()

print(f"Итого затрачено {end-start} секунд ({(end-start)/60} минут)")
