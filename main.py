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

    def get_result_from_api(self, date=None):
        LATITUDE = 60.39
        LONGITUDE = 5.32
        today = datetime.date.today()
        date = date
        if not date:
            date = input("Podaj datę (YYYY-mm-dd): \n")
            if not date:
                tomorrow = today + datetime.timedelta(days=1)
                date = tomorrow
            date_valid = date_pattern.match(str(date))
            if not date_valid:
                print("Podano nieprawidłową datę. Spróbuj ponownie.\n")
                return False
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&" \
              f"longitude={LONGITUDE}&hourly=rain&daily=rain_sum&timezone=" \
              f"Europe%2FLondon&start_date={date}" \
              f"&end_date={date}"
        resp = requests.get(url).json()['daily']['rain_sum'][0]
        if resp > 0:
            print("Będzie padać.")
        elif resp == 0:
            print("Nie będzie padać.")
        else:
            print("Nie wiem.")

        self.weather_forecast[date] = resp

        return {str(date): float(resp)}

    def save_result_to_file(self):
        data_to_save = {}
        for date, rain_sum in self.weather_forecast.items():
            data_to_save[str(date)] = rain_sum
        with open(self.the_file, 'w') as f:
            json.dump(data_to_save, f)

    def __getitem__(self, date):
        if date not in self.weather_forecast:
            api_based_forecast = self.get_result_from_api(date)
            if api_based_forecast:
                self.weather_forecast[date] = [api_based_forecast['date'], api_based_forecast['rain_sum']]
                self.save_result_to_file()
            else:
                return None
        return self.weather_forecast[date]

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
weather_forecast.get_result_from_api()
weather_forecast.save_result_to_file()
