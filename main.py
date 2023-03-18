import datetime
import json
import os
import re
import requests
# data YYYY-mm-dd w postaci regular expression
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
        if not date:
            date = input("Podaj datę (YYYY-mm-dd): \n")
            if not date:
                tomorrow = today + datetime.timedelta(days=1)
                date = tomorrow
            date_valid = date_pattern.match(str(date))
            if not date_valid:
                print("Podano nieprawidłową datę. Spróbuj ponownie.\n")
                pass
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&" \
              f"longitude={LONGITUDE}&hourly=rain&daily=rain_sum&timezone=" \
              f"Europe%2FLondon&start_date={date}" \
              f"&end_date={date}"
        resp = requests.get(url).json()['daily']['rain_sum'][0]

        return {
            'date': date,
            'rain_sum': resp
        }

    def save_result_to_file(self):
        with open(self.the_file, 'w') as f:
            json.dump(self.weather_forecast, f)

    def __getitem__(self, date):
        if date not in self.weather_forecast:
            api_based_forecast = self.get_result_from_api(date)
            self.weather_forecast[date] = [api_based_forecast['date'], api_based_forecast['rain_sum']]
            self.save_result_to_file()
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
wf = WeatherForecast(the_file=input_file)



# weather_forecast[date]  # da odpowiedź na temat pogody dla podanej daty
# weather_forecast.items()  # zwróci generator tupli w formacie (data, pogoda) dla już zapisanych rezultatów przy wywołaniu
# weather_forecast  # to iterator zwracający wszystkie daty, dla których znana jest pogoda

