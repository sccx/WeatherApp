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


# Wild Pansy Farm veggie field zip code
zip_code = "47229"

forecast_endpoint = "http://dataservice.accuweather.com/currentconditions/v1/" + zip_code + "/historical/24?apikey=" + config.accuweather_app_key + "&details=true"

inbound_message = api_call(forecast_endpoint)

# Create file with the data
with open('aw_data.txt', 'w') as outfile:
    json.dump(inbound_message, outfile)

# Save inbound data to S3 with timestamped_standard_name.json (?)
file_date = datetime.now().strftime("%Y%m%d-%H%M")
filename = file_date + '_' + 'awdata.txt'

s3 = boto3.resource('s3')
BUCKET = 'wpf-weather-data'

s3.Bucket(BUCKET).upload_file('owdata.txt', "openweather_data/" + filename)
