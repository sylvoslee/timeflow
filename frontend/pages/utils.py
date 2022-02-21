# pages shared logic goes here

import requests
from config import base_url

# fmt: off
year_month_list = ["2022_01","2022_02","2022_03","2022_04","2022_05",
"2022_06","2022_07","2022_08","2022_09","2022_10","2022_11", "2022_12"
]

hours = ["07", "08", "09", "10", "11", "12", "13", "14", "15", "16", 
    "17", "18", "19", "20", "21", "22"]
quarters = ["00", "15", "30", "45"]
# fmt: on

forecast_days_list = []
forecast_days_nr = range(1, 30)
for n in forecast_days_nr:
    forecast_days_list.append(n)


hours_list = []
for h in hours:
    for q in quarters:
        hours = f"{h}:{q}"
        hours_list.append(hours)
