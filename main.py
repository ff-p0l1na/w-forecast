import datetime
import json
import os
import re
import requests

# data YYYY-mm-dd w postaci regular expression:
date_pattern = re.compile(r'^\d{4}-(?:0[1-9]|1[0-2])-([012]\d|3[01])$')


class WeatherForecast:
    def __init__(self, the_file):
        self.the_file = the_file
        self.weather_forecast = self.get_result_from_file()

    def get_result_from_file(self):
        if not os.path.exists(self.the_file):
            forecast = {}
        else:
            with open(self.the_file, "r") as f:
                forecast = json.load(f)
        return forecast

    def get_result_from_api(self, date):
        LATITUDE = 60.39
        LONGITUDE = 5.32
        date = date
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&" \
              f"longitude={LONGITUDE}&hourly=rain&daily=rain_sum&timezone=" \
              f"Europe%2FLondon&start_date={date}" \
              f"&end_date={date}"
        resp = requests.get(url).json()['daily']['rain_sum'][0]

        self.weather_forecast[date] = resp

        return {str(date): float(resp)}

    def save_result_to_file(self):
        data_to_save = {}
        for date, rain_sum in self.weather_forecast.items():
            data_to_save[str(date)] = rain_sum
        with open(self.the_file, 'w') as f:
            json.dump(data_to_save, f)

    def __getitem__(self, date=None):
        today = datetime.date.today()
        if not date:
            date = input("Podaj datę (YYYY-mm-dd): \n")
            if not date:
                tomorrow = today + datetime.timedelta(days=1)
                date = str(tomorrow)
            date_valid = date_pattern.match(str(date))
            if not date_valid:
                print("Podano nieprawidłową datę. Spróbuj ponownie.\n")
                return False
        if str(date) not in self.weather_forecast:
            api_based_forecast = self.get_result_from_api(date)
            if api_based_forecast:
                self.save_result_to_file()
        elif str(date) in self.weather_forecast:
            weather_forecast.get_result_from_file()
        return self.weather_forecast[str(date)]

    def __setitem__(self, date, rain_sum):
        self.weather_forecast[date] = rain_sum
        self.save_result_to_file()

    def items(self):
        for date, rain_sum in self.weather_forecast.items():
            yield date, rain_sum

    def __iter__(self):
        dates = list(self.weather_forecast.keys())
        return iter(dates)


input_file = 'fallback.json'

weather_forecast = WeatherForecast(input_file)
check_forecast = weather_forecast.__getitem__()
if check_forecast > 0:
    print("Będzie padać.")
elif check_forecast == 0:
    print("Nie będzie padać.")
else:
    print("Nie wiem :(")





