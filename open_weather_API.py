# Call to Open Weather API to retrieve forecast data for Wild Pansy Farm
import requests
import pandas as pd
from datetime import datetime, timedelta
import config
import boto3
import json


# OpenWeather API call
def api_call(endpoint):
    response = requests.get(endpoint)
    json_data = response.json()
    return json_data


# Wild Pansy Farm veggie field latitude and longitude
lat = 38.824706
lon = -85.749063

forecast_endpoint = "https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely&appid=".format(lat=lat, lon=lon) + config.open_weather_app_id
inbound_message = api_call(forecast_endpoint)

# Create file with the data
with open('owdata.txt', 'w') as outfile:
    json.dump(inbound_message, outfile)

# Save inbound data to S3 with timestamped_standard_name.json (?)
file_date = datetime.now().strftime("%Y%m%d-%H%M")
filename = file_date + '_' + 'owdata.txt'

s3 = boto3.resource('s3')
BUCKET = 'wpf-weather-data'

s3.Bucket(BUCKET).upload_file('owdata.txt', "openweather_data/" + filename)

