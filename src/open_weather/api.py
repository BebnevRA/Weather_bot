import requests

from src.open_weather.config import APY_KEY, LANGUAGE, UNITS


class OpenWeather:

    def __init__(self, city_name):
        link = f'https://api.openweathermap.org/data/2.5/weather?q=' \
               f'{city_name}&appid={APY_KEY}'

        res = requests.get(link, params={'lang': LANGUAGE, 'units': UNITS})

        # print('BODY:')
        # for k, v in res.json().items():
        #     print(k, ': ', v)
        if res.status_code == 200:
            self.error_message = False
        else:
            if res.status_code == 404:
                self.error_message = 'Город не найден, попробуйте еще.'
            else:
                self.error_message = 'Произошла неизвестная ошибка!'
            return

        self.city = res.json()['name']
        self.description = res.json()['weather'][0]['description']
        self.temp_now = res.json()['main']['temp']
        self.temp_min = res.json()['main']['temp_min']
        self.temp_max = res.json()['main']['temp_max']
        self.feels_like = res.json()['main']['feels_like']
        self.wind = res.json()['wind']['speed']

    def is_valid_city_name(self):
        if not self.error_message:
            return True
        else:
            return False

    def weather_str(self):
        return f'В городе {self.city} сейчас {self.temp_now}°.'
