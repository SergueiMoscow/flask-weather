import requests
import json
from flask import render_template
import plotly.express as px

import httpx

import private


class Weather:

    @staticmethod
    def render():
        return render_template("weather.html")

    @staticmethod
    def search_location(query) -> list:
        url = 'https://cleaner.dadata.ru/api/v1/clean/address'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': private.DADATA_TOKEN,
            'X-Secret': private.DADATA_SECRET
        }
        data = [query]
        client = httpx.Client(base_url=url, headers=headers)
        response = client.post(url, json=data)
        response_json = response.json()

        result = []
        for found in response_json:
            result.append({'location': found['result'], 'lat': found['geo_lat'], 'lon': found['geo_lon']})
        return result

    @staticmethod
    def get_current_state(location: dict) -> dict:
        # https://openweathermap.org/current
        # https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
        url = f"https://api.openweathermap.org/data/2.5/weather?" \
              f"lat={location['lat']}&" \
              f"lon={location['lon']}&" \
              f"appid={private.OPENWEATHERMAP_API_KEY}&" \
              f"units=metric&" \
              f"lang=ru"
        # print(url)
        response = requests.get(url)
        # print(f'Get_Current_State: {response.json()}')
        return response.json()

    @staticmethod
    def get_forecast(location: dict) -> dict:
        # https://openweathermap.org/forecast16
        # https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt={cnt}&appid={API key}
        url = f"https://api.openweathermap.org/data/2.5/forecast?" \
              f"lat={location['lat']}&" \
              f"lon={location['lon']}&" \
              f"units=metric&" \
              f"appid={private.OPENWEATHERMAP_API_KEY}"
        print(f'Ur: {url}')
        response = requests.get(url)
        print(f'Forecast: {response.json()}')
        return response.json()

    @staticmethod
    def get_forecast_fig(forecast_from_server: dict):
        forecast = forecast_from_server['list']
        date_time = []
        temp = []
        # clouds = []
        # humidity = []
        # forecast_clean = []
        for dt in forecast:
            date_time.append(dt['dt_txt'])
            temp.append(dt['main']['temp'])
            # clouds.append(dt['clouds']['all'])
            # forecast_clean.append({'dt': dt['dt_txt'], 'temp': dt['main']['temp'], 'humidity': dt['main']['humidity'], 'clouds': dt['clouds']['all']})
            # print(dt)

        # print(forecast_clean)
        fig = px.line(x=date_time, y=temp)
        return fig
