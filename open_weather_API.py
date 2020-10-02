# Call to Open Weather API to retrieve forecast data for Wild Pansy Farm

import requests
import pandas as pd
from datetime import datetime, timedelta
from credentials import app_id

# OpenWeather API call
def api_call(endpoint):
    response = requests.get(endpoint)
    json_data = response.json()
    return json_data

# Wild Pansy Farm veggie field latitude and longitude
lat = 38.824706
lon = -85.749063

forecast_endpoint = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&appid=".format(lat=lat, lon=lon) + app_id
inbound_message = api_call(forecast_endpoint)

# Save inbound data to S3 with timestamped_standard_name.json (?)




