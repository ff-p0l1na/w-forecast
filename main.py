from datetime import datetime
from datetime import timedelta
import json
import os
import pprint
import re
import requests

# data YYYY-mm-dd w postaci regular expression
date_pattern = re.compile(r'^\d{4}-(?:0[1-9]|1[0-2])-([012]\d|3[01])$')


class WeatherForecast:
    def __init__(self, input_file):
        self.input_file = input_file
        self.weather_forecast = self.get_result_from_file()


    def get_result_from_file(self):
        if not os.path.exists(self.input_file):
            forecast = {}
        else:
            with open(self.input_file, "r") as f:
                forecast = json.load(f)
                return forecast


    def get_result_from_api(self, date):
        latitude = 60.39
        longitude = 5.32
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        date = input("data pls \n")
        url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&" \
              f"longitude={longitude}&hourly=rain&daily=rain_sum&timezone=" \
              f"Europe%2FLondon&start_date={date}" \
              f"&end_date={date}"
        if date:
            resp = requests.get(url)
        else:
            date = tomorrow
            resp = requests.get(url)


    def __getitem__(self, date):
        if date not in self.weather_forecat:
            self.weather_forecast[date] = self.get_result_from_api(date)
