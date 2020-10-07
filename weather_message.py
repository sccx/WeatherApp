import json
import boto3
from datetime import datetime


def k_to_f(kelvin_temp):
    # Kelvin to Fahrenheit conversion: (0K - 273.15) * (9/5) + 32
    return (round((kelvin_temp - 273.15) * (9/5) + 32, 2))
 

# Retreive current weather from S3 bucket data
def current_weather(open_weather_json):
    temp = k_to_f(open_weather_json['current']['temp'])
    humidity = open_weather_json['current']['humidity']
    wind_speed = open_weather_json['current']['wind_speed']
    wind_direction = open_weather_json['current']['wind_deg'] # Call the function to convert degrees to cardinal directions
    visibility = open_weather_json['current']['weather'][0]['description']
    current_conditions = {'Temp': temp,
            'Humidity': humidity,
            'Wind Speed': wind_speed,
            'Wind Direction': wind_direction,
            'Visibility': visibility}
    return current_conditions


def forecast(ow_daily_dict):
    low, high = k_to_f(ow_daily_dict['temp']['min']), k_to_f(ow_daily_dict['temp']['max'])
    humidity = ow_daily_dict['humidity']
    wind_speed, wind_direction = ow_daily_dict['wind_speed'], ow_daily_dict['wind_deg']
    cond = ow_daily_dict['weather'][0]['main']
    weather_dict = {'Low temp':low,
                    'High temp':high,
                    'Humidity':humidity,
                    'Wind Speed':wind_speed,
                    'Wind Direction':wind_direction,
                    'Conditions':cond}
    return weather_dict


bucket_name = 'wpf-weather-data'
folder_name = 'weather-data'
file_date = datetime.now().strftime("%Y%m%d-%H%M")
ow_key = folder_name + "/" + file_date + "_owdata.txt"
aw_key = folder_name + "/" + file_date + "_awdata.txt"

s3_obj = boto3.client('s3')
s3_ow_obj = s3_obj.get_object(Bucket=bucket_name, Key=ow_key)
s3_ow_data = s3_ow_obj['Body'].read().decode('utf-8')
ow_json = json.loads(s3_ow_data)

s3_aw_obj = s3_obj.get_object(Bucket=bucket_name, Key=aw_key)
s3_aw_data = s3_aw_obj['Body'].read().decode('utf-8')
aw_json = json.loads(s3_aw_data)


the_current_weather = current_weather(ow_json)
today_forecast = forecast(ow_json['daily'][0])
tomorrow_forecast = forecast(ow_json['daily'][1])
rain = aw_json[0]['PrecipitationSummary']['Past24Hours']['Imperial']['Value']


# Weather Message

message_name = "message.txt"

with open(message_name, "w") as text_file:
    text_file.write("Current Conditions")
    for key,value in the_current_weather.items():
        text_file.write("\n{}: {}".format(key,value))

    text_file.write("\n\nRainfall Past 24 Hours\n")
    text_file.write(str(rain) + " inches")

    text_file.write("\n\nToday's Forecast")
    for key,value in today_forecast.items():
        text_file.write("\n{}: {}".format(key,value))

    text_file.write("\n\nTomorrow's Forecast")
    for key,value in tomorrow_forecast.items():
        text_file.write("\n{}: {}".format(key,value))


destination_folder = "weather-messages"
upload_name = destination_folder + "/" + datetime.now().strftime("%Y%m%d-%H%M") + "_" + message_name


s3 = boto3.resource('s3')
s3.Bucket(bucket_name).upload_file(message_name, upload_name)




