import datetime
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


    def get_result_from_api(self, date=None):
        LATITUDE = 60.39
        LONGITUDE = 5.32
        tday = datetime.date.today()
        tomorrow = tday + datetime.timedelta(days=1)
        date = input("Podaj datę (YYYY-mm-dd): \n")
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&" \
              f"longitude={LONGITUDE}&hourly=rain&daily=rain_sum&timezone=" \
              f"Europe%2FLondon&start_date={date}" \
              f"&end_date={date}"
        if date:
            date_valid = date_pattern.match(str(date))
            if date_valid:
                pass
            else:
                print("Podano nieprawidłową datę. Spróbuj ponownie.\n")
        if not date:
            tomorrow = tday + datetime.timedelta(days=1)
            date = tomorrow
        resp = requests.get(url).json()['daily']['rain_sum'][0]


    def get_result_from_file(self):
        if not os.path.exists(self.input_file):
            forecast = {}
        else:
            with open(self.input_file, "r") as f:
                forecast = json.load(f)
                return forecast


    def save_result_to_file(self):
        with open(input_file, 'w') as f:
            json.dump(self.weather_forecast, f)


    def __getitem__(self, date):
        if date not in self.weather_forecat:
            self.weather_forecast[date] = self.get_result_from_api(date)


    def __setitem__(self, date, rain_sum):
        self.weather_forecast[date] = rain_sum
        self.save_result_to_file()


    def items(self):
        for date, rain_sum in self.weather_forecast.items():
            yield (date, rain_sum)


input_file = 'fallback.json'

rain = WeatherForecast(input_file=input_file)
